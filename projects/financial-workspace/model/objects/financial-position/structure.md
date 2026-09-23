---
title: Financial position relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Financial position structure

```text
Monthly snapshot 1 -- 0..* Account balance
Monthly snapshot 1 -- 0..* Asset position
Monthly snapshot 1 -- 0..* Liability position
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
