---
title: Trajectory and replay
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related: []
---

# Trajectory and replay

This subsystem records selected episodes, persists them as durable replay artifacts,
resolves those artifacts from runs, and presents them in the native voxel viewer. It
owns trajectory schemas, atomic storage, compatibility loading, replay selection,
frame state, regional rendering, camera behavior, and diagnostic captures.

The specification was audited at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`; tests were inspected but not run. UI
geometry and interaction states remain owned by the corresponding UI-design entry.

Collectors record initial state and per-step action, reward, positions, outcomes, and
overlay deltas. The writer selects the best buffered episode and emits scheduled and
best-so-far snapshots. Readers resolve legacy or compressed files, and the separately
built native viewer loads and scrubs the selected trajectory.

Small worlds use sidecar occupancy. Compiled worlds use a content-addressed world
reference plus sparse overlay mutations and never enumerate the full base.

## Reading map

- [Contract](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Design](design/README.md)
- [Guide](guides/README.md)
- [Validation](validation.md)
- [Storage migration](migrations.md)
