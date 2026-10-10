---
title: Timeout trace integration experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Timeout trace integration

[Laomedo #66](https://github.com/amadou-6e/laomedo/issues/66) asks whether
Laomedo can preserve a partial trace under a durable pre-dispatch identity
when Langflow times out but a synthetic external effect arrives later. This
follows [EXP-65](../post-timeout-job-status/README.md), which observed the
late effect but did not test Laomedo's own trace.

Read the [prospective protocol and amendment](protocol.md), [source pins](sources.md),
and [2026-10-05 attempt](iterations/2026-10-05/README.md). The amended
replication is a bounded synthetic integration, not a real-agent cancellation
result or acceptance of the first-slice timeout gate.

The [native continuation](iterations/2026-10-09-native/README.md), executed on
2026-10-10, adds real Codex cancellation before and during a named file effect
after a host adapter wait timeout. Both cases passed with durable partial identity
and exact cleanup. This does not replace the dated synthetic server 408 evidence
or accept the broader Q11 outage and effect-accounting gate.
