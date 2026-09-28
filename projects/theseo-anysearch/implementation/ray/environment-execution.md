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

## Configured parallelism versus execution

Training defaults to `num_env_runners=0` (inline sampling) and `num_envs_per_env_runner=1`; evaluation separately defaults to zero dedicated runners and one environment per runner. `evaluation.parallel_to_training` requires at least one dedicated evaluation runner. These are settings and validation rules, not observed actor counts. See [training settings](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/training.py#L103-L111) and [evaluation settings](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/evaluation.py#L35-L58).

| Adapter | Training EnvRunner configuration at this revision | Evidentiary limit |
| --- | --- | --- |
| PPO, DQN, Rainbow (new API stack) | Shared helper forwards runner count, environments per runner, GPUs per runner, in-flight request cap, and `FlattenObservations`. | Proves config construction, not vectorized execution. |
| APPO (legacy stack) | Sets those four parallelism/resource fields directly; does not use the connector-v2 helper. | Proves config assignment only. |
| SAC and multi-agent PPO (legacy stack) | Set runner count but do not forward the training environments-per-runner setting in the inspected adapter path. | The setting's intended vectorization effect is not established for these adapters. |

See [shared helper and PPO use](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L25-L40), [DQN use](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py#L176-L176), [Rainbow use](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/rainbow.py#L116-L116), [APPO fields](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/appo.py#L93-L103), [SAC runner count](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/sac.py#L111-L111), and [multi-agent PPO runner count](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L456-L456). No explicit `vectorization_mode` assignment was found in the tracked Python examined by the researcher; this does not establish which default a given Ray version uses. RLlib configuration API details belong in [environment integration](../rllib/environment-integration.md), and Tune placement requests in [resources and placement](resources-and-placement.md).

## What a runner must be able to load

`VoxelEnv.register_with_ray` registers a factory receiving an environment configuration. Environment construction can load geometry, scenario, and native extensions from file paths; trainer configuration resolves local trial artifact paths to absolute paths before handing them to RLlib. Those paths must also be readable where an environment is constructed. Path resolution alone does not distribute files to remote nodes, and remote visibility was not tested here. See [registration and geometry loading](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/environments/gymnasium/voxel_env.py#L145-L205), [factory/native loading](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/environments/gymnasium/voxel_env.py#L235-L285), and [trainer path setup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/trainer.py#L159-L183).

`VoxelEnv.reset` uses an explicit seed when supplied, otherwise its configured base seed plus an instance-local reset count. The inspected path does not show a worker or vector-index offset. This raises a possible repeated-sequence risk across instances, **not** evidence that identical trajectories occurred. See [reset seed selection](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/environments/gymnasium/voxel_env.py#L527-L533) and [generated-geometry seed](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/environments/gymnasium/voxel_env.py#L664-L688).

## Evidence and verification gap

Pinned [PPO real-Ray tests](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_ppo_trainer_ray.py#L27-L45) configure one training runner with two environments and [check evaluation results](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_ppo_trainer_ray.py#L132-L143), but do not assert distinct actor or environment-instance identities. Other inspected coverage uses zero runners, tests requested placement-group setup, or checks helper forwarding; none is a live count of vectorized environments. These tests were **read, not run** for this page. Count live actors and environment instances, inspect per-instance seeds and loaded paths, and compare rollout behavior before claiming supported vectorization or remote-filesystem behavior. Upstream Ray behavior, CI history, and live-cluster state were not inspected. [Testing guidance](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/docs/testing/README.md) describes an explicit Ray suite.
