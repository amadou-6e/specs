---
title: Ray execution and resource placement
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray execution and resource placement

This page describes source-wired behavior in `theseo-anysearch` commit [`fd94554c`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected on 2026-09-28. Its Ray integration tests were **read, not run** for this investigation. Resource declarations are not measurements of placement, concurrency, throughput, or cleanup on a live cluster. RLlib configuration APIs belong in [environment integration](../rllib/environment-integration.md); evaluation and training guarantees belong to [training and tuning](../../subsystems/training-and-tuning/README.md).

## Runtime ownership

Standalone algorithm builders share `_ensure_ray_runtime`: an already initialized runtime is reused; otherwise the builder initializes local Ray with at least `num_env_runners + 1` CPUs, dashboard disabled, and a temporary directory. DQN and Rainbow also account for configured remote learner CPUs. This is a local initialization budget, not proof that requested actors can be scheduled. See [`ppo.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L78-L115) and [DQN](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py).

`TuneRunner` builds options for either an external Ray address or local temporary storage. It records whether Ray was initialized before entry and conditionally calls `ray.shutdown()` in `finally`; callers must not assume it owns a preexisting runtime. Tune trainables separately stop their constructed `Algorithm` in `finally`. Read these cleanup scopes separately when diagnosing leaked resources. See [`tune_runner.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L970-L995) and [its execution/cleanup path](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1320-L1580). Source inspection does not establish successful shutdown after process crashes or forced cancellation.

## Tune trial boundary and resources

The module-level trainable is designed to cross Ray's cloudpickle boundary. It reconstructs configuration and paths, materializes the Python extension and native binary in the trial process before creating a trainer, then stops its algorithm on normal exception unwinding. A locally importable extension is therefore not evidence that a remote trial can load it. See [`tune_runner.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L286-L593).

For a Tune trial, the code declares a `PlacementGroupFactory` with a driver CPU/GPU bundle, one training EnvRunner CPU/GPU bundle, and one CPU bundle for each evaluation runner, using `SPREAD`. It applies `with_resources` to the base trainable **before** `with_parameters`; the source comment says reversing that order drops the placement group in the Ray version used there. Trials set `reuse_actors=False` to avoid stale placement-group bundle references. These are requested bundles, not observed allocations. See [`tune_runner.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1335-L1400) and [trial setup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1483-L1507).

Training settings expose runner count, environments per runner, per-runner GPU, and remote learners. Modern PPO, DQN, and Rainbow forward runner/vectorization fields through the shared PPO helper; PPO fixes `num_learners=0`, while DQN/Rainbow can configure remote learners. The Tune placement-group construction does not visibly add learner-specific bundles for the latter case. Treat a remote-learner Tune scheduling mismatch as a **hazard to test**, not a demonstrated failure. See [`training.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/training.py#L103-L108), [`ppo.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L23-L39), and the [Tune resource declaration](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1335-L1400). Actual worker creation and environment count remain runtime-unverified here.

## Parallel evaluation execution

The evaluation helper uses healthy remote evaluation runners, if available, with per-episode seed assignment and sorted results; otherwise it falls back to local collection, including a vector-collection path. Weight synchronization is optional, and the callback is serialized without retaining an `Algorithm` reference. Thus `parallel_evaluation=True` in configuration is not proof that an episode ran remotely; runner availability determines the branch. See [`parallel.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L18-L66) and [collection branches](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L276-L386). Policy/evaluation semantics are documented in [training and tuning](../../subsystems/training-and-tuning/README.md), not inferred from remote-runner presence.

## Verification and hazards

| Claim to establish | Existing pinned-revision evidence | Still needed |
| --- | --- | --- |
| Local Ray startup and owned shutdown | Source branches and cleanup `finally` blocks above | Run fresh and preinitialized-runtime cases; inspect Ray state after success and failure |
| Trial serialization and placement | Source-declared trainable and resource bundles; real-Ray Tune tests are declared in [`test_tune_runner_ray.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_tune_runner_ray.py) | Run pinned tests and observe concurrent-trial placement, remote learners, extension loading, and cancellation |
| Multiple runners and vectorized environments | Settings and RLlib forwarding; PPO real-Ray tests declare one runner/two environments in [`test_ppo_trainer_ray.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_ppo_trainer_ray.py) | Count live actors/environment instances; check seeds, resources, and rollout behavior |
| Parallel evaluation | Remote/local source branches and unit helper tests | Run both branches with a real policy; verify synchronization and episode identity |

The default local test gate excludes Ray/integration tests; [`docs/testing/README.md`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/docs/testing/README.md) gives `python -m pytest -m ray -q` for the explicit Ray suite. Earlier focused unit tests on a **different** checkout, `ed8982e`, passed 18 tests across PPO rollout configuration, parallel evaluation, and DQN runtime helpers. They do not prove the pinned revision or live actor scheduling.

On Windows, Tune patches Ray's internal `_atomic_save` to normalize mixed separators and report an actionable `MAX_PATH` error. This private-API patch is upgrade-sensitive; recheck it against the installed Ray version before upgrading. See [`tune_runner.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L601-L665). No upstream Ray internals, external CI, or live cluster state were inspected for this page.
