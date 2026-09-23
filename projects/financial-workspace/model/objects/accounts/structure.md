---
title: Accounts relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Accounts structure

```text
Account 1 -- 0..* Account alias
Account 1 -- 0..* Transaction
Account 1 -- 0..* Snapshot balance
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
