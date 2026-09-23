---
title: Subsystem template
status: template
kind: subsystem
owners:
  - example-team
last_reviewed: 2026-01-01
applies_to:
  - example-project
supersedes: null
related: []
---

# Subsystem template

Copy this folder and rename the copy for a new subsystem entry. This README
demonstrates the internal cardinality every copy must follow.

## Contained elements

```text
<subsystem>/
├── 1 README.md
├── 1 contract/README.md
├── 1 design/README.md
├── 1 validation.md
├── 0..1 guides/
└── 0..1 migrations.md
```

## Problem and ownership

State the capability this subsystem owns and its boundary.

## Guarantees

Summarize the guarantees and link to [contract/README.md](contract/README.md).

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Validation](validation.md)
