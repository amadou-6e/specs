---
title: Native build and verification workflow investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Native build and verification workflow: investigation plan

This is a plan for developing current implementation guidance, not a claim that
the archived design or an unrun test describes today's behavior. Baseline to
inspect: `theseo-anysearch` `develop` at
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`; refresh and record a newer
revision if the audit starts after that commit.

## Purpose and boundary

Give contributors a verified procedure for building, diagnosing, releasing, and benchmarking the native core. The [Rust testing inventory](testing.md) owns test tiers and current CI coverage. The [rust implementation index](README.md) owns contributor
guidance; subsystem contracts own observable behavior.

## Evidence to inspect

Current `theseo_anysearch/core/Cargo.toml`, Python build configuration, CI workflows, `theseo_anysearch/core/src/verification/`, and bench binaries; compare the [Rust testing inventory](testing.md) and archived [testing plan](../../legacy/rust-testing.md).

Read the owning subsystem specifications and their validation pages before
accepting an archived statement. Inspect relevant source and tests at one exact
product revision, then execute focused tests where practical. Record failures
and untested areas rather than assuming coverage from filenames.

## Questions to resolve

What build and diagnostic commands work on supported platforms? Which benches cover compiled worlds, regional replay, LOD, and cache behavior? What artifacts are generated, and which must not be committed? Which old performance targets are no longer valid? Test coverage and boundary parity are tracked in [testing.md](testing.md).

For each finding, label it **current**, **obsolete**, or **unverified**, and
record the source file, test, and revision supporting that label.

## Repository-specific concepts to classify

- The PyO3 wheel/native core, external capability ABI, compiled-world tools,
  and separately built native replayer and performance benchmarks.
- Record which verification is repository-specific and which is standard Cargo
  or Python tooling; link canonical behavior tests to subsystem validation.

## Deliverable and acceptance

Copyable build, diagnostic, release, and benchmark commands with prerequisites, expected artifacts, failure diagnostics, and an evidence table distinguishing checks actually run from checks merely described. Keep behavioral acceptance in each subsystem's `validation.md`. Replace this plan with accepted contributor guidance only after
source and test evidence has been recorded. Keep unresolved claims explicit and
do not copy historical text into a current rule without review.
