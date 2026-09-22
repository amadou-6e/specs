---
title: Widget Store design
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

# Design

Widget Store is backed by a single SQLite file (see
[decision 0001](../../../decisions/0001-use-sqlite-for-cache.md)). Reads and writes
go through one connection guarded by a mutex; there is no separate cache layer in
this example.
