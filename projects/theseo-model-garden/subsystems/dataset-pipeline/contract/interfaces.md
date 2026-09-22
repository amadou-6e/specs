---
title: Dataset pipeline interfaces
status: draft
kind: subsystem-interface
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Dataset pipeline interfaces

This page records the Python and serialized interfaces used to collect, split, and consume Model Garden voxel examples.

## Python API

`theseo_anysearch.garden.collect.collect_dataset(data_cfg, box_radius=2, run_registry=None, progress_cb=None) -> numpy.ndarray` is the aggregate collector. It returns concatenated grids or raises when no source contributes.

`GardenDataset` is a PyTorch dataset returning `(N, N, N)` float32 tensors. `make_train_val_datasets` creates training and validation datasets. `MultiRadiusDataset`, `RadiusBatchSampler`, and `make_multi_radius_train_val` provide shape-homogeneous multi-radius consumption.

Collector classes are importable, but no stable package-level API or semantic version is declared.

## Cache format

```text
<cache.path>/obs/<16-character-source-hash>.npz
<cache.path>/obs/<16-character-source-hash>_meta.json
```

The archive has an `observations` key. The sidecar contains the source model and, for training runs, the resolved run directory. Loading checks file existence and reads `observations`; it does not verify the sidecar.

## Trajectory input

JSON may be `{ "steps": [...] }` or `{ "episode": { "steps": [...] } }`. Each selected step field must flatten to exactly `(2 * box_radius + 1)^3` values. The default field is `local_grid`.

## CLI consumers

`theseo_anysearch/cli/commands/garden.py` invokes this subsystem for extraction, training, tuning, and inspection. CLI presentation is outside this contract.
