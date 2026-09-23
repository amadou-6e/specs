---
title: Subsystems
status: active
kind: architecture
owners:
  - example-team
last_reviewed: 2026-01-01
applies_to:
  - example-project
supersedes: null
related: []
---

# Subsystems

Expandable folder collection: each entry below is an independently owned,
multi-file folder following the schema demonstrated by [`template/`](template/).

## Contained elements

```text
subsystems/
├── 1 README.md
├── 1 template/
└── 0..* <subsystem>/ entries
```

## Entries

- [template](template/README.md) — copyable schema example (not an active subsystem).
- [widget-store](widget-store/README.md) — owns widget persistence.
