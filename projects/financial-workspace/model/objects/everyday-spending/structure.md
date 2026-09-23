---
title: Everyday spending relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Everyday spending structure

```text
Spending occurrence 0..1 -- 0..* Receipt line
Spending occurrence 0..* -- 0..* Transaction
Spending occurrence 0..* -- 0..* Evidence assertion
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
