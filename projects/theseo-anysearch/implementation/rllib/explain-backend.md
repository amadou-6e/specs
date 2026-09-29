---
title: Policy explainability backend implementation investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Policy explainability backend implementation: investigation plan

This is a plan for developing current implementation guidance, not a claim that
the archived design or an unrun test describes today's behavior. Baseline to
inspect: `theseo-anysearch` `develop` at
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`; refresh and record a newer
revision if the audit starts after that commit.

## Purpose and boundary

Map the implemented policy-explanation pipeline so contributors can change it without reviving obsolete methodology. The [rllib implementation index](README.md) owns contributor
guidance; subsystem contracts own observable behavior.

## Evidence to inspect

`rllib/explain/` modules (`requests`, `scenarios`, `backend`, `traces`, `scoring`, `features`, `explainers`, `reports`, `service`, `native_bridge`, and `ui/`), CLI wiring, and focused tests; compare archived [backend](../../legacy/rllib-explain-backend.md), [CLI](../../legacy/rllib-explain-cli.md), and [attribution](../../legacy/rllib-policy-attribution.md).

Read the owning subsystem specifications and their validation pages before
accepting an archived statement. Inspect relevant source and tests at one exact
product revision, then execute focused tests where practical. Record failures
and untested areas rather than assuming coverage from filenames.

## Questions to resolve

How is an RLModule restored and scored for DQN/PPO? Where are state provenance, trace divergence, feature grouping, backgrounds, and native UI messages checked? Which former SHAP-first design claims were never implemented or are now superseded? What is the current test gap for live environment traces?

For each finding, label it **current**, **obsolete**, or **unverified**, and
record the source file, test, and revision supporting that label.

## Repository-specific concepts to classify

- AnySearch feature groups, chosen-versus-safe action scores, trace provenance
  and divergence checks, report identities, and the persistent native UI bridge.
- Separate generic attribution algorithms from the project's accepted grouped
  occlusion behavior and explicitly reject obsolete SHAP-first assumptions.

## Deliverable and acceptance

A current module/responsibility table, extension and failure-path checklist, and focused test commands. Method meaning, accepted inputs, and report validity stay in [policy explainability](../../subsystems/policy-explainability/README.md). Replace this plan with accepted contributor guidance only after
source and test evidence has been recorded. Keep unresolved claims explicit and
do not copy historical text into a current rule without review.

## Initial audit checkpoint (2026-09-28)

This is a bounded source/test inspection, **not** acceptance of the full plan.
The plan's `origin/develop` baseline is
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`. The available product checkout
was `ed8982e218d39e064965661696f8b6da34bf2bb5` on `exp/296`, with unrelated
uncommitted files; `service.py` and its replay/background test differ from
`origin/develop`. The focused tests below therefore validate the checkout's
explain implementation, not an isolated `develop` checkout.

| Finding | Classification and evidence |
| --- | --- |
| `service.py` restores DQN/PPO scorers from run/checkpoint, resolves trajectory or scenario sources, builds the schema/background, and invokes `PolicyExplanationBackend`. | **Current in inspected checkout**: `service.py`, `scoring.py`; focused tests described below. Live checkpoint restoration remains **unverified** by this pass. |
| `backend.py` selects steps, scores actions, computes grouped chosen-versus-best-safe margins, and writes reports through `reports.py`; `features.py` owns grouping. | **Current in both inspected revisions**: those source modules and `test_backend_smoke.py`, `test_feature_schema.py`. This is a code-responsibility map, not a second behavior contract. |
| `native_bridge.py` serves persistent JSON-line requests; `ui/session.py` holds the restored service. | **Current in both inspected revisions**: source modules and `test_native_bridge.py`; an actual Rust viewer process was **not** exercised. |
| The archived backend's `artifacts.py` and `GroupedShapExplainer` package plan is not the current module layout. | **Obsolete as implementation guidance**: compare `legacy/rllib-explain-backend.md` with present `service.py`, `explainers.py`, and `reports.py`. No SHAP implementation was found in this package. |
| `PolicyEvaluationTraceCollector._cursor()` reads `observation["cursor_pos"]`, while the live voxel wrapper reads cursor state from `env._rust_env.cursor_pos()`; its focused test supplies a synthetic `cursor_pos` observation. | **Current mismatch / live compatibility unverified**: `traces.py`, `environments/gymnasium/voxel_env.py`, and `test_trace_collector.py`. The owning subsystem's `validation.md` already records this gap. Do not use the fixture test as proof of live-environment compatibility. |

Verification in the available checkout:
`.venv/Scripts/python.exe -m pytest tests/test_rllib/test_unit/test_explain -q`
returned **44 passed**. The system Python lacked `pytest`. This does not establish
end-to-end checkpoint restoration, live VoxelEnv trace collection, or Rust viewer
integration. Next, reproduce against a clean pinned revision, add/run a live trace
test, and then resolve the mismatch in the owning implementation before promoting
this page from draft to contributor guidance.
