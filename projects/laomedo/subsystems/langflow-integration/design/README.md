---
title: Langflow integration design
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration design

The target editor embeds a heavily modified Langflow surface while retaining
all Langflow components. The single-agent form supplies a one-agent graph;
multi-agent authoring uses the graph editor. Stage defaults are copied at
creation, so later default changes do not mutate existing stage settings.

This design depends on verified Langflow hooks for agent-node invocation,
workflow lifecycle and artifact/file handoffs. A separate execution overview
shows agent invocation timing and telemetry; it does not mirror every Langflow
component. Waterfall presentation and selective rerun remain open.

No editor modification, API binding or orchestration persistence mechanism is
implemented by this document. Observable behavior belongs to
[interfaces](../contract/interfaces.md). Design container: README.md (1),
focused mechanism pages (0..*).

The [decision-readiness ledger](decision-readiness.md) separates first-slice
intent from unresolved Langflow capabilities, owner choices and bounded
experiments; it is not a second runtime contract.
