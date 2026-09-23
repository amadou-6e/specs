---
title: Evidence domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Evidence

Owns system-independent evidence references, assertions, provenance, coverage, and transformation lineage.

## Owned concepts

Evidence source, Evidence assertion, Coverage record, Derived artifact.

## Boundaries

This domain owns system-independent financial meaning. Provider identity and presentation belong to system models, cross-system aliases to mappings, and execution steps to processes.

## Maturity

Status is **draft**. Implemented coverage varies by process; unsupported fields remain unknown rather than inferred.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
