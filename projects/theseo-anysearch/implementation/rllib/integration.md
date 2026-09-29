---
title: RLlib object integration investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib objects: investigation plan

Start with the framework objects AnySearch actually creates, subclasses, calls,
or persists. This is a source inventory, **not** a general explanation of RLlib
and not an accepted compatibility guide. Inspect the product's `origin/develop`
revision `fd94554c9620096f94aaed95ffda6a1bbd4711ec` or record a newer
exact revision before accepting a finding.

## First-pass object inventory

| RLlib object | How AnySearch touches it | Source to audit next |
| --- | --- | --- |
| `AlgorithmConfig` | Algorithm adapters translate typed project settings into RLlib training, environment, evaluation, and EnvRunner configuration. | `rllib/algorithms/{ppo,dqn,appo,sac,rainbow}.py`; compare supported algorithms and versions rather than assuming every file is active. |
| `Algorithm` | Trainer code builds and runs algorithms; checkpointing calls `save()` and `restore()`. `AnySearchDQN` subclasses RLlib DQN and changes learner-update/weight-sync behavior. | `rllib/trainer/`, `rllib/trainer/checkpointing.py`, `rllib/algorithms/dqn_runtime.py`. |
| `RLModule` and model configuration | Project model settings become RLlib `DefaultModelConfig`; custom legacy `TorchModelV2` models are rejected on that path. The explanation scorer can restore only an `RLModule` from a learner checkpoint subtree. | `rllib/models/base.py`, algorithm adapters, `rllib/explain/scoring.py`. |
| Learner and LearnerGroup | The DQN runtime subclass suppresses a TD-error metric in one configuration and wraps `learner_group.update`; its synchronization assumptions are framework-version sensitive. | `rllib/algorithms/dqn_runtime.py` and focused DQN tests. |
| Policy and policy mapping | Multi-agent PPO constructs `PolicySpec` mappings; the explanation scorer retains an Algorithm/Policy-ID path alongside module-only scoring. | `rllib/algorithms/ppo.py`, `rllib/explain/scoring.py`. |
| EnvRunner configuration | Adapters set rollout/evaluation runner counts and per-runner environment counts; a custom evaluator configures the evaluation pool. | `rllib/algorithms/`, `rllib/trainer/evaluation/parallel.py`. The resulting actors and vectorization belong to [Ray environment execution](../ray/environment-execution.md); placement and resources belong to [Ray resources](../ray/resources-and-placement.md). |

These touch points were found in source at the pinned revision. They do not prove
that each path is exercised in production or stable across RLlib upgrades. In
particular, the scorer's module-only `RLModule.from_checkpoint()` path and
full-Algorithm restore path need real checkpoint tests before either is described
as generally supported. The [policy-explainability subsystem](../../subsystems/policy-explainability/README.md)
owns what a score or explanation means; this page only tracks RLlib integration.

## Investigation sequence

1. For each row, trace construction, methods called, project-owned wrappers,
   version-sensitive assumptions, and callers. Classify it **current**,
   **obsolete**, or **unverified** with source and test references.
2. Run focused unit tests, then one real train-save-restore-infer cycle for each
   supported algorithm and model stack. Include negative checkpoint and
   incompatible-space cases. Do not substitute mocks for checkpoint evidence.
3. Trace the EnvRunner configuration into the [Ray environment execution audit](../ray/environment-execution.md)
   and the project settings into their owning subsystem contracts. Keep runtime
   scheduling and behavioral semantics out of this object inventory.
4. Replace this draft with a small, version-pinned contributor guide: which
   adapters to edit, compatibility checks to preserve, and tests to run when
   an RLlib object changes.

## Evidence already gathered

On the available product checkout `ed8982e218d39e064965661696f8b6da34bf2bb5`
(`exp/296`), 18 focused unit tests passed:
`.venv/Scripts/python.exe -m pytest
tests/test_rllib/test_unit/test_ppo_rollout_config.py
tests/test_rllib/test_unit/test_parallel_evaluation.py
tests/test_rllib/test_unit/test_dqn_runtime.py -q`. The suite checks adapter and
helper behavior but **not** a real checkpoint round trip, worker count, or
measured resource use. Those remain unverified.
