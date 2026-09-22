---
title: Using the dataset pipeline
status: draft
kind: subsystem-guide
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Using the dataset pipeline

This guide shows the minimal workflow for defining, extracting, and reusing Model Garden voxel examples. It assumes Theseo AnySearch and its native extension are installed. The result is cached `.npz` arrays consumed by Garden training or tuning.

## Define data

```yaml
data:
  sources:
    - type: position_sample
      geometry:
        sampler:
          type: random_boxes
          seed: 42
          num_geometries: 50
          total_samples: 50000
  cache:
    path: runtime/garden/cache
    force_refresh: false
  split:
    val_fraction: 0.1
    seed: 42
```

Run `anysearch garden extract <data-yaml>`. Successful extraction writes under `cache.path/obs/`; later runs reuse archives unless refresh is forced.

Force refresh whenever source contents, trajectories, radius, fill thresholds, native code, or collection behavior changes because these inputs are not all in the cache key.

## Recorded trajectories

Register a run through the Garden CLI, then configure:

```yaml
data:
  sources:
    - type: training_run
      run: my-run-reference
      obs_key: local_grid
```

Trajectory values must match the selected radius. Malformed files are skipped; inspect logs and final counts.

## Interpretation cautions

The default split is observation-level, not world-, route-, or trajectory-level. Do not claim held-out geometry generalization from it. For frozen experiments retain exact caches, configuration, code revision, and an external hash; the pipeline does not publish a sufficient immutable manifest.
