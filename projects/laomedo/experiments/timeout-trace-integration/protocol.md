---
title: Timeout trace integration protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The [prospective protocol at `2a2a1ad`](https://github.com/amadou-6e/laomedo/blob/2a2a1ad/experiments/exp66/PROTOCOL.md)
fixed one Langflow v2 call, a 3-second effective server timeout, a 6-second
synthetic runner delay, and read-only job-status polls at 0, 1, 4 and 7
seconds after a `408`. Laomedo must commit run/trace/stage/invocation IDs
and the dispatch attempt before calling Langflow. It may not retry the
timed-out POST. Reopening its store must preserve the trace without dispatch.

The first call's trace retained a source hash for the effect but omitted the
full sanitized source row required to recompute it. [Amendment 01 at
`95c1121`](https://github.com/amadou-6e/laomedo/blob/95c1121/experiments/exp66/AMENDMENT-01.md)
was committed before one diagnostic replication. It changed only capture of
the runner row's `case`, `event`, `utc` and `monotonic` fields. The first
observation remains separately pinned and is not passed off as final
hash-verifiable evidence.

Both calls were zero-model, local synthetic tests. Neither protocol authorizes
real-agent cancellation or proves that a timeout stops a remote action.
