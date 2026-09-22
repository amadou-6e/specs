---
title: Dataset pipeline validation
status: draft
kind: subsystem-validation
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Dataset pipeline validation

This page maps guarantees to automated checks present in revision `49fef5f`. It does not describe unrun tests as passing.

## Present checks

| Guarantee | Evidence | What it proves |
|---|---|---|
| Config defaults and unknown-key rejection | `tests/test_garden/test_unit/test_garden_data_config.py` | Tested model and loader behavior |
| STL path discovery and exclusion | `TestStlListSamplerConfig` in that file | Explicit paths, directory scans, and index exclusions |
| Float32 tensors and input immutability | `tests/test_garden/test_unit/test_garden_dataset.py::TestGardenDataset` | Dataset wrapper semantics |
| Seeded split determinism and sizing | `TestMakeTrainValDatasets` | Repeatable ordered splits |
| Radius-homogeneous batches | `TestRadiusBatchSampler` | Grouping and DataLoader collation |
| Augmentation shape and voxel semantics | `tests/test_garden/test_unit/test_garden_augment.py` | Rotation, flip, cutout, paste, noise, jitter, and pair properties |

## Checks run in this pass

No implementation tests were run because only specification files changed. The entry was checked manually against source and test files. Parent integration should run the specs validator.

## Missing coverage

- No focused tests exercise the collectors, aggregate collection, cache reuse, stale-cache detection, or sidecar integrity.
- No end-to-end test covers every source type through its real entry point.
- Malformed trajectories, missing run registrations, all-STL failure, invalid ratios, empty arrays, and zero-training splits lack complete tests.
- Multi-worker augmentation reproducibility is unverified.
- No split test prevents world, geometry, route, or trajectory leakage.
- No complete content-addressed dataset manifest exists to validate.

The imported [architecture record](../../architecture/model-garden-monolith.md) describes intended workflows, and the [perception-encoder experiment](../../experiments/perception-encoder-r0/README.md) records dataset-dependent studies. Neither substitutes for tests of the live contract.
