---
title: Decisions
status: active
kind: decision
owners:
  - example-team
last_reviewed: 2026-01-01
applies_to:
  - example-project
supersedes: null
related: []
---

# Decisions

Expandable document collection: each entry is one independently owned Markdown
document explaining why a durable choice was made.

## Contained elements

```text
decisions/
├── 1 README.md
├── 1 template.md
└── 0..* <NNNN>-<slug>.md entries
```

## Entries

- [template](template.md) — copyable schema example (not an active decision).
- [0001-use-sqlite-for-cache](0001-use-sqlite-for-cache.md) — storage engine choice
  for Widget Store.
