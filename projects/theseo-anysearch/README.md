# Project: Theseo Anysearch

Status: active
Owner: amadou-6e
Last reviewed: 2026-08-24

## Problem

Theseo Anysearch combines voxel environments, heuristic route planning, reinforcement
learning, imitation pretraining, experiment orchestration, explainability, and replay
UI work. The specifications provide a durable source of truth for behavior and design
decisions that span the Python, Rust, RLlib, and UI stacks.

## Outcome

Keep the project's intended behavior, contracts, architecture, experiments, and UI
design evidence reviewable independently from the implementation repository.

## Context

This directory preserves the original specification workspace imported from the
[Theseo Anysearch repository](https://github.com/amadou-6e/theseo-anysearch). Existing
organization and filenames remain intact so historical references and Draw.io assets
continue to resolve.

## Scope

- Cross-project naming and repository structure.
- Python environments, observations, models, training, tuning, and experiment design.
- RLlib policy-explanation contracts and interfaces.
- Rust voxel, world, environment, rendering, ingestion, bridge, and testing design.
- Replay and explanation UI Draw.io sources, historical design snapshots, and visual
  reference captures.
- Research notes, known bugs, deferred work, and terrain-generation design.

## Non-goals

- Product implementation, generated runtime output, model weights, and datasets.
- Rewriting or normalizing historical specifications during the initial import.
- Treating screenshots as editable UI source material.

## Risks and unknowns

- Some imported documents describe historical or prospective behavior and may not
  match the current implementation.
- Overlapping documents may use terminology from different development periods.
- Specification status and ownership metadata should be refined as documents receive
  active review.

## References

- [Naming conventions](naming.md)
- [Project structure](project-structure.md)
- [Experiment design](experiments.md)
- [3D routing environment inventory](routing-environment-inventory.md)
- [3D routing asset and integration inventory](routing-asset-inventory.md)
- [Python specifications](python/)
- [RLlib explanation specifications](rllib/explain/README.md)
- [Rust specifications](rust/)
- [UI design workspace](ui-design/)

