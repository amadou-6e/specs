---
title: Training and tuning orchestration
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../experiments.md
  - ../../python/rllib.md
  - ../../python/tune.md
---

# Training and tuning orchestration

## Problem and ownership

Own experiment loading, RLlib algorithm construction, staged training, evaluation,
Tune search, resource allocation, checkpointing, and pretraining handoff. It does not
own environment dynamics, model internals, or scientific experiment conclusions.

## Consumers

Experiment authors, local operators, CI smoke tests, model-garden checkpoints, and
tracking integrations consume this subsystem.

## Maturity and migration status

Imported documents mix configuration, implementation, runbooks, and historical
experiment guidance. This entry establishes their intended behavioral owner; exact
schemas still require reconciliation.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Guides](guides/README.md)
- [Validation](validation.md)
