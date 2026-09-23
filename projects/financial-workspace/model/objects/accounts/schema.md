---
title: Accounts entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Accounts schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Account | `account_id` | provider, native account reference, type, ownership scope, currency policy, lifecycle status |
| Account alias | `alias_id` | account, provider scope, native identifier, validity interval |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
