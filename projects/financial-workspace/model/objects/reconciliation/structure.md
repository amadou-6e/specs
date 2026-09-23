---
title: Reconciliation relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Reconciliation structure

```text
Transaction 1 -- 0..* Reconciliation link -- 1 Domain subject
Reconciliation link 1 -- 0..* Allocation
Exception 0..* -- 0..* Reconciliation link
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
