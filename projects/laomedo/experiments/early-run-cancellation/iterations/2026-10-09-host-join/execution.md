---
title: Playground host join execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution record

The [Phase G correlation protocol](https://github.com/amadou-6e/laomedo/blob/e52194a53f8cf7278b9931f993fe0fed8c96d4ac/experiments/exp22/PHASE-G-CORRELATION-PROTOCOL.md)
preceded the installed identity work. The later
[one-turn protocol](https://github.com/amadou-6e/laomedo/blob/aa12af6cd6389dc4fdf81528772fdc6e58d4ef1d/experiments/exp22/PHASE-G-LIVE-PROTOCOL.md)
and probe were committed at `aa12af6` before the real submission. A
credential-free disposable SQLite restart check and a no-model real-route
preflight passed first. The same Claude reviewer session gave a go for one
bounded local submission after a focused recheck of the bridge-route Stop
attribution. This specs page is retrospective evidence, not a protocol freeze.

The local test used the pinned Langflow 1.12.3 image, the checked-in five-node
flow with an optional host-bridge input, a private SQLite mount, one loopback
host bridge, the existing single-user Codex login volume, and one-turn runner
limit. The Langflow container received only the bridge token, not the runner
token or Codex login. The browser opened Playground and clicked Send. Its task
would first attempt a content-free credential read, then start a 30-second
sentinel command so visible Stop could interrupt it. The native turn failed
before those commands, so the test did not reach its Stop trigger. No GitHub
credential, grant or write was provided.

Private state remains outside Git at
`%LOCALAPPDATA%/Laomedo/exp22-phase-g-live-20261009-a/`. The shared ledger
reserved exactly one slot immediately before Send, moved from 6/12 to 7/12,
and records `real_join_inconclusive`. No retry occurred. Only sanitized status,
hashes and evidence limits are published.
