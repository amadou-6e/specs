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

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. These are requested resources, not observed allocations; pinned-revision live-Ray tests were not run.

For each Tune trial, the code declares a `PlacementGroupFactory` with a driver CPU/GPU bundle, one training EnvRunner CPU/GPU bundle per runner, and one CPU bundle per evaluation runner, using `SPREAD`. See [`tune_runner.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1335-L1400). [Trial boundaries](trials-and-process-boundaries.md) document wrapper order and actor reuse.

Training settings expose runner count, environments per runner, per-runner GPU, and remote learners. Modern PPO, DQN, and Rainbow forward runner/vectorization fields through a shared PPO helper; PPO fixes `num_learners=0`, while DQN/Rainbow can configure remote learners. The Tune placement-group construction does not visibly add learner-specific bundles for the latter case. Treat a remote-learner scheduling mismatch as a **hazard to test**, not a demonstrated failure. See [`training.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/training.py#L103-L108), [`ppo.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L23-L39), and the [Tune resource declaration](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1335-L1400).

The pinned [real-Ray Tune tests](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_tune_runner_ray.py) declare placement-group checks; they were read, not run here. Verify actual concurrent-trial placement and remote Learner reservations. RLlib configuration calls belong in [environment integration](../rllib/environment-integration.md); the resulting environment instances belong in [environment execution](environment-execution.md).
