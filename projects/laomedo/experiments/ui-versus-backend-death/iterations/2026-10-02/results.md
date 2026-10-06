---
title: UI versus backend-death results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

Run A was dispatching when the client socket closed. Langflow remained alive; the saved flow could be opened again. After gate release, the same Laomedo run completed. The client received BrokenPipeError, which did not imply stage cancellation.

Run B was dispatching with one committed attempt before the backend hard kill. Docker changed from running to exited. On restart, startup sweep reported one run and the record became terminal crashed, evidence_complete=0, reason backend_restart. Its dispatch attempts remained one, with no same-run redispatch. Run A remained completed after restart. The record retained a trace ID; no downstream trace-event completeness beyond the flag was assessed.

This passes the tested distinction between UI disconnect and fate-shared backend death. It does not prove that an independently running agent container is stopped or loses a grant. EXP-07 tests that separate boundary. It also does not implement a complete production Langflow adapter or live agent run.
