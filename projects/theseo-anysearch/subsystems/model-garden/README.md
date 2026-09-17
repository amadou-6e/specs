---
title: Model garden
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../python/model-garden.md
  - ../../python/perception-encoder-pretraining.md
  - ../../python/perception-encoder-compact-package.md
---

# Model garden

## Problem and ownership

Own reusable pretrained representation packages, dataset and checkpoint identities,
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
