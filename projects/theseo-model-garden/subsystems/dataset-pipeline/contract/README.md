---
title: Dataset pipeline contract
status: draft
kind: subsystem-contract
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Dataset pipeline contract

This page defines observable dataset-construction behavior in revision `49fef5f` and distinguishes it from historical proposals.

## Lifecycle

1. A validated `DataConfig` supplies discriminated sources.
2. Each source maps to an observation-cache path using the first 16 hexadecimal characters of SHA-256 over `source.model_dump_json()`.
3. Unless refresh is forced, an existing archive is loaded without recollection.
4. Position sources sample environments; training-run sources scan trajectory JSON.
5. Non-empty source arrays are concatenated in configuration order. If none remain, collection raises `RuntimeError`.
6. Dataset construction applies a seeded permutation and reserves at least one item for validation.

## Shape and value guarantees

- Examples become `numpy.float32` cubes of side `2 * box_radius + 1`.
- `GardenDataset` copies before augmentation and returns `torch.float32`; reading does not mutate the source.
- Augmentations preserve shape. Noise remains binary; paste uses voxel-wise maximum and cannot remove occupied voxels.
- Validation uses a disabled `AugmentationConfig`, independent of training settings.

## Determinism

- Split membership is deterministic for the ordered input and `split.seed`.
- Procedural boxes and STL position selection use configured NumPy seeds.
- Online augmentation owns mutable RNG state, so access order and worker scheduling affect results; augmentation is not stable per sample index.
- `RadiusBatchSampler` uses Python `random.shuffle` without a configured private generator, so shuffled order is not governed by `SplitConfig.seed`.

## Sources

Fixed geometry uses random actions in a one-agent `MultiVoxelEnv` and records `local_grid` after steps. Procedural boxes generate scenes and oversample before fill-based mixing. STL collection uses `theseo_core.PyVoxelSampler` to sample free cells. An STL failure is logged and skipped.

Training-run collection reads sorted JSON from `trajectories/` or Tune-style descendants, accepts a top-level episode or `episode` envelope, and reshapes each configured observation field. Malformed files are logged and skipped. Run names resolve through a supplied registry or `<cache.path>/runs.json`; unresolved runs are skipped.

## Split and batching invariants

- `n_val = max(1, int(sample_count * val_fraction))`; remaining items train.
- Split fractions are not constrained and may leave no training items.
- Multiple radii split independently using the same settings.
- `RadiusBatchSampler` emits complete batches only and never combines radii.

## Cache identity limitations

The key covers only serialized source configuration. It excludes STL bytes and directory contents, trajectories, requested radius, fill settings, collector code, native revision, and environment behavior. A cache can therefore be stale or shape-incompatible. Sidecar metadata is descriptive and unvalidated. There is no immutable dataset manifest or complete dataset identity.

## Unsupported and late-rejected cases

- Geometry with neither `env` nor `sampler` fails during collection; if both exist, `env` wins.
- Binary STL scale parsing is unsupported and silently falls back to `1.0`.
- Invalid ranges, impossible boxes, empty sources, and invalid split fractions lack comprehensive preflight validation.
- Morphology is silently skipped when SciPy is unavailable.
- Historical claims about two-level world caches and rotated STL worlds are not live guarantees.
