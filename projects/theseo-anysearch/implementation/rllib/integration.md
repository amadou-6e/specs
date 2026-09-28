---
title: RLlib integration boundaries investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib integration boundaries: investigation plan

This is a plan for developing current implementation guidance, not a claim that
the archived design or an unrun test describes today's behavior. Baseline to
inspect: `theseo-anysearch` `develop` at
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`; refresh and record a newer
revision if the audit starts after that commit.

## Purpose and boundary

Identify the current adapters between AnySearch configurations, environments, models, algorithms, and RLlib. The [rllib implementation index](README.md) owns contributor
guidance; subsystem contracts own observable behavior.

## Evidence to inspect

`rllib/algorithms/`, `models/`, `runner/`, environment registration and configuration translation, CLI training entry points, and relevant tests; compare archived [module proposal](../../legacy/rllib-module-spec.md).

Read the owning subsystem specifications and their validation pages before
accepting an archived statement. Inspect relevant source and tests at one exact
product revision, then execute focused tests where practical. Record failures
and untested areas rather than assuming coverage from filenames.

## Questions to resolve

Which algorithm adapters are actually wired versus only present? Where are RLModule/model, environment, policy mapping, and observation/action-space compatibility established? How does the runner select execution without owning training? Which old abstract classes or roadmap claims are obsolete?

Inventory the RLlib objects we actually construct or call: `AlgorithmConfig`,
`Algorithm`, `RLModule`, Learner, Policy, EnvRunner configuration, checkpoint
paths, and model registration. For each, distinguish upstream API from the
AnySearch wrapper, adapter, or compatibility check. Investigate actors, worker
placement, and vectorized execution in [Ray](../ray/execution.md).

For each finding, label it **current**, **obsolete**, or **unverified**, and
record the source file, test, and revision supporting that label.

## Repository-specific concepts to classify

- Typed experiment configuration, route/task sampling, policy-facing observation
  encodings, action modes, and AnySearch algorithm adapter defaults.
- Separate RLlib-provided registration and learning APIs from project-owned
  adapters and compatibility checks.

## Deliverable and acceptance

A verified dependency map and extension checklist for adding an algorithm or model, with exact source and test references. Link spaces and model semantics to [observations and models](../../subsystems/observations-and-models/README.md). Replace this plan with accepted contributor guidance only after
source and test evidence has been recorded. Keep unresolved claims explicit and
do not copy historical text into a current rule without review.

## Initial adapter inspection (2026-09-28)

At `origin/develop` `fd94554c9620096f94aaed95ffda6a1bbd4711ec`, the
`rllib/algorithms/{ppo,dqn,appo}.py` adapters translate project settings into
RLlib `AlgorithmConfig`/EnvRunner/evaluation configuration; `rllib/models/base.py`
translates project model settings into `DefaultModelConfig` and rejects a legacy
custom model on the RLModule path. `rllib/trainer/checkpointing.py` calls
`Algorithm.save()` and `restore()`. The explanation scorer uses
`RLModule.from_checkpoint()` for its module-only path. These are **current source
touch points**, not yet a complete or integration-tested compatibility map.

The available `exp/296` checkout at
`ed8982e218d39e064965661696f8b6da34bf2bb5` passed 18 focused unit tests:
`.venv/Scripts/python.exe -m pytest
tests/test_rllib/test_unit/test_ppo_rollout_config.py
tests/test_rllib/test_unit/test_parallel_evaluation.py
tests/test_rllib/test_unit/test_dqn_runtime.py -q`. This does not validate the
effective Ray actor count, resource use, or a real checkpoint round trip; those
remain **unverified** and belong to the [Ray execution audit](../ray/execution.md)
and a future integration test.
