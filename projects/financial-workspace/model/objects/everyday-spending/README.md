---
title: Everyday spending domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Everyday spending

Owns receipt-backed and statement-derived routine consumption classifications that do not require procurement item tracking.

## Owned concepts

Spending occurrence, Receipt line.

## Boundaries

This domain owns system-independent financial meaning. Provider identity and presentation belong to system models, cross-system aliases to mappings, and execution steps to processes.

## Maturity

Status is **draft**. Implemented coverage varies by process; unsupported fields remain unknown rather than inferred.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
