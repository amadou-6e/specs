---
title: Local application and Langflow demonstration design index
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Local application and Langflow demonstration

The owner interview is recorded in [decision 0006](../../../decisions/0006-release-packages.md).
Observable behavior and acceptance are owned by
[application execution](../contract/application-execution.md), with
[Output Contract](../../agent-execution/contract/output-contract.md) owning
validation/precheck semantics. This original review path remains a design index;
it is not a second copy of those requirements or evidence of implementation.

## Immediate mechanism work

The owner redirected implementation to a runnable Langflow graph before the
standalone issue-board/chat UI. Reuse issue ingestion and Skill/Codex components;
compose them with the proposed Output Contract, conditional routing and scoped
draft publication. Existing components were inventoried at Laomedo develop
`6882fc8ea7a90bcaf310fa6c38f8a049789797e5`. No contract component or composed
acceptance result existed in that inventory.

Proposed dataflow:

```text
Issue context ──► Agent ◄── Skill Reference
                    │
                    ▼
              Output Contract
                    │
                    ▼
             Conditional routing
             /        |         \
       success    task failure   rejection
          |           |           |
      draft PR   reviewer/HITL   configured route
```

Resolve same-requirement precheck access, contract/output port types,
issue/run provenance, recovery references and publisher capability lifetime
before implementation. The existing active-stage write grant cannot simply
be reused after completion. These are open mechanism choices, not approved
transport APIs or live-write grants.

## Reading path and evidence boundaries

- [Release overview](../../../architecture/release-packages.md): packages and scope.
- [Assignment and frozen tags](../contract/application-execution.md#workflow-tags-and-frozen-revisions).
- [Chat/editor handoff](../contract/application-execution.md#direct-laomedo-chat-assistant).
- [Complete demonstration and acceptance](../contract/application-execution.md#next-requested-demonstration-the-complete-langflow-graph).
- [Existing Work Graph](../contract/work-graph.md): source snapshots/readiness.
- [Validation](../validation.md): existing bounded evidence, not this new demo.

The shdennlin/issue-graph functional reference and GitHub Actions visual
reference remain recorded in the contract. No package adoption is selected.
Reviewed Draw.io must own new UI geometry, controls, states and transitions.
No Draw.io or standalone UI was created/activated in this interview repair.
