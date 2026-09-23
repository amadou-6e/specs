---
title: Tax relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Tax structure

```text
Tax year 1 -- 0..* Tax classification
Tax year 1 -- 0..* Tax filing
Tax year 1 -- 0..* Tax assessment
Tax classification 1 -- 1 financial subject
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
