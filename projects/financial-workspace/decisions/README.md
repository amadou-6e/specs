---
title: Decisions
status: active
kind: decision
owners:
  - amadou-6e
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related: []
---

# Decisions

Expandable document collection: each entry is one independently owned Markdown
document explaining why a durable choice was made — for example a concrete storage,
schema, or tooling choice that the [architecture](../architecture/README.md)
documents don't need to justify in place.

## Contained elements and relationships

```text
decisions/
├── 1 README.md            # this file
├── 1 template.md          # copyable schema example, status: template
└── 0..* <NNNN>-<slug>.md   # named entries, sequentially numbered
```

To add a decision, copy `template.md` to the next sequential number (`NNNN`, zero
padded to four digits) and a short slug, then replace its `status: template`
frontmatter and example content. Decisions are single files — do not create a folder
for an ordinary decision record.

## Entries

- [template](template.md) — copyable schema example (not an active decision).

No real decisions have been recorded yet. The architecture documents in
[../architecture/](../architecture/README.md) currently carry proposals and open
questions (see `data-model.md`'s "Decisions before migration" and
`cash-flow-workflow.md`'s "Open design choices") that have not yet been resolved;
once one of them is settled, record it here rather than editing the proposal in
place.
