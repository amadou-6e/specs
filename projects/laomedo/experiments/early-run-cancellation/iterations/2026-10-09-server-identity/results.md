---
title: Pinned Langflow server identity bounded result
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded result

The [published Laomedo Phase G result](https://github.com/amadou-6e/laomedo/blob/4f12370/experiments/exp22/PHASE-G-IDENTITY-RESULTS.md)
reports two fake-runner dispatches from one saved flow. Both carried the same
flow ID and configured stage ID; the two graph run IDs differed. A private
SQLite snapshot contained both graph run ID strings in `span.inputs`,
`span.outputs` and `message.session_metadata`. One also occurred in
`vertex_build.data`. The saved flow ID occurred in `message.session_id` and
`trace.session_id`, among other columns.

These are substring matches in one disposable database. They do not attest
the IDs as stable database keys, prove storage across restart, or establish a
durable Laomedo invocation-to-runner request binding. The earlier in-process
graph path exposed no saved flow ID; a second `arun` on the same graph object
did not dispatch the component again. The installed-server test used the API
run path, not Playground Stop. No model call occurred, so the user-extended
ledger remains **6/12**.

The host suite passed 366 tests with 8 skipped, and the pinned Langflow
custom-node suite passed 19 tests. Gate 2 still requires pre-dispatch
reservation, exact acknowledgement binding, and restart without redispatch.
The active-tool and pre-thread Stop findings are unchanged; #22/Q11 remain open.
