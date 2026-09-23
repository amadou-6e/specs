---
title: Recurring expenses relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Recurring expenses structure

```text
Recurring service 1 -- 0..* Contract term
Recurring service 1 -- 0..* Service month
Service month 0..* -- 0..* Transaction
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
