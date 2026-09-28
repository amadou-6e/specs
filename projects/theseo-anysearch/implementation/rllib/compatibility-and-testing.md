---
title: RLlib compatibility and testing
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib compatibility and testing

This page separates dependency declarations, source-wired adapters, declared
tests, and demonstrated runtime support. Its baseline is AnySearch commit
[`fd94554c`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec),
inspected on 2026-09-28. The baseline source and tests were read, but its tests
were **not run** for this audit. Upstream RLlib internals, external CI and run
manifests were not inspected. Nothing below certifies an algorithm/version
combination for production use.

## Version evidence is not a support promise

The [dependency declaration][pyproject] requires Python `>=3.10` and
`ray[default,rllib]>=2.9`, without an exact Ray version or upper bound. Torch
`>=2` is optional. No tracked Python lockfile was found in the pinned source
tree during this audit. An installed Ray 2.58.0 was observed in a virtual
environment on a **different** checkout (`ed8982e`); it is neither the declared
minimum nor a proven supported version. Record the exact Python, Ray/RLlib,
Torch, and native-extension versions with each run before comparing behavior.

| Term | What it means here |
| --- | --- |
| Declared version | A packaging constraint; it does not prove compatibility throughout the allowed range. |
| Installed version | The dependencies present in one environment; it does not say which tests passed. |
| Tested version | Exact versions paired with a recorded test command, source revision, and result. None was established at this pinned baseline in this audit. |
| Supported version | A reviewed compatibility claim backed by representative real training, evaluation, and restore tests. No such range is established here. |

## API stacks and combination evidence

The adapters do not share one RLlib stack. Single-agent PPO, DQN, and Rainbow
enable the RLModule/Learner and EnvRunner/Connector V2 stack; SAC, APPO, and
multi-agent PPO explicitly disable it. The modern model builder rejects a
custom legacy `TorchModelV2`, while the legacy builder registers one.
[PPO adapter][ppo] · [DQN adapter][dqn] · [Rainbow adapter][rainbow] ·
[SAC adapter][sac] · [APPO adapter][appo] · [Model builder][model-builder]

The matrix describes **evidence tiers**, not a blanket supported-combinations
matrix. “Declared test” means test source was inspected, not executed at the
pinned revision. Registry membership is deliberately separate from a build
path and a passing real run. [Registry][registry] · [Coverage tests][coverage]

| Algorithm / configuration | Registry and source path | Pinned-baseline test evidence inspected | Runtime support finding |
| --- | --- | --- | --- |
| PPO, DQN, Rainbow, SAC, multi-agent PPO, default configurations | Registered; adapter has an RLlib configuration/build path. | Five real-Ray/Tune coverage cases declare two trials and one iteration each, with `num_env_runners=0`; read, not run. | **Unverified** at this baseline. A test declaration is not a passing result or broad configuration coverage. |
| APPO | Registered with an adapter/build path on the legacy stack. | No comparable case found in the inspected algorithm-coverage file; other tests were not exhaustively searched. | **Unverified**; neither “unsupported” nor “trainable” follows from this search. |
| DDPG, TD3 | Registered, but adapters explicitly raise `NotImplementedError`. | Registry/config checks cannot overcome the stub. | **Not usable through these built-in adapters** at this revision. |
| Modern PPO/DQN/Rainbow plus default FC | Model configuration path exists. | Coverage cases above exercise only their specified settings, if run. | Source-wired, not runtime-certified. |
| Modern PPO plus legacy custom CNN | Modern model builder rejects `custom_model`. | A [real-Ray integration test][cnn-test] nevertheless requests PPO/CNN training; read, not run. | **Contradictory test intent and source path**; do not list as supported without resolving the test and builder discrepancy. |
| Legacy SAC/APPO plus registered CNN | Legacy registration path exists. | No verified live CNN result in this audit. | **Unverified**. |
| Multi-agent PPO with heterogeneous agents sharing one `PolicySpec` | Policy mappings are constructed from configured agents. | Coverage declaration does not establish heterogeneous-space safety. | **Unverified**. |

