---
title: Environment runtime
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related: []
---

# Environment runtime

The environment runtime turns a configured world and task into the reset and step
protocol consumed by agents. It owns actions, authoritative state transitions,
rewards, lifecycle outcomes, diagnostics, legal-action masks, and the Gymnasium and
PettingZoo adapters around the native engine.

This specification was audited against product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`. It remains draft because the inspected
tests were not executed and `SurfaceEnv` needs a deeper focused audit.

## Ownership and consumers

The runtime owns episode behavior after a world and task have been selected. World
storage belongs to [Worlds and geometry](../worlds-and-geometry/README.md), observation
schemas to [Observations and policy models](../observations-and-models/README.md), and
provider discovery to the external
[Theseo World Providers](../../../theseo-world-providers/README.md) project.

Heuristics, RLlib, Tune, trajectory collection, evaluation, and direct framework
clients consume this subsystem.

## Runtime variants

- `VoxelEnv` exposes single-agent Gymnasium behavior.
- `MultiVoxelEnv` exposes parallel multi-agent voxel navigation through PettingZoo.
- `SurfaceEnv` is a PettingZoo surface runtime with distinct observation and lifecycle
  behavior; it is not field-for-field compatible with `VoxelEnv`.

All variants delegate performance-sensitive state transitions to Rust through PyO3.
Python owns framework conformance, configuration translation, scenario selection, and
ordered lifecycle hooks.

## Limitations

- A compiled world must be paired with an explicit waypoint, curriculum, or scenario
  source. The runtime refuses to enumerate it to invent an episode.
- Single-agent and multi-agent contracts differ and must not be blended.
- Native predicate and mask failures surface as errors; they are not replaced with a
  fabricated mask.

## Reading map

- [Contract](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Design](design/README.md)
- [Validation](validation.md)
