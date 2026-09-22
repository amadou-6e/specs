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

## Contained elements and relationships

```text
decisions/
├── 1 README.md
├── 1 template.md              # copyable schema example, status: template
└── 0..* <NNNN>-<slug>.md       # named entries, sequentially numbered
```

To add a decision, copy `template.md` to the next sequential number (`NNNN`, zero
padded to four digits) and a short slug, then replace its `status: template`
frontmatter and example content. Decisions are single files — do not create a folder
for an ordinary decision record.

## Entries

- [template](template.md) — copyable schema example (not an active decision).
- [0001-use-sqlite-for-cache](0001-use-sqlite-for-cache.md) — storage engine choice
  for Widget Store.
