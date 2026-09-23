---
title: Widget Store
status: active
kind: subsystem
owners:
  - example-team
last_reviewed: 2026-01-01
applies_to:
  - example-project
supersedes: null
related: []
---

# Widget Store

## Contained elements

```text
widget-store/
├── 1 README.md
├── 1 contract/README.md
├── 1 design/README.md
└── 1 validation.md
```
A named entry copied from [`subsystems/template/`](../template/README.md) and
filled in — this is what a real, non-template subsystem looks like.

## Problem and ownership

Widget Store owns durable persistence of widgets: creating, retrieving, updating, and
deleting them. Nothing else in the example system writes widget state directly.

## Guarantees

A write is durable once its call returns. See
[contract/README.md](contract/README.md) for the full guarantee list.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Validation](validation.md)
