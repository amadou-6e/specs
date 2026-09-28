---
title: Ray resources and placement
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray resources and placement

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. This page describes **requested** resources in source code, not observed actor placement or throughput. Upstream Ray internals and a live distributed run at this revision were not inspected.

## Inputs and their different effects

[`TrainingConfig`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/training.py#L102-L108) types the overall GPU request (`num_gpus`), remote Learner count and per-Learner CPU/GPU requests, training EnvRunner count, environments per runner, and per-EnvRunner GPU request. Evaluation has its [own runner count](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/evaluation.py); [`TuneConfig.max_concurrent` defaults to four](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/models.py#L187-L233). These are configuration inputs, not measurements of actors or devices actually allocated. Environment-instance behavior is covered in [environment execution](environment-execution.md); RLlib configuration calls are covered in [environment integration](../rllib/environment-integration.md).

For experiment Tune, [`_tune_trial_num_gpus`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L678-L707) returns zero for a CPU-only request; otherwise it preserves an explicit `training.num_gpus`, or chooses `1 / max_concurrent` when more than one GPU trial is allowed, or one GPU for a single trial. The resulting fraction is also [injected into trial training settings](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1076-L1122). This arithmetic does not check whether the cluster has enough GPUs for all requested actors.

## Experiment Tune placement request

The experiment Tune runner wraps the base trainable with a `PlacementGroupFactory` using `SPREAD`, **before** wrapping it with `with_parameters`. Its bundle list is:

| Bundle | CPU request | GPU request |
| --- | ---: | ---: |
| Trial/driver | 1 | Computed trial fraction, if positive |
| Each training EnvRunner | 1 | `training.num_gpus_per_env_runner`, if positive |
| Each evaluation EnvRunner | 1 | None explicitly requested |

The code passes `max_concurrent_trials` into Tune separately. These statements are declarations made by the project; whether RLlib's actors occupy the intended bundle indices is a runtime question. [Placement construction and wrapper order](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1335-L1393), [Tune concurrency](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1480-L1493).

DQN and Rainbow [forward remote-Learner count and per-Learner resources](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py#L164-L172) to RLlib; PPO explicitly [sets `num_learners=0`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L305-L311). The experiment placement-group construction above contains **no Learner-specific bundle**. Thus remote-Learner placement and GPU sufficiency are open validation questions; this source difference is not evidence that a Learner fails to schedule or necessarily runs outside the group.

## Other entry points are not the same resource policy

Standalone algorithm builders call [`_ensure_ray_runtime`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L78-L110), whose local `ray.init(num_cpus=...)` budget is one CPU plus the count passed by its caller. PPO passes training plus evaluation runner counts; [DQN also adds requested remote-Learner CPUs](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py#L101-L109). Initialization capacity is distinct from a Tune placement-group reservation, and an already initialized Ray runtime is not resized by this calculation.

The [legacy Tune CLI](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/cli/commands/tune.py) has a separate conditional `PACK` placement request that includes a Learner bundle and rollout-worker CPU bundles, but not the experiment runner's evaluation or per-runner GPU bundles. The [Garden Tune runner](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/garden/tune_runner.py#L159-L167) instead requests one CPU and a CUDA-dependent GPU fraction per trial, with no explicit EnvRunner or Learner bundles. Do not transfer placement conclusions from one entry point to another.

## Validation boundary

The pinned [real-Ray Tune test](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_tune_runner_ray.py) declares a one-EnvRunner bundle-index regression, conditional on `theseo_core`; most algorithm coverage uses zero runners. These tests were **read, not run** at the pinned revision. A separate checkout's unit suites for Tune resources and schedulers reported **112 passed**, but its Tune runner differs from this baseline; those results validate neither this exact implementation nor live placement. No inspected test establishes concurrent GPU trials with remote Learners and evaluation runners together. Before claiming that combination supported, run it at a pinned dependency set and inspect actor placement, allocated resources, startup/failure behavior, and trial throughput.
