---
title: Financial position entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Financial position schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Asset position | `asset_position_id` | subject, cutoff, amount, currency, valuation basis |
| Liability position | `liability_position_id` | obligation, cutoff, amount, currency, certainty |
| Monthly snapshot | `scope + cutoff` | account balances, assets, liabilities, valuation policy |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
