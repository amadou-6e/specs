---
title: Financial position domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Financial position

## Contained elements

```text
<model-entry>/
├── 1 README.md
├── 1 structure.md
├── 1 schema.md or schema/
├── 1 rules.md or rules/
├── 0..1 examples/
└── 0..1 presentation/
```
Owns point-in-time assets, liabilities, balances, valuations, and monthly snapshots.

## Owned concepts

Asset position, Liability position, Monthly snapshot.

## Boundaries

This domain owns system-independent financial meaning. Provider identity and presentation belong to system models, cross-system aliases to mappings, and execution steps to processes.

## Maturity

Status is **draft**. Implemented coverage varies by process; unsupported fields remain unknown rather than inferred.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
