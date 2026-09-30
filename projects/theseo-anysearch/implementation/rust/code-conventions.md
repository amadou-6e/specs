---
title: Rust code conventions investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Rust code conventions: investigation plan

This page proposes an audit, not a style policy. Pin the product source revision
before accepting any convention.

## Evidence to inspect

Sample public and private modules in `theseo_anysearch/core/src/`, the
`extension_sdk` and macro crates, their tests, crate manifests, formatter and lint
configuration, CI, and contributor instructions. Compare existing `///` item docs,
`//!` module docs, comments, examples, and error text. Check commands in a clean
environment rather than assuming a tool is configured or enforced.
The imported [Rust naming examples](../../legacy/root-naming.md) are candidate
evidence only, including old bridge paths; verify each against the pinned
current crate tree before making it contributor policy.

## Questions to resolve

- What is the intended structure of crates, modules, imports, re-exports, and tests?
- Which public APIs need rustdoc, examples, safety/ABI notes, or invariants? Where
  are ordinary comments preferable, and what documentation style is already used?
- What conventions govern naming, `Result` and error types, panics, `unsafe`,
  ownership, lifetimes, serialization, logging, and feature flags?
- Which `cargo fmt`, Clippy, rustdoc, test, and benchmark checks run in CI? Which
  patterns are consistent practice, and which are isolated or historical?

## Deliverable and acceptance

Produce concise contributor rules and an exception list, each backed by source,
test/configuration, and pinned revision. Mark unsupported claims **unverified**.
Separate repository policy from general Rust idiom and observable subsystem behavior.
