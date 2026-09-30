---
title: RLlib models and policies
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib models and policies

This page describes AnySearch's model and policy integration at product revision
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`. It records what source
configures or rejects, **not** which combinations have completed a live training
run. Observation meaning belongs to the [observations-and-models subsystem](../../subsystems/observations-and-models/README.md);
training outcomes belong to [training and tuning](../../subsystems/training-and-tuning/README.md).

## Two model paths

`ModelConfig` carries `hidden_sizes`, `activation`, `custom_model`, and
`custom_model_config`. The modern builder translates the first two fields to
RLlib `DefaultModelConfig` and raises `ValueError` whenever `custom_model` is
set. The legacy builder instead passes FC settings as a model dictionary or
registers the requested custom model and forwards its custom config.
`BaseRLModule` is an AnySearch abstract encoder interface, **not** a concrete
RLlib `RLModule`; the pinned source search found no subclass. [Model settings][settings]
· [Model helpers][model-base]

The legacy registrations are `voxel_box_2d_cnn`, `voxel_box_3d_cnn`,
`voxel_hierarchical_box_3d_cnn`, and `voxel_box_3d_cnn_pretrained`.
Their shared `BaseVoxelTorchModel` extends RLlib `TorchModelV2`; it keeps
`action_mask` out of auxiliary features, checks its width against policy logits,
and masks disallowed logits. Registration and unit-level model behavior do not
establish that an algorithm can build and train with a given model.
[CNN registration][cnn] · [Model base][model-base]

| Adapter path | Default FC model | Custom `TorchModelV2` | Evidence limit |
| --- | --- | --- | --- |
| Single-agent PPO, DQN, Rainbow | Modern RLModule/Learner and Connector V2 configured. | Rejected by the modern model builder. | Live training and inference unverified here. |
| SAC, APPO | Legacy model dictionary and API stack configured. | Legacy registration path configured. | Live build/training, including APPO, unverified here. |
| Multi-agent voxel PPO | Legacy API stack configured. | No custom-model compatibility established by this audit. | Live policy-space and training behavior unverified here. |

These are **source-wired paths, not a support matrix**. DDPG and TD3 are
explicit algorithm stubs and are excluded; see [algorithms](algorithms.md).
The adapter-specific calls are in [PPO][ppo], [DQN][dqn], [Rainbow][rainbow],
[SAC][sac], and [APPO][appo]. An [integration test][cnn-ray-test] attempts PPO
with a custom CNN, but the pinned modern PPO builder rejects `custom_model`.
That test declaration is conflicting historical intent, not evidence of a
working PPO/CNN combination.

## Policy identities and observation adaptation

Multi-agent PPO creates one RLlib `PolicySpec` for each configured policy ID,
using the observation and action spaces of the first agent assigned that ID.
Its mapping function returns the configured policy ID for an agent, or the
agent ID when no explicit policy is set. Without an agent configuration, it
creates `shared_policy` from `agent_0`'s spaces. Unlike the class docstring,
configured agents do **not** necessarily share one policy. Sharing an ID across
heterogeneous spaces has not been validated. [Multi-agent PPO][ppo] ·
[Multi-agent environment][multi-env]

Single-agent modern PPO installs RLlib `FlattenObservations` before module
inference. The [evaluation adapter][evaluation] separately flattens observations
for module inference with Gymnasium utilities, while its legacy path uses an
RLlib `Policy` and `ObsPreprocessorConnector`. Source inspection does not prove
that training and evaluation preprocessing are equivalent for every observation
mode. [PPO adapter][ppo]

The voxel environment can supply an `action_mask` when configured, and the
legacy custom model consumes it. No explicit mask-aware RLModule or connector
was found in the inspected modern adapter paths; modern action-mask enforcement
is **unverified**. Flattening could include the mask as a feature rather than
apply it to logits; that is an inference requiring a runtime test. The
inspected multi-agent observation schema does not expose a mask.
[Voxel environment][voxel-env] · [Model base][model-base] ·
[Multi-agent environment][multi-env]

## Change and verification boundary

When changing a model or policy mapping, check the selected adapter's API
stack first. Keep `ModelConfig` translation, observation spaces, connector
behavior, model registration, and evaluation adaptation aligned. Do not claim
new support from a registration entry or a mocked build. The next checks are a
minimal real-Ray build/train/infer cycle for each claimed combination, explicit
PPO-plus-CNN rejection, heterogeneous policy-space validation, modern masking,
checkpoint/evaluation preprocessing parity, and the pinned RLlib dependency
version. [Model helpers][model-base] · [Adapters][ppo] · [Evaluation adapter][evaluation]

The pinned source and test declarations were inspected, but upstream RLlib
internals and real Ray integration were not. On a **different** product checkout
(`ed8982e`), 78 focused tests passed across CNN models, PPO rollout config, and
parallel evaluation. That result does not validate the pinned baseline or any
live training combination; the parallel-evaluation test differs between the
two revisions. [CNN unit tests][cnn-tests] · [PPO tests][ppo-tests] ·
[Evaluation tests][evaluation-tests]

[settings]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/algorithm.py
[model-base]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/models/base.py
[cnn]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/models/cnn.py
[ppo]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py
[dqn]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py
[rainbow]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/rainbow.py
[sac]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/sac.py
[appo]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/appo.py
[voxel-env]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/environments/gymnasium/voxel_env.py
[multi-env]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/environments/pettingzoo/multi_voxel_env.py
[evaluation]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py
[cnn-ray-test]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_cnn_models_ray.py
[cnn-tests]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_cnn_models.py
[ppo-tests]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_ppo_rollout_config.py
[evaluation-tests]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_parallel_evaluation.py
