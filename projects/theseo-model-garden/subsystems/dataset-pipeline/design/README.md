---
title: Dataset pipeline design
status: draft
kind: subsystem-design
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Dataset pipeline design

This page explains how collection, caching, splitting, and online augmentation realize the dataset contract.

## Data flow

```text
DataConfig
  -> source discriminator
     -> environment random rollouts
     -> PyVoxelSampler STL free-cell sampling
     -> registered trajectory extraction
  -> per-source .npz cache
  -> concatenate in source order
  -> seeded train/validation permutation
  -> GardenDataset / MultiRadiusDataset
  -> online augmentation at __getitem__
  -> trainer or Tune DataLoader
```

Collection is eager: accepted examples are materialized before splitting. Cache reuse is whole-source rather than streaming. This simplifies consumption but makes memory scale with the corpus and provides weak cache validation.

## State and boundaries

Pydantic models own parsing. Collectors own environment/native access and cache publication. The filesystem owns archives, metadata, and run registration. Dataset objects own float32 copies and mutable augmentation RNG state. Split functions choose membership without persisting a manifest. Trainers own downstream DataLoaders.

The native sampler, environment observations, trajectories, caches, and local paths are trusted. Per-file failures are caught and skipped, improving partial-source resilience while potentially hiding systematic corruption until collection becomes empty.

## Trade-offs

Random rollouts reuse the real observation path but are inefficient and yield an uncontrolled position distribution. STL free-cell sampling is direct but follows a distinct native path. Online augmentation saves storage but exact replay depends on access scheduling.

Independent per-radius splits preserve every resolution and homogeneous tensor shapes, but do not keep examples from the same world or trajectory in one split. This permits geometry-level leakage in representation experiments.
