---
title: Experiment tracking
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../python/mlflow-tracking.md
---

# Experiment tracking

## Problem and ownership

Own structured recording of run parameters, metrics, identities, artifacts, status,
and links needed to find and compare training or tuning executions. It does not own
metric definitions or scientific conclusions.

## Consumers

Training, tuning, evaluation, local monitoring, result summaries, and experiment
replication consume tracking records.

## Maturity and migration status

The imported MLflow specification contains detailed schema and implementation claims
that require reconciliation with current code and the new experiment-iteration model.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Guides](guides/README.md)
- [Validation](validation.md)
