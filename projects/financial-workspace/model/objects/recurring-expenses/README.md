---
title: Recurring expenses domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Recurring expenses

<!-- BEGIN GENERATED: object-domain-summary -->
> Defines continuing services, effective contract terms, service periods, and expected recurring obligations.

## Domain boundary

**Includes:**

- Recurring service identity
- Contract terms and effective intervals
- Billing cadence and service periods
- Expected service-month obligations
- Cancellation and lifecycle state

**Excludes:**

- Posted settlement transactions
- One-off purchases
- Raw contracts, mandates, and invoices
- Provider-specific billing exports
<!-- END GENERATED: object-domain-summary -->

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
recurring-expenses/
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
