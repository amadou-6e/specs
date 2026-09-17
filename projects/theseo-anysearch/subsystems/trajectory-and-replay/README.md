---
title: Trajectory and replay
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../python/trajectory-recording.md
  - ../../python/tune-replay.md
  - ../../rust/rendering.md
---

# Trajectory and replay

## Problem and ownership

Own trajectory serialization, replay loading, frame state, regional large-world
visualization, rendering, camera behavior, and deterministic visual diagnostics. It
does not own environment transition correctness or experiment evaluation semantics.

## Consumers

Training/evaluation callbacks, the native replayer, explanation tooling, and UI design
work consume this subsystem.

## Maturity and migration status

Imported specs predate several large-world and minimap changes. The Draw.io workspace
remains authoritative for reviewed UI geometry and interactions.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Guides](guides/README.md)
- [Validation](validation.md)
