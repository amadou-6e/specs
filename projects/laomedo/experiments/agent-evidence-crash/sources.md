---
title: Agent evidence crash sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [EXP-05 issue](https://github.com/amadou-6e/laomedo/issues/35) and
  [agent-execution readiness E02](../../subsystems/agent-execution/design/decision-readiness.md).
- [IF-05 invocation](../../subsystems/agent-execution/contract/schemas/if-05-stage-invocation.md)
  and [IF-08 event](../../subsystems/agent-execution/contract/schemas/if-08-agent-event.md)
  are draft target payloads, not claims of deployed interfaces.
- [EXP-04 run-store result](../durable-pre-dispatch/iterations/2026-10-02/results.md)
  is the prerequisite. Its implementation was merged in
  [Laomedo PR #54](https://github.com/amadou-6e/laomedo/pull/54).
- [Laomedo source at `e274903`](https://github.com/amadou-6e/laomedo/tree/e274903242a4f1724fc598ba50de9cff4f433690)
  contains the EXP-05 harness, tests and sanitized observation. This is a
  published issue branch revision, not yet a merged implementation result.
- [Run-traces T07](../../subsystems/run-traces/design/decision-readiness.md)
  owns the still-open source-key versus at-least-once replay policy for
  [EXP-09](https://github.com/amadou-6e/laomedo/issues/39).
