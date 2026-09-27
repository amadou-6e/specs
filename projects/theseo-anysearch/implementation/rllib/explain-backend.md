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
