---
title: Procurement domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Procurement

<!-- BEGIN GENERATED: object-domain-summary -->
> Defines purchases and their commercial lifecycle from order through item, return, and merchant refund.

## Domain boundary

**Includes:**

- Orders and merchant-scoped references
- Purchase items and supported allocations
- Commercial order, dispatch, delivery, and return dates
- Returns and merchant refunds
- Procurement categories

**Excludes:**

- Posted payment movements
- Recurring contract terms
- Raw invoices, receipts, and order emails
- Provider-specific publication layouts
<!-- END GENERATED: object-domain-summary -->

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
procurement/
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
