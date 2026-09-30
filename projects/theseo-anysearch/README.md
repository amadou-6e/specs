# Project: Theseo Anysearch

Status: active
Owner: amadou-6e
Last reviewed: 2026-08-24

Before adding or reorganizing Theseo specifications, read
[SPECS.md](SPECS.md). It defines the project's documentation taxonomy,
ownership rules, lifecycle, and live template examples.

## Problem

Theseo Anysearch combines voxel environments, heuristic route planning, reinforcement
learning, imitation pretraining, experiment orchestration, explainability, and replay
UI work. The specifications provide a durable source of truth for behavior and design
decisions that span the Python, Rust, RLlib, and UI stacks.

## Outcome

Keep the project's intended behavior, contracts, architecture, experiments, and UI
design evidence reviewable independently from the implementation repository.

## Context

This directory originated as a specification workspace imported from the
[Theseo Anysearch repository](https://github.com/amadou-6e/theseo-anysearch).
Historical source text is preserved under [legacy/](legacy/README.md) when its
former root path or authority no longer fits the current taxonomy. Git history
retains the original locations.

## Contained elements

```text
projects/theseo-anysearch/
├── 1 README.md
├── 1 spec.json
├── 1 SPECS.md
├── 0..1 glossary.md
├── 1 architecture/
├── 1 subsystems/
├── 1 experiments/
├── 1 research/
├── 1 decisions/
├── 1 implementation/
├── 1 ui-design/
├── 1 bugs/
├── 1 legacy/
└── 0..* transitional imported documents and directories
```

The named categories are the closed project taxonomy. Each category README defines
the entry type and cardinalities below that boundary. Transitional imported material
remains available for historical links, but new specifications must use the category
that owns their purpose. [SPECS.md](SPECS.md) is authoritative for structure and
placement rules; `spec.json` owns machine-readable project metadata.

## Scope

- Cross-project naming and repository structure.
- Python environments, observations, models, training, tuning, and experiment design.
- RLlib policy-explanation contracts and interfaces.
- Rust voxel, world, environment, rendering, ingestion, bridge, and testing design.
- Replay and explanation UI Draw.io sources, historical design snapshots, and visual
  reference captures.
- Research notes, known bugs, and deferred work owned by Anysearch.

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

- [Current architecture](architecture/README.md)
- [Python and Rust contributor guidance](implementation/README.md)
- [Experiment records](experiments/README.md)
- [Durable bug records](bugs/README.md)
- [Imported root documents and their replacements](legacy/README.md)
- [Theseo Model Garden](../theseo-model-garden/README.md)
- [Theseo World Providers](../theseo-world-providers/README.md)
- [Python implementation rules](implementation/python/README.md)
- [Policy explainability contract](subsystems/policy-explainability/README.md)
- [Rust implementation guidance](implementation/rust/README.md)
- [Imported Rust and RLlib historical documents](legacy/README.md)
- [UI design workspace](ui-design/)

