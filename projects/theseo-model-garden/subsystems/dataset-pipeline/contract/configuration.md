---
title: Dataset pipeline configuration
status: draft
kind: subsystem-configuration
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Dataset pipeline configuration

This page describes the validated YAML fields and defaults affecting collection, reuse, splitting, and augmentation.

## Data settings

`DataConfig` forbids unknown fields and requires `sources`.

| Field | Default | Effect |
|---|---:|---|
| `cache.path` | `runtime/garden/cache` | Archive and `runs.json` root |
| `cache.force_refresh` | `false` | Ignore an existing source cache |
| `split.val_fraction` | `0.1` | Validation share, rounded down with minimum one |
| `split.seed` | `42` | Input permutation seed |
| `min_fill_pct` | `0.0` | Non-empty classification threshold |
| `empty_sample_ratio` | `0.05` | Requested empty share in position sampling |

Sources are `position_sample` or `training_run`. Fixed geometry supports `stl_path`, `geometry_boxes`, `scale=40.0`, and `grid_size=32`. `stl_list` defaults to 60,000 samples and seed 42. `random_boxes` defaults to 50 scenes, 1–5 boxes, grid size 32, 50,000 samples, and seed 42.

## Augmentation settings

All transforms are disabled by default. Settings are `rotate90`, `flip`, `cutout`, `geometry_paste`, `noise_prob`, `translation_jitter`, and `morph_prob`. Cutout defaults to two regions of size 1–2. Paste defaults to probability 0.3 and size 2 when configured.

Augmentation does not affect the cache key because it runs online. Radius and fill settings do affect collected output but are also absent from the key; use force refresh or a different cache path when changing them.

## Loading

`load_data_config` accepts a root mapping or `data:` wrapper. `load_garden_config` accepts a root mapping or `model_garden:` wrapper and resolves a string-valued data reference relative to the model YAML. Embedded source paths are not generally rebased by these loaders.
