---
title: Model Garden extension
status: draft
kind: extension
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../../../python/model-garden.md
  - ../../../../python/perception-encoder-pretraining.md
  - ../../../../python/perception-encoder-compact-package.md
---

# Model garden

## Extension relationship

- Host subsystem: [Observations and policy models](../../README.md)
- Extension point: [representation packages](../../contract/extensions.md)
- Optionality: the base observation and model contracts remain usable without a
  garden package
- Cross-subsystem consumer: training and tuning may produce or load packages but does
  not host this extension

## Problem and ownership

Optionally supply reusable pretrained representation packages, dataset and checkpoint identities,
certification metadata, cache reuse, compatibility checks, and loading into downstream
models. Research protocols and architecture-selection evidence remain experiments.

## Consumers

Observation models, imitation pretraining, RL training, Tune trials, diagnostics, and
artifact tooling consume garden packages.

## Maturity and migration status

The imported model-garden spec mixes stable package behavior with a long perception
research program. This entry retains only the intended product boundary; experiment
documents require separate migration.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Validation](validation.md)
