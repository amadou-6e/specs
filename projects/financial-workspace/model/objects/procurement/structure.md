---
title: Procurement relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Procurement structure

```text
Order 1 -- 1..* Purchase item
Purchase item 0..* -- 0..* Transaction
Purchase item 0..* -- 0..* Return
Return 0..1 -- 0..* Merchant refund
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
