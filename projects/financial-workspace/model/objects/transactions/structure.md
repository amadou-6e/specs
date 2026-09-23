---
title: Transactions relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Transactions structure

```text
Account 1 -- 0..* Transaction
Transaction 0..1 -- 0..1 Transfer pair -- 0..1 Transaction
Transaction 0..* -- reconciliation links -- 0..* economic subjects
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
