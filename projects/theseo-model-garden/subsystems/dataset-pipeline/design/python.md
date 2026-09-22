---
title: Dataset pipeline Python responsibilities
status: draft
kind: subsystem-language-map
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
---

# Dataset pipeline Python responsibilities

This map identifies concrete modules implementing the pipeline in Theseo AnySearch revision `49fef5f`.

## Configuration

`theseo_anysearch/garden/data_config.py` defines source, sampler, cache, split, and augmentation models and YAML loaders. Its encoder and trainer settings belong to other subsystem concerns.

## Collection

`theseo_anysearch/garden/collect.py` hashes source configuration, loads and publishes caches, builds environment settings, samples environments and STL free cells, extracts trajectories, and concatenates arrays. `theseo_anysearch/environments/pettingzoo/multi_voxel_env.py` is an external observation boundary owned by Theseo AnySearch.

## Dataset consumption

`theseo_anysearch/garden/dataset.py` implements PyTorch wrappers, seeded splits, multi-radius index mapping, and homogeneous batching. `theseo_anysearch/garden/augment.py` implements rotations, flips, cutout, paste, noise, circular translation, and optional SciPy morphology.

## Callers

`theseo_anysearch/cli/commands/garden.py`, `theseo_anysearch/garden/trainer.py`, and `theseo_anysearch/garden/tune_runner.py` invoke this subsystem but own command presentation, optimization, and orchestration respectively.
