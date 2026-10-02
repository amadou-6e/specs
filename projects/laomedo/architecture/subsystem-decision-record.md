---
title: Laomedo subsystem decision record
status: draft
kind: architecture
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Laomedo subsystem decision record

This records individual choices the user made while refining the
[subsystem handoffs](subsystem-handoffs.md), through 2026-10-02. These are
product design decisions, not claims that Langflow or Laomedo implements them.
The [earlier journey](user-traversal.md) predates some clarifications; the
decisions below identify those changes explicitly. Edge IDs refer to the
[editable handoff graph](subsystem-handoffs.drawio).

## Workflow setup and definitions

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D01 | Laomedo embeds a heavily modified Langflow editor and exposes all Langflow components. Langflow owns graph authoring and workflow sequencing. | H4-H7 |
| D02 | Single-agent execution also goes through Langflow as a one-agent workflow. Laomedo presents a simpler setup form for that path. | H4-H5 |
| D03 | Each configured agent stage has its own agent, prompt, model, effort, files and skills. Defaults ease creation by being copied into a stage; later default edits do not change existing stages. | H5 |
| D04 | A stage may receive both user-added files and artifacts from earlier stages through Langflow handoffs. | H5-H6 |
| D05 | Users may select, create or edit graph, prompt and skill variations through the UI or with chat-agent assistance. Editing a run configuration does not itself publish a library revision. | H3-H4 |
| D06 | Prompts and skills may be curated in native or GitHub-backed libraries by users and agents. GitHub publication uses a PR by default; direct branch editing is an explicit option. | H3 |

The term **stage** means one configured agent node in a workflow. An
**invocation** is one execution of that node, potentially spanning many
agent turns. A loop produces a new invocation of the same stage.

## Launch and version resolution

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D07 | A run may start from a GitHub issue, directly from a prompt, on a timer, or from a configured GitHub event: opening an issue, opening a PR, or a failed Actions workflow. | H1-H2 |
| D08 | Each timer or event hook selects a saved single-agent or Langflow configuration and supplies event context as run input. | H1-H4 |
| D09 | Saved configurations, prompts and skills use `latest` by default; the user may pin a revision. At launch, Laomedo resolves every selector to an exact revision and keeps it fixed for the run, including recovery. | H1-H5 |
| D10 | The agent reads current GitHub issue context and checks for related open PRs. If the run supplies a PR, the agent continues it. Otherwise it opens a new PR and reports a related existing PR at completion. | H2, H11-H12 |

## Workspaces, sessions and containers

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D11 | For a single agent or each workflow stage, the user can choose an existing local workspace or an isolated checkout. Execution occurs in Docker on the user's machine with the selected workspace mounted. The same approval policy applies to both choices; local execution warns that auto-approval reduces interruptions but retains risk. | H5 |
| D12 | Agent stages do not share containers. Each stage's container persists across its invocations until the workflow ends, then is removed automatically. Stages may mount a common external Codex home directory. | H5-H8 |
| D13 | Session persistence is user-assigned per stage: start a new session or reuse an existing one, including a session from another stage. Session data persists outside the container for recovery and telemetry. | H5, H8 |
| D14 | Predictable simultaneous use of one session causes a pre-launch warning, but launch remains possible. An actual concurrent attempt errors at execution time. | H5-H6 |

## Execution, recovery and inspection

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D15 | An errored invocation blocks dependent stages while independent branches continue by default. A user can select end-on-error before launch, or interrupt all active agents immediately through Stop. | H6-H7 |
| D16 | Closing Laomedo does not stop a workflow; the UI reconnects when reopened. | H7-H8 |
| D17 | Container crashes trigger automatic recovery, with a default of three recovery attempts per invocation. Recovery resumes the same agent session and sends a prompt to inspect existing state before repeating actions. After those attempts fail, the invocation is marked errored. | H5-H8 |
| D18 | The execution overview is separate from the Langflow graph. It shows agent invocations and their timing; a waterfall is a candidate layout, not a chosen one. Each loop invocation appears separately and opens its own telemetry when selected. | H7-H8 |
| D19 | Selective stage reruns using previous upstream outputs are desired, subject to verifying Langflow's capabilities. | Future H4-H6 command |

## Access and outcomes

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D20 | Agents work unattended within their containers. External tool integrations are added explicitly. Access requests follow auto-approval; if auto-approval is disabled or denies a request, the request escalates to the user. | H5-H8; approval interface open |
| D21 | An approved external access request resumes the same invocation and applies only to that run. A denied request, with optional user text from an “Other” field, returns to the agent so it can try another approach. | H5-H8; approval interface open |
| D22 | The chat assistant uses the same subsystem operations as the UI to configure and launch runs and guide navigation. Its actions also follow auto-approval; without approval it asks the user. | H1-H4; approval interface open |
| D23 | The agent directly creates or updates the GitHub PR. Laomedo retains and displays its reference. A follow-up run against that PR lets the user choose a new or existing session and hints to the agent that review comments exist. | H11-H12, H16 |
| D24 | The run record contains configuration, status, trace, summary and references to outputs. Produced code, specs and other artifacts may live in the workspace or another persistent destination. The summary identifies artifact type, location and saved/published state. | H9-H10, H13 |
| D25 | An unsuccessful run yields an editable semi-structured report. The user reviews it before publishing a follow-up issue; that issue can be run like any other issue. Findings are stored only when selected, with GitHub publication a separate action. | H13-H16 |

## Still open

- The authoritative persisted workflow state during UI closure and reconnection,
  and the reconciliation with the earlier
  [shared-contract wording](shared-contracts.md) about runner ownership.
- Langflow's actual support for selective stage reruns, durable reconnection,
  and artifact/file references across all component types.
- The transport, identity and user interaction for external access requests;
  decisions D20-D22 specify behavior but not an API.
- Artifact destination defaults, overrides, controls, retention and handling of
  unsaved outputs. No storage system has been chosen.
- The exact execution-overview layout and telemetry content/retention policy.
- Wire formats, field names, error taxonomies, and where each proposed
  subsystem boundary lands in the implementation.

These decisions are recorded here so later contracts can be drafted from them
without reopening settled product questions. They do not remove the need to
verify third-party capabilities or to review an implementation contract.
