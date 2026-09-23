---
title: Reconciliation entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Reconciliation schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Reconciliation link | `link_id` | typed endpoints, method, state, evidence, rule/reviewer, timestamps |
| Allocation | `allocation_id` | link or endpoints, amount, currency, tolerance, remainder |
| Exception | `exception_id` | scope, reason, evidence gap, status, resolution |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
