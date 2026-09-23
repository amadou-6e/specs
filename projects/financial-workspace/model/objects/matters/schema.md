---
title: Matters entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Matters schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Matter | `matter_id` | type, subject, opened date, lifecycle, responsible party |
| Claim | `claim_id` | matter, claimed amount, currency, submission and decision state |
| Matter event | `event_id` | matter, event type, effective time, actor, evidence |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
