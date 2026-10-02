---
title: Durable pre-dispatch protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

Use the EXP-03 synthetic graph as exact launch input. Require all node source hashes and a nonempty resolved config. Persist run ID, trace ID, frozen graph, graph/component hashes, config bytes/ref and trigger in SQLite with synchronous FULL before acknowledging launch. Commit a conservative dispatch attempt before calling the deterministic callback. Restart after controlled process exit at: before write; after commit before ack; after ack before dispatch; after attempt before callback; after callback before completion; and normal completion. Compare persisted rows with a monotonic synthetic callback counter. Startup sweep marks every nonterminal row crashed and never replays.

Pass: no callback without recoverable identity; failed/absent reservation prevents dispatch; no same-run replay after restart. A committed attempt with no callback and a callback with no completion must be reported as separate ambiguous crash windows, not reclassified as no effect or complete. Zero model turns. The written protocol documents the executed fixture; it was not separately reviewed before execution.
