---
title: RLlib algorithm adapters
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib algorithm adapters

This contributor guide describes the adapter code at product revision
`fd94554c9620096f94aaed95ffda6a1bbd4711ec` (`origin/develop` when
inspected on 2026-09-28). It records **source-backed implementation paths**, not
a certification that every selectable algorithm trains successfully. Training
lifecycle and evaluation behavior belong to the
[training-and-tuning subsystem](../../subsystems/training-and-tuning/design/README.md);
actor placement and vectorized execution belong to [Ray](../ray/README.md).

## Selection is not usability

The adapter registry accepts `appo`, `ddpg`, `dqn`, `multi_agent_voxel_ppo`,
`ppo`, `rainbow`, `sac`, and `td3`. The separate typed-settings lookup also
recognizes `heuristic`, but the RLlib trainer registry does not. Both lists
must be checked when changing an
algorithm name. [Registry][registry] · [Typed configuration lookup][models]

| Algorithm | What the pinned source establishes | Verification limit |
| --- | --- | --- |
| PPO, DQN, Rainbow, SAC, multi-agent voxel PPO | Adapter construction paths configure RLlib and call `build_algo()`. | The pinned baseline's real-Ray/Tune coverage tests were **read, not run** for this audit; code presence is not proof of a successful training run. |
| APPO | A typed config and registered adapter exist, with a path that calls `build_algo()`. | No APPO case was found in the inspected baseline algorithm-coverage tests; trainability is **unverified**. |
| DDPG, TD3 | Names and typed configs exist, but their adapters explicitly raise `NotImplementedError` because the present environments do not expose the required continuous `Box` action space. | Explicit stubs, not usable built-in trainers. |

This classification comes from the [adapter registry][registry], [algorithm
configurations][models], [individual adapter modules][adapters], and [coverage
tests][coverage]. The [algorithm README][algorithm-readme] says APPO is not
registered; that conflicts with the pinned registry and APPO adapter. Treat the
README statement as stale, **not** as evidence that APPO trains.

## Settings-to-Algorithm path

`settings/loading.py` reads `training.algorithm`, chooses the project-owned
Pydantic class through `get_algorithm_config_class()`, and places the resulting
typed object in `Settings.algorithm_config`. `Trainer.from_settings()` then
resolves a project adapter with `get_trainer_class()`; the registry imports that
class lazily. In `_build_algorithm()`, an adapter delegates shared construction
to `build_algorithm_from_settings()`: project environment, model, and
hyperparameters become RLlib `AlgorithmConfig` calls; the environment is
registered, evaluation is configured, `build_algo()` is called, and an
evaluator is attached. Iteration, checkpointing, and reporting are trainer
responsibilities rather than adapter responsibilities. [Settings loader][loading]
· [Settings root][settings-root] · [Trainer][trainer] · [Shared adapter
construction][adapters]

The adapters do **not** share one RLlib API stack. Single-agent PPO, DQN, and
Rainbow opt into RLModule/Learner and EnvRunner/Connector V2. SAC, APPO, and
multi-agent voxel PPO retain the legacy stack in the pinned source. The
multi-agent PPO adapter constructs `PolicySpec` mappings; SAC uses legacy model
and replay configuration. Check the selected adapter's stack and spaces before
copying configuration from another algorithm. [Adapter modules][adapters]

## DQN-specific runtime extension

`DQNTrainer` binds `AnySearchDQN` and `AnySearchDQNTorchLearner`. After the
RLlib learner computes loss, the custom learner removes `TD_ERROR_KEY` from
its metrics when `report_td_errors` is false. The DQN adapter sets that flag
false for uniform replay and true for prioritized replay. The source comment
describes avoiding an unused per-sample TD-error transfer; this audit did not
measure that cost. [DQN adapter][dqn] · [Runtime extension][dqn-runtime]

`AnySearchDQN.setup()` wraps `learner_group.update()`. Every configured
`weight_sync_interval` updates, the wrapper derives module IDs from the first
result (excluding `ALL_MODULES`) and requests an inference-only sync to
EnvRunners. It also replaces the runner group's ordinary `sync_weights()` with
a no-op. This is a framework-internal method substitution: it assumes a
nonempty update result with the expected shape and that suppressing other sync
calls is appropriate. These are **upgrade risks**, not observed failures.
[Runtime extension][dqn-runtime]

Rainbow uses the standard RLlib `DQNConfig`, **not** these custom DQN algorithm
or learner classes. Shared replay and resource settings do not imply shared
runtime synchronization behavior. [Rainbow adapter][rainbow] · [DQN
adapter][dqn]

## Add or upgrade an adapter

For an additional built-in algorithm, introduce its typed project config and
lookup key in `algorithms/models.py`; implement a `Trainer` adapter whose
`_build_algorithm()` selects the appropriate RLlib config and API stack;
register and export the adapter explicitly. Verify that the settings name,
adapter key, action/observation spaces, and stack agree. These are steps
**inferred from the existing construction path**, not a guarantee that the
new algorithm is supported. [Typed configurations][models] · [Registry][registry]
· [Adapter modules][adapters]

Before claiming support or upgrading RLlib, check the upstream signatures the
adapter calls, then test typed-config dispatch, algorithm construction, at
least one real training iteration, and evaluation in the pinned dependency
environment. For DQN, cover uniform and prioritized replay plus the
weight-sync path with real EnvRunners; mocks alone cannot validate the runtime
effect. The inspected baseline includes [real-Ray/Tune coverage cases][coverage]
and [DQN runtime unit tests][dqn-tests], but neither suite was run at the
pinned baseline in this audit. On a **different current checkout**, five DQN
runtime tests and four registry/config tests passed; they are not baseline
trainability evidence.

## Evidence boundary

This document's claims are pinned to product source, not to upstream RLlib
internals. Upstream implementation, all configurations, baseline real-Ray
tests, APPO training, legacy SAC/multi-agent PPO runs, and real multi-runner DQN
synchronization remain unverified here. Recheck these before changing `status`
from `draft` or making an unconditional support claim.

[registry]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/registry.py
[models]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/models.py
[adapters]: https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms
[algorithm-readme]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/README.md
[coverage]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_algorithm_coverage.py
[loading]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/loading.py
[settings-root]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/root.py
[trainer]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/trainer.py
[dqn]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py
[dqn-runtime]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn_runtime.py
[rainbow]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/rainbow.py
[dqn-tests]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_dqn_runtime.py
