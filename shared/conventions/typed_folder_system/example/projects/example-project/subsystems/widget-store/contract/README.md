---
title: Widget Store contract
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

# Contract

- `create(widget)` returns a unique id; the widget is durably stored before the call
  returns.
- `get(id)` returns the widget or a not-found error; it never returns partially
  written state.
- `delete(id)` is idempotent: deleting a missing id is not an error.
- Storage has no enforced size limit in this example.
