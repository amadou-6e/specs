---
title: Widget Store validation
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

# Validation

| Guarantee | Check |
| --- | --- |
| Durable write before `create` returns | `tests/test_widget_store.py::test_create_is_durable` |
| Idempotent delete | `tests/test_widget_store.py::test_delete_missing_id_is_noop` |

No benchmark coverage exists yet for concurrent access; recorded here as a known gap
rather than left unstated.
