---
title: Native extension implementation investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Native extensions: investigation plan

This is an investigation plan, not an accepted compatibility or authoring rule.
Inspect a pinned `theseo-anysearch` revision and record it with the findings.

## Purpose and boundary

Explain how this repository implements Rust extensions, from an experiment's
`cdylib` through SDK macros, compilation, capability discovery, loading, and
invocation. Subsystem contracts own the supported extension points and observable
behavior; this page will own contributor-facing source placement and change steps.

## Evidence to inspect

Inspect `theseo_anysearch/extension_sdk/`, its `macros/` crate,
`theseo_anysearch/core/src/voxel/{common,predicates,outcomes,rewards,metrics,scenarios}/`,
`theseo_anysearch/experiments/native_extensions.py`, CLI compilation code,
`docs/extensions/`, showcase extensions, and relevant unit/integration tests.
Compare each documented ABI or precedence claim with code and tests at the same
revision. Link the owning subsystem's `contract/extensions.md` where present.

## Questions to resolve

- Which extension families exist, and which are native Rust versus Python hooks?
  Which crate or package owns each registration, loader, context, and invocation?
- What do SDK macros generate? Where are ABI version, exported symbol names,
  capability bits, C-compatible layouts, and error conversion defined and tested?
- How do compilation, source hashes, cache reuse, run-local artifact copying,
  worker loading, platform compatibility, and trust boundaries work?
- How are ordering, precedence, deterministic inputs, and failures validated?
  Which changes require a new ABI version or migration?
- Which current docs/examples describe actual behavior, and which are stale?

## Deliverable and acceptance

Produce a source map and change checklist for adding or modifying one extension
family, with a small verified example and focused test commands. Classify each
finding **current**, **obsolete**, or **unverified** with source, test, and revision.
Keep behavioral guarantees linked to subsystem contracts; do not restate them here.
