---
title: Dataset pipeline
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Dataset pipeline

The dataset pipeline turns geometry or recorded trajectories into local binary voxel grids used by Model Garden pretraining. It owns source configuration, collection, observation-cache reuse, deterministic train/validation splitting, radius-homogeneous batching, and online augmentation. Model training and artifact publication belong to other subsystems; world acquisition and routing tasks belong to peer projects.

This specification describes Theseo AnySearch revision `49fef5f`, which currently hosts the Model Garden implementation under `theseo_anysearch/garden/`.

## Consumers

- `anysearch garden extract`, `train`, and `tune`;
- the Model Garden trainer and Tune runner; and
- perception-encoder experiments requiring frozen voxel corpora and splits.

## Supported scope and maturity

The live implementation samples fixed geometry, STL lists, procedural boxes, and registered trajectory files. It caches one compressed observation array per serialized source, concatenates successful sources, creates seeded train/validation splits, and groups multiple observation radii without mixing tensor shapes within a batch.

The subsystem remains `draft`: cache identity is configuration-derived rather than content-derived, collection has no durable dataset manifest, and several malformed or empty input cases are detected only during execution.

## Primary guarantees

- Successful collection returns float32 arrays shaped `(samples, N, N, N)`, where `N = 2 * box_radius + 1`.
- A cache hit is reused unless `force_refresh` is true.
- A fixed split seed gives the same permutation for the same ordered input.
- Validation samples receive no online augmentation.
- Multi-radius batches contain one radius only.

## Reading map

- [Contract](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Internal design](design/README.md)
- [Python responsibilities](design/python.md)
- [Usage](guides/README.md)
- [Validation](validation.md)
