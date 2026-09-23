---
title: Evidence relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Evidence structure

```text
Evidence source 1 -- 0..* Evidence assertion
Evidence assertion 1 -- 1 Domain subject
Derived artifact 1 -- 1..* Evidence source
Coverage record 1 -- 0..* Evidence source
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
