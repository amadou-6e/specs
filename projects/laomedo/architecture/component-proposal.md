---
title: Agent and skill component specification index
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent and skill component specification index

Status: proposed, 2026-09-28. This index scopes the first implementation and
its dependencies. Each component has its own behavioral spec. None of these
Markdown files specifies UI geometry, controls, states, or transitions; those
require view-owned Draw.io specifications before UI implementation.

Implementation update, 2026-10-01: the
[local Langflow skill-agent pilot](../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
now verifies single-user Codex execution, native skill-read/tool events,
snapshot-bound restart/resume, fresh-run separation, and cancellation. The
sections below preserve the original proposal and estimates rather than a
current checklist of missing prototype capabilities. Claude parity and full
product contracts remain incomplete.

## What is being specified

Laomedo should let a flow select an exact skill revision, run Codex or Claude
Code with that skill and selected model/effort, inspect what happened inside
the agent, and ask an agent to propose a skill edit. The source execution and
skill revision remain unchanged when an experiment or edit draft is created.

| Specification | Responsibility |
| --- | --- |
| [Shared contracts](shared-contracts.md) | IDs, refs, run request/result, component edges, provenance |
| [Skill Revision](../subsystems/skill-registry/contract/revisions.md) | Versioned skill bundles and isolated rule/example reads |
| [Skill Draft](../subsystems/skill-registry/contract/drafts.md) | Versioned editing policy, agent edit, patch, validation, promotion boundary |
| [Codex Agent](../subsystems/agent-execution/contract/codex.md) | Model/effort, session lifecycle, skill delivery, native events |
| [Claude Agent](../subsystems/agent-execution/contract/claude.md) | Equivalent Claude behavior and provider-specific differences |
| [Runner isolation](../subsystems/agent-execution/contract/isolation.md) | Private persistent profiles, workspace boundaries, grants, local versus remote storage |
| [Run traces](../subsystems/run-traces/contract/README.md) | Raw and normalized events, correlation, inspection, failure handling |

The project separates a versioned **Definition** (settings, skill references,
input contract), an immutable observed **Execution** (events, outputs,
side effects), and a linked **Experiment** (a new run or edit draft with its
own identity). An experiment never overwrites its source. Recorded replay is
not re-execution, and a trace cannot prove every declared rule was loaded.

## Existing evidence and gaps

An uncommitted local fixture proved that a Langflow APIRequest node can call a
Codex bridge for a fixed read-only CSV task. Reviewers cannot inspect that
fixture in this repository. The bridge pasted one `SKILL.md` into the prompt,
hashed that file, used the user's default Codex profile, and returned a
final response and thread ID.
It has no isolated profile, native skill bundle, model/effort controls,
resumption, or inner trace. No local Claude adapter has been verified. These
gaps define the starting point rather than completed capability.

Langflow custom components are a possible initial canvas integration. The
components must call shared Laomedo services rather than own the only copy of
skill revisions, sessions, or traces. This preserves a path to a dedicated
Laomedo editor without changing the execution contract.

## Delivery order and effort

Assume one engineer familiar with Python, Langflow, and the existing bridge.
The estimates include basic integration tests and an inspection surface;
they exclude model usage costs and a full UI design/implementation cycle.
Claude estimates carry more uncertainty until an SDK spike verifies native
events, skills, effort, and session storage.

| Slice | Depends on | Engineering estimate |
| --- | --- | ---: |
| Shared records and runner | None | 3-5 days |
| Skill Revision read path | Shared records | 3-5 days |
| Codex Agent read-only adapter | Runner and monitoring event intake | 3-5 days |
| Skill Draft edit path | Skill Revision and agent adapter | 5-7 days |
| Claude Agent adapter | Runner, contracts, monitoring | 4-6 days |
| Inspection and hardening | Both adapters | 3-5 days |

Allow **about 4-7 engineer-weeks** for a single-user local MVP. The lower end
assumes the existing Codex bridge can be adapted cleanly. Allow **8-12 weeks**
for a robust multi-user product with recovery and a dedicated Laomedo UI.
Remote-only persistence adds deployment and operations work. These estimates
are planning ranges; a short Claude SDK spike should narrow them.

## Cross-spec acceptance gate

The first usable vertical slice must prove a pinned skill revision, a
read-only isolated Codex run, a persistent private native session, and a
trace containing tool activity beyond the final answer. The second slice
must prove a draft skill edit under a pinned policy, with an unchanged base
revision and reviewable patch. The third adds Claude with equivalent run
identity and inspection. Each provider-specific absence is reported as
unknown or unsupported, never silently normalized into a false capability.

## Open product decisions

- Does “no new session on the user's computer” mean absent from personal
  agent history, or no native session files physically on the client?
- Is Git the canonical skill store or an export of a Laomedo registry?
- Which manifest format defines stable rule/example IDs and dependencies?
- Who can promote a skill draft or grant write and network permissions?
- Is Langflow only an initial canvas, or part of the first shipped product?

## External references

- [Codex SDK](https://developers.openai.com/codex/sdk/) and
  [App Server](https://developers.openai.com/codex/app-server/). Both URLs
  currently redirect to the official `learn.chatgpt.com` documentation.
- [Claude Agent SDK Python reference](https://code.claude.com/docs/en/agent-sdk/python),
  [sessions](https://code.claude.com/docs/en/agent-sdk/sessions), and
  [skills](https://code.claude.com/docs/en/agent-sdk/skills).
- [Langflow custom components](https://docs.langflow.org/components-custom-components)
  and [traces](https://docs.langflow.org/traces).
