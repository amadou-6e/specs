---
title: Pinned Langflow server identity execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution record

The [Phase G protocol frozen at Laomedo `e52194a`](https://github.com/amadou-6e/laomedo/blob/e52194a/experiments/exp22/PHASE-G-CORRELATION-PROTOCOL.md)
named a credential-free identity gate. The implementation used a disposable
Langflow 1.12.3 container pinned to image digest
`sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`
and a loopback fake runner. A saved flow was imported once, then invoked twice
through `/api/v1/run/{flow_id}`. The component code was modified only in the
disposable imported flow to send `graph.run_id`, `graph.flow_id` and stage ID
to the fake runner. No agent provider or model was called.

The first server attempt received 403 before runner dispatch because it
supplied only disposable auto-login bearer authentication. Later attempts
used a disposable Langflow API key kept in process memory. The run took a
private SQLite backup before removing the disposable container and used a
[read-only inspector](https://github.com/amadou-6e/laomedo/blob/4f12370/experiments/exp22/phase_g_inspect_snapshot.py)
to report table and column match counts without row contents. The originally
mounted `/app/langflow` host directory remained empty; the pinned image's
default SQLite URL pointed inside its site-packages tree. The test did not
restart the server or demonstrate durable storage across restart.
