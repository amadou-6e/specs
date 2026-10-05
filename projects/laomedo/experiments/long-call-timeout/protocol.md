---
title: Long-call timeout protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The [source protocol](https://github.com/amadou-6e/laomedo/blob/e4f4685e0a58d3825ab6c6c7175e57fff3ca116a/experiments/exp10/PROTOCOL.md)
was committed before the successful four-case run. It froze pinned Langflow
1.12.3, its image digest, one disposable localhost-bound container, a
loopback-only synthetic runner, four delays and timeout limits, one attempt
per case, and **zero model turns**. It forbids inferring that a timed-out
external action stopped without effect evidence.

Cases: a 0.2-second control; a 4-second runner delay with a 1-second outer
client timeout; a 5-second delay with a 2-second component HTTP timeout; and
a 6-second delay with a verified 3-second Langflow v2 synchronous server
timeout. The fixture's startup corrections did not change any case or limit.
Exact source and artifact hashes are in the [manifest](iterations/2026-10-05/evidence/manifest.md).
