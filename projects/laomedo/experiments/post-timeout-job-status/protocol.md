---
title: Post-timeout job-status protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The [prospective protocol at `c5f2f68`](https://github.com/amadou-6e/laomedo/blob/c5f2f68df9f869656707c26fa4e08ccbe2ef4ce8/experiments/exp65/PROTOCOL.md)
fixed one v2 synchronous call, a 6-second loopback endpoint, a verified
3-second server ceiling, an 8-second component limit, a 15-second caller
limit, and read-only job-status polls at 0, 1, 4 and 7 seconds after `408`.
It limited each run to zero model turns and forbade retrying the timed-out POST.
The first run produced four `500` lookups but omitted their `detail.code`.

[Amendment 01 at `1c6790a`](https://github.com/amadou-6e/laomedo/blob/1c6790a63000bd114278bdf88b04ddff38ef8529/experiments/exp65/AMENDMENT-01.md)
was committed before a separate diagnostic run. It allowed only whitelisted
error-code capture; the invocation and poll schedule remained unchanged. The
first observation is retained at its committed revision, not silently
reinterpreted or overwritten in the evidence record.

Neither protocol tests a real Codex worker, Laomedo IF-06/07 trace persistence,
or cancellation. A `408` or terminal job state alone cannot prove the remote
effect stopped.
