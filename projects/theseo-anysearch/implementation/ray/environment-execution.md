---
title: Ray environment execution
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray environment execution

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. This page distinguishes configured vectorization from measured actor and environment counts.

Training settings expose `num_env_runners` and `num_envs_per_env_runner`. Modern PPO, DQN, and Rainbow forward these through the shared PPO helper. This establishes RLlib configuration wiring, not how many actors or environment instances actually start. See [`training.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/training.py#L103-L108) and [`ppo.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L23-L39). RLlib API adaptation belongs in [environment integration](../rllib/environment-integration.md); resource reservations belong in [resources and placement](resources-and-placement.md).

Pinned [PPO real-Ray tests](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_ppo_trainer_ray.py) declare one runner and two environments; they were read, not run here. Count live actors and environment instances, inspect seeds and resource use, and compare rollout behavior before claiming a supported vectorization effect. The default local test gate excludes Ray/integration tests; [testing guidance](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/docs/testing/README.md) gives `python -m pytest -m ray -q` for an explicit Ray suite.
