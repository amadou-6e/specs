---
title: Python extension implementation investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Python extensions: investigation plan

This page plans an audit; it does not establish a new extension contract. Pin
the product revision and distinguish Python hooks from the native Rust SDK.

## Evidence to inspect

Inspect `theseo_anysearch/experiments/custom_*.py`, environment lifecycle and
scenario registration, provider discovery, worker serialization, CLI/config
resolution, `docs/extensions/`, examples, and tests. Compare native handoff with
the [Rust extension investigation](../rust/extensions.md).

## Questions to resolve

Which Python extension families exist, how are they named, registered, resolved,
serialized to workers, and invoked? What is the relationship to Rust hooks and
their precedence or coexistence? Which failures are caught before execution?
How do state, determinism, versioning, and reproducibility affect contributors?
Which hooks are public contracts versus internal customization points?

## Deliverable and acceptance

Produce an extension-family map and verified change checklist with focused tests
and examples. Label each finding **current**, **obsolete**, or **unverified** and
cite source, tests, and revision. Defer observable behavior to subsystem contracts.
