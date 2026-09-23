---
title: Financial entity relationships
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/objects/financial-domain/catalog, model/objects/financial-domain/states-and-time]
---

# Relationship model

This view answers where ownership ends and explicit join records begin.

```text
Account 1 -- 0..* Transaction
Order 1 -- 1..* Purchase item
Recurring service 1 -- 0..* Service month
Journey 0..1 -- 0..* Purchase item
Matter 1 -- 0..* Claim
Evidence 1 -- 0..* Evidence link -- 1 Domain entity
Transaction 1 -- 0..* Reconciliation link -- 1 Domain entity
Transaction 1 -- 0..* Allocation -- 1 Domain entity
```

Domain entity can be Purchase item, Service month, Claim, Matter, Tax classification, or another supported subject. Links carry typed endpoints; reconciliation adds method, state, evidence, timestamps, and reviewer/rule; allocation adds amount/currency.

The 2026 crosschecks are specialized projections: `ledger_id` identifies a purchase candidate, transaction IDs identify movements, and statuses preserve zero, unique, and ambiguous candidates. Heuristics do not imply confirmation. Titles, paths, merchant strings, amounts, and date proximity are matching attributes, not identity. External IDs and paths remain owned by system/repository entries; cross-system owns mappings.
