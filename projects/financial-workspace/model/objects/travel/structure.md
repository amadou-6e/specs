---
title: Travel relationship model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Travel structure

```text
Journey 1 -- 1..* Travel segment
Journey 0..* -- 0..* Booking
Journey 0..* -- 0..* Travel stay
Journey 0..* -- 0..* Purchase item
```

Relationships crossing native systems use typed mappings and retain both endpoint identities.
