---
title: Observations and policy models
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../python/voxel-observations.md
  - ../../python/cnn-models.md
  - ../../python/architectures.md
---

# Observations and policy models

## Problem and ownership

Own observation schemas and preprocessing, spatial encoder inputs, policy/value model
interfaces, action-logit production, and compatibility between observations and model
architectures. It does not own environment transitions or training protocols.

## Consumers

RLlib policies, imitation pretraining, model-garden encoders, explainability, and
evaluation tooling consume these contracts.

## Maturity and migration status

Imported observation and model specs span several design generations. Perception
encoder studies are primarily experiments and evidence; only promoted interfaces
belong in this subsystem contract.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Validation](validation.md)
