---
title: Travel domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Travel

<!-- BEGIN GENERATED: object-domain-summary -->
> Defines journeys, bookings, route segments, and stays using verified travel dates and locations.

## Domain boundary

**Includes:**

- Journeys and purpose classification
- Travel segments and transport mode
- Origin, destination, departure, and arrival
- Bookings and provider references
- Travel stays and stay intervals

**Excludes:**

- Payment and refund transactions
- Reimbursement or compensation claims
- Unverified routes inferred from merchant names
- Raw tickets, itineraries, and booking files
<!-- END GENERATED: object-domain-summary -->

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
travel/
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
