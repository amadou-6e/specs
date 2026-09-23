---
title: Matters relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Matters structure

```text
Matter 1 -- 0..* Matter event
Matter 1 -- 0..* Claim
Claim 0..* -- 0..* Transaction
Matter 0..* -- 0..* Evidence assertion
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
