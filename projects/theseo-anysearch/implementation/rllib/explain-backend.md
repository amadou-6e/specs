---
title: RLlib checkpoint and policy-scoring adapter investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib checkpoint and policy-scoring adapter: investigation plan

This page concerns only the RLlib-dependent adapter used by the
[policy-explainability subsystem](../../subsystems/policy-explainability/README.md).
The subsystem owns the explanation pipeline, methods, inputs, reports, validity,
and Python/Rust responsibility map. This is draft contributor guidance, not a
second explanation contract.

Baseline to inspect: `theseo-anysearch` `origin/develop` at
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`; record a newer exact revision
if the audit proceeds against one.

## RLlib objects and touch points to inspect

| RLlib object or concept | AnySearch touch point and question |
| --- | --- |
| `Algorithm` and legacy `Policy` | `rllib/explain/scoring.py`: when do scorer paths restore a full algorithm, call `compute_single_action`, or use a policy ID? Which paths remain active? |
| `RLModule` | `DQNPolicyScorer.from_module_checkpoint`, `PPOPolicyScorer`, `rllib/models/base.py`: how is a module restored, fed structured observations, and asked for inference outputs? |
| Learner checkpoint layout | `scoring.py` checkpoint path resolution and trainer checkpoint writer: which path and metadata assumptions are project-specific, version-sensitive, and tested? |
| DQN/PPO outputs | `scoring.py` and `test_policy_scorer.py`: where are Q-values, logits, selected actions, and optional critic values extracted and checked? |
| Observation/action spaces | run-config reconstruction in `scoring.py`, `service.py`, and tests: how are policy-facing shapes and action count matched to the checkpoint? |

The source contains a module-only `RLModule.from_checkpoint` path that avoids
building a Ray `Algorithm` runtime, plus a full-algorithm restore path for
older callers. Treat both as code observations, not evidence that both are
supported for every checkpoint. Worker/actor/vectorization execution belongs
in [Ray](../ray/execution.md); generic attribution, trace provenance, and the
native UI bridge belong to the [subsystem design](../../subsystems/policy-explainability/design/README.md).

## Investigation and acceptance

Inspect `rllib/explain/scoring.py`, `rllib/models/`, `rllib/algorithms/`, trainer
checkpoint writing, CLI explain entry points, and focused scorer/restoration
tests at one pinned revision. Determine supported RLlib versions, modern versus
legacy paths, checkpoint selection, error handling, and policy/space compatibility.
Run a real saved DQN and PPO checkpoint through the scorer before claiming
restoration works; mock scorer tests establish only adapter logic.

Classify each finding **current**, **obsolete**, or **unverified** with source,
test, and revision. The resulting contributor guide should be a small
checkpoint/scorer change checklist, not a rewrite of the subsystem contract.

## Initial inspection boundary (2026-09-28)

The available product checkout was `ed8982e218d39e064965661696f8b6da34bf2bb5`
on `exp/296`, not a clean `develop` checkout. The focused explain suite returned
**44 passed** with `.venv/Scripts/python.exe -m pytest
tests/test_rllib/test_unit/test_explain -q`; no real checkpoint was restored in
this pass. The `service.py` and replay/background test differ from the pinned
`develop` baseline. This result remains **unverified for live restoration**.

The generic trace collector's `cursor_pos` mismatch and the cross-cutting module
map are recorded by the [subsystem design](../../subsystems/policy-explainability/design/python.md)
and [validation](../../subsystems/policy-explainability/validation.md), not owned
by this RLlib adapter page.
