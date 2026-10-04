---
title: Agent evidence crash protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The [issue protocol](https://github.com/amadou-6e/laomedo/issues/35) specified
synthetic kills at reservation, native-ID receipt and event flush. This detailed
protocol was written **after** the attempt, not prospectively frozen or
independently reviewed before execution.

Use the merged EXP-04 SQLite run store to reserve run and trace IDs. In the
same temporary database, reserve one stage/invocation identity before a
synthetic callback, persist a synthetic native-session ID when received, and
commit one raw event before deriving its projection. Exit the child at:
before invocation reservation, after reservation, after dispatch/before native
ID, after native-ID receipt, after raw-event flush, and after projection.
Normal completion is the control. Restart by reopening the database, mark
unfinished invocation/run rows crashed, project only committed raw receipts,
and never redispatch the callback.

Compare the child exit code, dispatch-attempt count, IDs, native-ID presence,
raw and projected receipt sequences, stream completeness, and terminal status.
Pass only if reserved identities are unique/recoverable, absent IDs/events are
not invented, the raw receipt survives a flush crash, projection is traceable
to that receipt, and no crashed invocation becomes complete or resumes.
This is a process-kill test, not a host-power-loss or real-provider test.
No model calls, remote writes, credentials, or personal sessions are used.
