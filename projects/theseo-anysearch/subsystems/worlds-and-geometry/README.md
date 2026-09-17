---
title: Worlds and geometry
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../rust/voxel-spec.md
  - ../../rust/world.md
  - ../../rust/ingest.md
---

# Worlds and geometry

## Problem and ownership

Own the representation, coordinates, occupancy semantics, mutation, persistence, and
geometry-ingestion primitives of a voxel world. It does not own episode behavior,
provider discovery, or routing-task selection.

## Consumers

Environment runtime, world providers, planners, observation construction, rendering,
and offline compilers consume this subsystem.

## Maturity and migration status

This entry indexes imported Rust and geometry specifications. Some legacy documents
describe the former fixed 1000³ world and HashMap backend; treat such details as
historical until reconciled with the later chunked and disk-backed world design.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Validation](validation.md)
