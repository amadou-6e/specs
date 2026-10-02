---
title: UI and backend-death protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

Import a no-model Chat Input -> synthetic stage -> Chat Output flow into a disposable pinned Langflow 1.12.3 server. The custom stage reserves a Laomedo run/trace record, commits a dispatch attempt, writes an entered sentinel and waits for a release file. Store Langflow database and Laomedo launch records in a private Docker volume. Run A: close the HTTP client socket while the stage waits, open the saved flow again with a fresh session token, release and confirm the same Laomedo run completes. Run B: wait for another stage entry, hard-kill the Langflow container, inspect its stopped state, restart the same image/volume with a pre-server startup sweep, and verify the old run is crashed/incomplete with one attempt and no redispatch.

Pass requires A still active after UI disconnect and completed after release; B terminal crashed/incomplete after restart, no same-run redispatch. Observe trace ID and container state. This test uses two local synthetic runs, zero model turns, and no agent container; that omission is explicit. The written protocol records the executed fixture, not a separately preregistered review.
