---
title: Matters domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Matters

Owns stateful returns, claims, reimbursements, disputes, deposits, and recoverable balances that may produce future movements.

## Owned concepts

Matter, Claim, Matter event.

## Boundaries

This domain owns system-independent financial meaning. Provider identity and presentation belong to system models, cross-system aliases to mappings, and execution steps to processes.

## Maturity

Status is **draft**. Implemented coverage varies by process; unsupported fields remain unknown rather than inferred.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
