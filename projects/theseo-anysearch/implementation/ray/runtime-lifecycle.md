---
title: Ray runtime lifecycle
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray runtime lifecycle

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. Ray integration tests at this revision were read, not run. This page concerns runtime ownership, not RLlib configuration or training guarantees.

Standalone algorithm builders share `_ensure_ray_runtime`: an already initialized runtime is reused; otherwise the builder initializes local Ray with at least `num_env_runners + 1` CPUs, dashboard disabled, and an output-derived temporary directory. DQN and Rainbow also account for configured remote learner CPUs. This is an initialization budget, not proof that requested actors can be scheduled. See [`ppo.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L78-L115) and [DQN](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py).

`TuneRunner` builds options for either an external Ray address or local temporary storage. It records whether Ray was initialized before entry and conditionally calls `ray.shutdown()` in `finally`; callers must not assume it owns a preexisting runtime. Tune trainables separately stop their constructed `Algorithm` in `finally`. See [`tune_runner.py` options](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L970-L995) and [execution/cleanup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1320-L1580). Source inspection does not establish shutdown after process crashes or forced cancellation.

To verify ownership, run fresh and preinitialized-runtime cases, then inspect Ray state after success and failure. See [trial boundaries](trials-and-process-boundaries.md) for trial-local cleanup and [resources](resources-and-placement.md) for reservations.
