---
title: Python responsibilities for pretraining and qualification
status: draft
kind: subsystem-language-design
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md]
---

# Python responsibilities for pretraining and qualification

This page maps the subsystem contract to Python modules at Theseo AnySearch commit
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`.

## Configuration boundary

`theseo_anysearch/garden/data_config.py` defines `GardenTrainingConfig`,
`GardenTuneConfig`, and `GardenConfig`. It rejects extra fields and resolves an
external data YAML during loading. It does not enforce most numeric or cross-field
constraints.

## Training execution

`theseo_anysearch/garden/trainer.py` owns loaders, optimizer construction, optional
cosine scheduling, class-weight estimation, epoch execution, validation evaluation,
best-loss tracking, resume checkpoints, callbacks, and `TrainResult`.

`theseo_anysearch/garden/dataset.py` supplies single- and multi-radius datasets and the
radius-homogeneous batch sampler. Their construction belongs to the data pipeline, but
their batch semantics affect the trainer.

## Tune execution

`theseo_anysearch/garden/tune_runner.py` parses Ray sampler declarations, applies
dotted sampled values, constructs workers, assigns resources, configures ASHA, and
selects the minimum validation-loss result.

## Command orchestration

`theseo_anysearch/cli/commands/garden.py` resolves configurations, collects data,
builds models, selects a device, calls training or tuning, presents progress, retrains
a Tune winner when requested, and hands final state to `GardenStore`.

## Adjacent ownership

`theseo_anysearch/garden/encoder.py` and `theseo_anysearch/garden/models/` belong to
encoder-model construction. `theseo_anysearch/garden/store.py` belongs to the registry
and artifact boundary. No Python module currently owns frozen-probe qualification or
certification decision generation.
