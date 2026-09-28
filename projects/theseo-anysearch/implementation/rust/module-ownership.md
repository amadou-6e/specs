---
title: Rust module ownership investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Rust module ownership: investigation plan

The imported [repository map](../../legacy/root-project-structure.md) is
historical. Verify its crate and module claims against a pinned current source
revision before incorporating any of them here.

This is a plan for developing current implementation guidance, not a claim that
the archived design or an unrun test describes today's behavior. Baseline to
inspect: `theseo-anysearch` `develop` at
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`; refresh and record a newer
revision if the audit starts after that commit.

## Purpose and boundary

Determine where native behavior and supporting code belongs before contributors extend it. The [rust implementation index](README.md) owns contributor
guidance; subsystem contracts own observable behavior.

## Evidence to inspect

`core/src/lib.rs`, `core/src/voxel/README.md`, `core/src/environments/README.md`, `core/src/surface/`, `core/src/bridge/`, `core/src/replay/`, `core/src/rendering/`, and `core/src/verification/`; compare the archived [world](../../legacy/rust-world.md), [environment](../../legacy/rust-environment.md), and [renderer](../../legacy/rust-rendering.md) documents.

Read the owning subsystem specifications and their validation pages before
accepting an archived statement. Inspect relevant source and tests at one exact
product revision, then execute focused tests where practical. Record failures
and untested areas rather than assuming coverage from filenames.

## Questions to resolve

Which modules own world storage versus episode mutation? Which layer owns action transitions, PyO3 conversion, and viewer-only state? What public exports and internal paths are intended to remain stable? Which imported module paths no longer exist?

Map the `core` crate, `extension_sdk` crate and its procedural macros, native
executables, and test targets separately. Identify dependency direction and the
boundary between built-in behavior and dynamically loaded experiment extensions;
develop the latter in the [extension investigation](extensions.md).

For each finding, label it **current**, **obsolete**, or **unverified**, and
record the source file, test, and revision supporting that label.

## Repository-specific concepts to classify

- Compiled world packs versus per-episode overlays, voxel action pipelines, native
  extension capabilities, and viewer-only replay state.
- For each concept, identify the owning source module and link its observable
  behavior to the subsystem contract; document here only contributor placement.

## Deliverable and acceptance

A current module map with dependency direction, one owner per responsibility, extension-placement examples, and source/test references. Link observable guarantees to the owning subsystem rather than redefining them. Replace this plan with accepted contributor guidance only after
source and test evidence has been recorded. Keep unresolved claims explicit and
do not copy historical text into a current rule without review.
