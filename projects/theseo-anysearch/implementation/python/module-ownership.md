---
title: Python module ownership investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Python module ownership: investigation plan

This is a plan for current contributor guidance, not an accepted package map.
Pin and record the `theseo-anysearch` revision used for the audit.

## Evidence to inspect

Inspect `theseo_anysearch/` package exports and directories, CLI entry points,
settings models, worlds and environments, experiment orchestration, imitation,
garden, and `rllib/` adapters; compare imports and tests with package READMEs.
Inspect the PyO3 boundary with the [Rust bridge plan](../rust/python-bridge.md).

## Questions to resolve

Which layer owns configuration, extension discovery, world compilation, policy
integration, training orchestration, artifacts, and user-facing CLI behavior?
Which Python modules are general package infrastructure versus RLlib-specific?
Where are dependency direction and public import stability enforced? Which
apparently similar modules have distinct responsibilities or stale documentation?

## Deliverable and acceptance

Produce a package/dependency map and placement checklist for new functionality,
with exact source and test references. Classify findings **current**, **obsolete**,
or **unverified**. Link behavior to owning subsystems rather than redefining it.
