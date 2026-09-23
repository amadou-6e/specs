---
title: Transactions entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Transactions schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Transaction | `transaction_id` | account, signed amount, currency, observed status, posting/value dates, counterparty, provenance |
| Transfer pair | `transfer_pair_id` | outbound transaction, inbound transaction, review state |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
