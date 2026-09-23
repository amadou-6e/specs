---
title: Everyday spending entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Everyday spending schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Spending occurrence | `spending_id` | merchant, commercial date, amount, currency, category, evidence status |
| Receipt line | `receipt_line_id` | occurrence, description, quantity and line amount when available |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
