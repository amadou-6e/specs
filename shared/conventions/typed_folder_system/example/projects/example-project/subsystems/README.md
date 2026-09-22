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

## Contained elements and relationships

```text
subsystems/
├── 1 README.md
├── 1 template/       # copyable schema example, status: template
└── 0..* <subsystem>/  # named entries, one per owned behavioral boundary
```

To add a subsystem, copy `template/`, rename the copy, and replace its `status:
template` frontmatter and example content. Do not nest a copied template beneath
another template, and do not add an extra naming layer between `subsystems/` and the
entry folder.

## Entries

- [template](template/README.md) — copyable schema example (not an active subsystem).
- [widget-store](widget-store/README.md) — owns widget persistence.