The [DDPG][ddpg] and [TD3][td3] stubs make the distinction between
“registered” and “trainable” especially important. Two source/documentation
conflicts also need correction: the [algorithm README][algorithm-readme]
calls APPO unregistered, contrary to the [registry][registry], and the
[coverage-test heading][coverage] labels PPO legacy even though the
[single-agent PPO adapter][ppo] enables the new stack. Neither heading is
runtime evidence.

## Upgrade-sensitive surfaces

- The mixed API stacks mean a change to a connector, model, or evaluation
  adapter must be tested on **both** paths; sharing an algorithm registry does
  not imply shared preprocessing or masking. Modern mask enforcement and
  training/evaluation observation parity are still unverified here.
  [Adapters][ppo] · [Model builder][model-builder] ·
  [environment integration](environment-integration.md)
- `AnySearchDQN` subclasses RLlib DQN/Learner and substitutes
  `learner_group.update` and `env_runner_group.sync_weights`, using
  `TD_ERROR_KEY` and `ALL_MODULES`. These RLlib-internal touch points need
  targeted revalidation on every upgrade; source inspection does not show
  how each upstream version behaves. [DQN runtime][dqn-runtime]
- The explanation scorer expects the literal
  `learner_group/learner/rl_module/<policy_id>/metadata.json` subtree before
  calling `RLModule.from_checkpoint`. That layout is version-sensitive and was
  not checked against a real checkpoint in this audit. [Scorer][scorer] ·
  [checkpoint integration](checkpoints.md)
- The evaluation connector and callback configuration need real-policy parity
  checks, particularly across old/new stacks. Whether configured EnvRunners
  become particular actors, placements, or vectorized executions belongs to
  [Ray execution](../ray/execution.md), not this page.
  [environment integration](environment-integration.md)

## Evidence required before a compatibility claim

At the pinned revision, [algorithm coverage][coverage] **declares** real-Ray
tests for five adapters. Registry unit tests check names and configuration,
not trainability. The [PPO resume test][ppo-resume] trains, saves, constructs a
fresh trainer, and checks restored **iteration**, not policy-output equality;
the [DQN integration test][dqn-integration] trains and saves but does not
restore. These tests were read, not run in this research. Passing focused
tests reported on a different checkout cannot establish the pinned baseline.

For each claimed algorithm, model, observation mode, and version combination:

1. Capture exact source and dependency versions; run a real build, at least
   one training iteration, and evaluation, recording commands and artifacts.
2. Test explicit negative and edge cases: APPO, PPO with legacy CNN, modern
   action masks, multi-agent heterogeneous spaces, and DQN synchronization
   with multiple actual EnvRunners.
3. Save and restore a full `Algorithm` and the module-only explanation path;
   compare representative action scores or outputs before and after restore,
   not only iteration counters.
4. Repeat after dependency upgrades and record failures by layer: project
   configuration, RLlib API construction, actor execution, observation
   preprocessing, checkpoint restoration, or evaluation.

Keep training outcomes and acceptance criteria in the
[training-and-tuning subsystem](../../subsystems/training-and-tuning/README.md),
observation meaning in [observations and models](../../subsystems/observations-and-models/README.md),
and worker/resource behavior in [Ray](../ray/README.md). This page records
RLlib adaptation and the evidence required to claim compatibility.

[pyproject]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/pyproject.toml
[registry]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/registry.py
[ppo]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py
[dqn]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn.py
[rainbow]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/rainbow.py
[sac]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/sac.py
[appo]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/appo.py
[ddpg]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ddpg.py
[td3]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/td3.py
[model-builder]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/models/base.py
[dqn-runtime]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/dqn_runtime.py
[scorer]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/explain/scoring.py
[coverage]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_algorithm_coverage.py
[ppo-resume]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_ppo_trainer_ray.py
[dqn-integration]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_dqn_trainer_ray.py
[cnn-test]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_cnn_models_ray.py
[algorithm-readme]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/README.md
