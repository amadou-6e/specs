---
title: Recurring expenses entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Recurring expenses schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Recurring service | `service_id` | provider, description, category, cadence, start/end, lifecycle |
| Service month | `service_id + service_month` | expected amount, currency, due date, observed settlement state |
| Contract term | `term_id` | service, effective interval, price and cadence |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
