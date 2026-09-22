---
title: 3D routing environment and asset sources
status: draft
kind: research
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-world-providers]
supersedes: null
related:
  - ../routing-environment-inventory.md
  - ../routing-asset-inventory.md
---

# 3D routing environment and asset sources

## Question and relevance

Which externally available systems provide usable 3D routing tasks, world geometry,
observations, or references, and what additional work is required before Theseo may
use them for training or evaluation?

## Status

This topic is an initial structural migration of source characterizations from the
existing routing environment and asset inventories. Those documents remain the
historical synthesis until their findings are fully migrated and reviewed.

## Evaluation criteria

Sources are characterized separately by geometry, task, observation, and reference
assets; actual inspection versus publication claims; task readiness; metric and
coordinate fidelity; rights; leakage risk; and missing adapters or validators.

## Synthesized findings

- [F-001 — Geometry availability does not imply task readiness](findings/F-001-geometry-is-not-a-task.md)

## Existing synthesis

- [3D routing environment inventory](../routing-environment-inventory.md)
- [3D routing asset and integration inventory](../routing-asset-inventory.md)

## Recommendation and open questions

Use the source registry to select bounded adapter or benchmark experiments. Do not
treat inclusion as permission to train, redistribute, or claim upstream benchmark
results. Rights, task validity, metric transforms, and independent collision checks
remain source-specific gates.

## Sources

See the [source registry](sources/README.md).
