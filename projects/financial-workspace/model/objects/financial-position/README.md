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

<!-- BEGIN GENERATED: object-domain-summary -->
> Defines assets, liabilities, balances, and valuations observed at a specific cutoff.

## Domain boundary

**Includes:**

- Asset positions
- Liability positions
- Account balances at a cutoff
- Valuation basis, currency, and certainty
- Scoped monthly snapshots

**Excludes:**

- Period cash flow
- Individual posted transactions
- Unqualified expected amounts
- Raw balance statements and valuation documents
<!-- END GENERATED: object-domain-summary -->

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
financial-position/
├── 1 README.md
├── 1 structure.md
├── 1 schema.md or schema/
├── 1 rules.md or rules/
├── 0..1 examples/
└── 0..1 presentation/
```
<!-- END GENERATED: contained-elements -->

## Maturity

Status is **draft**. Implemented coverage varies by process; unsupported fields remain unknown rather than inferred.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
