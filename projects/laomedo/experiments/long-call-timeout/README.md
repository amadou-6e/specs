---
title: Long-call timeout experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Long-call timeout

[EXP-10](https://github.com/amadou-6e/laomedo/issues/40) asks whether a
timed-out Langflow agent-node call can still cause an external effect. The
[prospective protocol](protocol.md) used a synthetic in-container HTTP runner
and zero model turns. A prospective amendment allowed a separate direct-capture
replication. The [2026-10-05 attempt](iterations/2026-10-05/README.md)
observed late effects after outer-client and v2 server timeouts in both runs. This is
runtime evidence, not an implemented Laomedo run/trace outcome contract.

Read the [source pins](sources.md) before treating the result as portable to
another Langflow version, route or timeout configuration.
