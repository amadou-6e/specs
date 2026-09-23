---
title: Procurement entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Procurement schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Order | `order_id` | merchant scope, order reference, order date, currency, total when supported |
| Purchase item | `purchase_id` | order, description, quantity, item amount when supported, category |
| Return | `return_id` | purchase items, request and receipt dates, status |
| Merchant refund | `refund_id` | return or purchase, expected and received amounts |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
