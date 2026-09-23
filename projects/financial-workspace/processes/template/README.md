---
title: Example financial process
status: template
kind: process
owners:
  - financial-workspace
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related: []
---

# Example financial process

This folder is copied and renamed for each repeatable workflow.

```text
<process>/
|-- README.md    1
|-- workflow.md  1
`-- examples/   0..1
```

The README owns purpose, scope, triggers, inputs, outputs, identities, invariants, approval boundaries, completion criteria, and maintenance responsibility. `workflow.md` owns the decision flow and failure paths. `examples/` may contain small reviewed fixtures or diagrams; generated runs do not belong here.
