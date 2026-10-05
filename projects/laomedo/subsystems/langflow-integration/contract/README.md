---
title: Langflow integration contracts
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration contract index

[Interfaces](interfaces.md) own run entry/correlation, lifecycle events, run
context and follow-up requests. Agent invocation and outcome are jointly
described there but their agent-side behavior belongs to
[agent execution](../../agent-execution/contract/interfaces.md). Shared record
definitions remain in [architecture](../../../architecture/shared-contracts.md).
The proposed [timeout and late-effect reconciliation](timeout-reconciliation.md)
qualifies IF-06/07 and Q11 without changing Langflow's graph-state ownership.

Contract container: README.md (1), focused interface/configuration pages
(0..*). [Validation](../validation.md) qualifies maturity.
