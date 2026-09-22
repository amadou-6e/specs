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

## Contained elements and relationships

```text
<subsystem>/
├── 1 README.md
├── 1 contract/
│   └── 1 README.md
├── 1 design/
│   └── 1 README.md
└── 1 validation.md
```

A mature subsystem entry requires `README.md`, `contract/README.md`,
`design/README.md`, and `validation.md`. (The full convention also allows optional
`contract/interfaces.md`, `contract/configuration.md`, `contract/extensions.md`,
`design/<language>.md`, `guides/`, `extensions/`, and `migrations.md` — omitted here
to keep the worked example small.)

## Problem and ownership

State the capability this subsystem owns and its boundary.

## Guarantees

Summarize the guarantees and link to [contract/README.md](contract/README.md).

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Validation](validation.md)
