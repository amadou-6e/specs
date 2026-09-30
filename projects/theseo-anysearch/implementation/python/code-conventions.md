---
title: Python code conventions investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Python code conventions: investigation plan

This is an audit plan, not a style policy. Pin the product source revision before
promoting observations to contributor rules.

## Evidence to inspect

Sample public and internal modules across `theseo_anysearch/`, package and test
configuration, CI, contributor docs, type annotations, docstrings, module comments,
CLI help, settings models, and tests. Check actual formatter, linter, type-checker,
and documentation commands; do not infer enforcement from a tool's installation.
Treat the imported [naming examples](../../legacy/root-naming.md) as candidate
evidence only; verify package, class, method, flag, and JSON-key rules against
the pinned current tree before adopting or rejecting each rule.

## Questions to resolve

- What are the conventions for package exports, imports, naming, typing, dataclasses
  or Pydantic models, exceptions, logging, paths, and optional dependencies?
- Which public APIs need docstrings and examples? What docstring form and level of
  detail are used consistently, and how are parameter/return/error semantics kept
  synchronized with type annotations and tests?
- How are async/process boundaries, Ray worker imports, deterministic seeds, and
  Python/Rust conversion documented? Which patterns are repository-specific?
- Which formatter, lint, type, docs, and test checks actually run in CI? Does the
  existing [testing page](testing.md) match the current suite?

## Deliverable and acceptance

Produce concise, source-backed contributor conventions and an explicit exception
list. Classify claims **current**, **obsolete**, or **unverified**, citing source,
test/configuration, and revision. Do not turn isolated examples into policy.
