---
title: Rust to Python bridge investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Rust to Python bridge: investigation plan

This is a plan for developing current implementation guidance, not a claim that
the archived design or an unrun test describes today's behavior. Baseline to
inspect: `theseo-anysearch` `develop` at
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`; refresh and record a newer
revision if the audit starts after that commit.

## Purpose and boundary

Document how contributors change the native/PyO3 boundary without changing policy-facing behavior accidentally. The [rust implementation index](README.md) owns contributor
guidance; subsystem contracts own observable behavior.

## Evidence to inspect

`core/src/bridge/dto.rs`, `core/src/bridge/python/module.rs`, `errors.rs`, `environments/`, `geometry.rs`, `rendering.rs`, and `sampling.rs`; Python adapters and bridge parity tests; compare archived [bridge](../../legacy/rust-bridge.md).

Read the owning subsystem specifications and their validation pages before
accepting an archived statement. Inspect relevant source and tests at one exact
product revision, then execute focused tests where practical. Record failures
and untested areas rather than assuming coverage from filenames.

## Questions to resolve

Which Rust types and errors are translated at the boundary? How are initialization, reset, step, observation, geometry, and rendering exposed? Which signatures are public, and which archived DTOs or function names are obsolete? How are ABI/version and Python-space parity checked?

For each finding, label it **current**, **obsolete**, or **unverified**, and
record the source file, test, and revision supporting that label.

## Repository-specific concepts to classify

- AnySearch-specific environment result/observation DTOs, typed settings,
  compiled-world handles, native extension errors, and action-mask transfer.
- Separate PyO3 mechanics supplied by the library from translation and parity
  decisions owned by this repository.

## Deliverable and acceptance

A reviewed binding map, error/compatibility rules, change checklist, and focused parity-test commands. Public behavior remains in [environment runtime](../../subsystems/environment-runtime/contract/README.md) and other owning contracts. Replace this plan with accepted contributor guidance only after
source and test evidence has been recorded. Keep unresolved claims explicit and
do not copy historical text into a current rule without review.
