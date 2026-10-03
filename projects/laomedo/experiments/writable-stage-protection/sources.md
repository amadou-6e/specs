---
title: Writable stage protection sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [Agent execution E05, S04 and Q17/Q18](../../subsystems/agent-execution/design/decision-readiness.md), specs 6ff8995.
- [Execution isolation target](../../subsystems/agent-execution/contract/isolation.md), still draft and containing a noted older read-only versus writable-checkout conflict.
- [EXP-18 issue](https://github.com/amadou-6e/laomedo/issues/48) requires protocol review before a pinned Docker test.
- [EXP-07 lease protocol](../orphan-lease/protocol.md) is a prerequisite; no E05 runtime evidence is claimed here.
- [2026-10-03 protocol review](https://github.com/amadou-6e/specs/pull/195#pullrequestreview-5399309348) approved create-only steps 1-2 and required exact inspect, network, denial-evidence and host-symlink amendments before stage startup.
- [2026-10-03 verifier review](https://github.com/amadou-6e/laomedo/pull/58#pullrequestreview-5399309404) reproduced eight create-only Docker downgrades accepted by the earlier verifier.
