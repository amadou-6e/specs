---
title: Native Codex node acceptance
status: complete
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Native Codex node acceptance

Bounded installed-node acceptance for [Laomedo #21](https://github.com/amadou-6e/laomedo/issues/21).
The initial four-turn attempt is preserved, followed by a separately authorized
two-turn retry. The ledger is now 6/6. Bounded #21 acceptance work is complete
and ready for review; no issue is closed or product specification accepted here.

Read [protocol](protocol.md), [sources](sources.md), and [attempt index](iterations/README.md).
Contract owner: [Langflow node](../../subsystems/agent-execution/contract/langflow-node.md).
Fresh execution, restart/resume, independent fresh tool/host checks and explicit
cancel through the imported node are observed. Cancel uses runner flag/transport
teardown, not a claimed native interrupt acknowledgement. See the
[retry results](iterations/2026-10-01-retry/results.md); UI Stop and outstanding
command semantics remain follow-ups #22 and #24.

