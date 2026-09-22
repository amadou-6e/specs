---
title: Example Project architecture
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

# Example Project architecture

Fixed top-structured category: this file is the one system-wide structure for
architecture. A real project may add focused documents beside this one (for example
`architecture/data-flow.md`), but does not create arbitrary new architecture
partitions or a copyable `architecture/template/` folder — that is what distinguishes
a fixed top-structured category from an expandable folder collection.

## System context

The example system has one subsystem, [Widget Store](../subsystems/widget-store/README.md),
which owns widget persistence for the rest of the (fictional) system.

## Cross-subsystem invariants

None yet — this example has only one subsystem, so there are no cross-subsystem
invariants to record.
