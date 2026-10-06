---
title: Agent-event replay sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [EXP-09 issue #39](https://github.com/amadou-6e/laomedo/issues/39)
  defined the replay/reorder/keyless question and synthetic zero-model limit.
- [T07 decision 0003](../../decisions/0003-agent-event-replay.md) and
  [IF-08/IF-11 target](../../subsystems/run-traces/contract/interfaces.md)
  at specs `6b614e34eac93dea31ce4e80143c001fb4cdd066` supplied the
  selected, still-draft test oracle. [Specs PR #203](https://github.com/amadou-6e/specs/pull/203)
  was open when this attempt ran.
- [Laomedo source `3115d5b`](https://github.com/amadou-6e/laomedo/commit/3115d5bec3f15f250f5b1605873185e537cbe3d4)
  contains the test, probe and sanitized observation. Its base was
  `89d0dd6b2881179ec61ba58e4307221f7a21d79b`, containing the merged
  [EXP-05 raw store](../agent-evidence-crash/README.md). This source was
  published on issue branch `feat/39`, not a merged product capability at
  experiment time.
- [Historical #123 projector](../../research/runner-feasibility/sources/123.md)
  assumed source-ID stability and is a contrast, not an adapter modified by
  this experiment.
