---
title: Laomedo subsystem handoff decisions
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Laomedo subsystem handoff decisions

## Status and sources

This is a **reconstructed discussion record**, not a verbatim chat log. It
records individual choices the user made while refining the
[subsystem handoffs](../architecture/subsystem-handoffs.md), through
2026-10-02. The [earlier journey](0001-issue-to-agent-journey.md) predates
some clarifications; the decisions below identify those changes explicitly.
Edge IDs refer to the
[editable handoff graph](../architecture/subsystem-handoffs.drawio). Exact
message timestamps and unrecorded wording are not available in the repository.
This record remains draft pending user review. It specifies desired product
behavior, not proof that Langflow or Laomedo implements it.
The inspected handoff graph history is pinned to specs commit
`7cd26f6da454f4da8b325b2a3b526b9f5c724e76` (last change to that diagram
before this record).

## Discussion trail

The discussion began by rejecting two proposed subsystem boundaries:
workspace management was folded into agent execution, and workflow authoring
and sequencing were assigned to Langflow. A separate PR-delivery subsystem was
also unnecessary because the agent writes the PR directly; Laomedo needs the
PR reference for results and follow-up. The user then asked how the single-agent
form and Langflow choice cross subsystem boundaries, and requested the
[handoff graph](../architecture/subsystem-handoffs.drawio).

The follow-up interview proceeded from graph setup to stage defaults and
inputs; failure, loops and telemetry; external approvals and recovery; local
Docker workspaces and session persistence; and finally launch triggers,
version selectors and PR continuation. Questions about state machines were
explicitly redirected to their purpose: defining information exchanged at
subsystem interfaces. The numbered choices below preserve the resulting
answers. They are grouped by concern rather than presented as exact message
order, and do not imply that unanswered mechanism questions were settled.

## Workflow setup and definitions

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D01 | Laomedo embeds a heavily modified Langflow editor and exposes all Langflow components. Langflow owns graph authoring, workflow sequencing and live run state. A Langflow process restart or crash ends the run; Laomedo does not resume an in-flight workflow. The safety/observability implications of exposing every component remain contested. | H4-H7 |
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
| D09 | Saved configurations, prompts and skills use `latest` by default; the user may pin a revision. At launch, Laomedo resolves every selector to an exact revision and keeps it fixed throughout the run. Any later recovery design must preserve these frozen revisions; first-slice crash recovery is not implied. | H1-H5 |
| D10 | The agent reads current GitHub issue context and checks for related open PRs. If the run supplies a PR, the agent continues it. Otherwise it opens a new PR and reports a related existing PR at completion. | H2, H11-H12 |

## Workspaces, sessions and containers

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D11 | For a single agent or each workflow stage, the user can choose an existing local workspace or an isolated checkout. Execution occurs in Docker on the user's machine with the selected workspace mounted. The stage checkout is writable so the agent can edit, commit, push and open a PR; runner, skill and unrelated host paths require separate protection. The same approval policy applies to both workspace choices; local execution warns that auto-approval reduces interruptions but retains risk. | H5 |
| D12 | Agent stages do not share containers. Each stage's container persists across its invocations until the workflow ends, then is removed automatically. Stages may mount a common external Codex home directory. | H5-H8 |
| D13 | Session persistence is user-assigned per stage: start a new session or reuse an existing one, including a session from another stage. Session data persists outside the container for telemetry and possible later recovery; persistence alone does not establish that a crashed turn can resume. Cross-stage reuse is outside the first slice. | H5, H8 |
| D14 | Predictable simultaneous use of one session causes a pre-launch warning, but launch remains possible. An actual concurrent attempt errors at execution time. | H5-H6 |

## Execution, recovery and inspection

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D15 | An errored invocation blocks dependent stages while independent branches continue by default. A user can select end-on-error before launch, or interrupt all active agents immediately through Stop. | H6-H7 |
| D16 | Closing only the Laomedo UI does not stop a workflow while Langflow remains running; the UI reconnects when reopened. A Langflow restart or crash ends the run, not a transparent workflow recovery. How the UI reports that terminal loss remains open. | H7-H8 |
| D17 | The interview proposed automatic recovery after an agent-stage container crash while Langflow remains running: up to three attempts, using the same native session and a prompt to inspect existing state. **This is a deferred target, not first-slice behavior.** In the first slice, a mid-turn container crash terminates that invocation with incomplete/unknown evidence; it is not automatically restarted. Before specifying recovery, run a bounded experiment that interrupts a real agent mid-turn, restarts it from the persisted session, and checks what it resumes, repeats or loses, including external effects. A prompt to inspect state alone does not prove safe recovery. A fate-shared Langflow/Laomedo backend crash ends the whole run under D01/D16. | H5-H8 |
| D18 | The execution overview is separate from the Langflow graph. It shows agent invocations and their timing; a waterfall is a candidate layout, not a chosen one. Each loop invocation appears separately and opens its own telemetry when selected. | H7-H8 |
| D19 | Selective stage reruns using previous upstream outputs are desired, subject to verifying Langflow's capabilities. | Future H4-H6 command |

For the first single-agent slice, Laomedo must durably establish the run and
trace identity before dispatch. If it cannot, it refuses dispatch rather than
starting an untraceable agent. This is a confirmed launch rule, not evidence
that the persistence boundary has been implemented or tested. A backend crash
terminates the run; a stage-container crash terminates its invocation without
automatic same-session recovery. Both retain partial or unknown evidence
instead of reporting that no work occurred. The bounded restart experiment
needed to revisit D17 is tracked in the
[agent-execution readiness draft on PR #182](https://github.com/amadou-6e/specs/pull/182);
its protocol and outcome are not yet established.

## Access and outcomes

| ID | Decision | Handoff affected |
| --- | --- | --- |
| D20 | Agents work unattended within their containers. External tool integrations are added explicitly. Access requests follow auto-approval; if auto-approval is disabled or denies a request, the request escalates to the user. | H5-H8; approval interface open |
| D21 | An approved external access request resumes the same invocation and applies only to that run. A denied request, with optional user text from an “Other” field, returns to the agent so it can try another approach. | H5-H8; approval interface open |
| D22 | The chat assistant uses the same subsystem operations as the UI to configure and launch runs and guide navigation. Its actions also follow auto-approval; without approval it asks the user. | H1-H4; approval interface open |
| D23 | The agent directly creates or updates the GitHub PR. Laomedo retains and displays its reference. A follow-up run against that PR lets the user choose a new or existing session and hints to the agent that review comments exist. | H11-H12, H16 |
| D24 | The run record contains configuration, status, trace, summary and references to outputs. Produced code, specs and other artifacts may live in the workspace or another persistent destination. The summary identifies artifact type, location and saved/published state. | H9-H10, H13 |
| D25 | An unsuccessful run yields an editable semi-structured report. The user reviews it before publishing a follow-up issue; that issue can be run like any other issue. Findings are stored only when selected, with GitHub publication a separate action. | H13-H16 |

## Contested choices and capability dependencies

These rows preserve what was chosen during the interview; they are **not
cleared for implementation** merely because a choice was recorded. The
[systems-design review on PR #172](https://github.com/amadou-6e/specs/pull/172)
challenged the following decisions. The user's subsequent clarification settles
one boundary: Langflow owns live run state, and its restart or crash terminates
the run. A separate Laomedo ledger for resuming the workflow is **not** part of
this design. Persisted trace and result records may describe a terminated run;
they do not reconstitute its execution.

| Decisions | Reconsider before implementation |
| --- | --- |
| D01, D16 | How terminal Langflow loss is detected and reported; whether UI reconnection works while Langflow itself remains alive; how non-agent Langflow components fit approval and telemetry. Do not promise run recovery across Langflow restart. |
| D07, D08 | Timer/event-service ownership, duplicate suppression, catch-up behavior, per-configuration concurrency and an event feedback-loop guard. |
| D11, D12, D14 | Writer exclusion when parallel or unattended stages mount the same local checkout; whether direct local mounts should be restricted or isolated checkouts required. |
| D13, D23 | Cross-stage session dependencies and workspace compatibility; the source workspace and current PR head for an existing-session follow-up after its previous container is removed. |
| D15 | Whether Langflow can continue independent branches after a stage error, enforce loop limits, and prevent new dispatch after Stop. The pilot's node raises on error; desired default behavior is not verified. |
| D17 | Deferred pending a controlled real-agent mid-turn crash/session-restart experiment. Observe restored session state, repeated or lost actions, trace continuity and external effects before choosing a recovery protocol or retry count. A state-check prompt alone is not a guarantee. |
| D20, D21, D22 | Who holds approval requests, their expiry/default for unattended runs, and whether non-agent components can bypass the same controls. |
| D10, D23, D25 | Which stage may create/update the run's PR, how its reference is collected, and who produces a failure report when the agent cannot. |

Unverified third-party or adapter capabilities affect D01 (all components),
D04 (file/artifact handoffs), D15 (branch failure and Stop semantics), D16
(reconnection to a live Langflow run), D17 (mid-turn native-session resume),
D19 (selective stage rerun), and D23 (native-session resume after workspace or
PR-head changes). D09 additionally requires a tested way to snapshot and run
the exact Langflow flow and component code selected at launch. None of these
capabilities was established by the spec validator or this documentation PR.

## Still open

- The owner and runtime policy for timer/GitHub-event ingestion, duplicate
  suppression, feedback-loop prevention, and runs triggered while the UI is
  closed. This is separate from Langflow's ownership of an active run.
- How a Langflow crash is detected and represented as a terminal run result,
  including partial traces and orphaned agent-stage containers. There is no
  plan here to resume the graph after Langflow restarts.
- How a crashed stage container can safely resume its native session mid-turn
  remains outside the first slice until the controlled restart experiment
  establishes what the provider actually resumes, repeats or loses.
- Langflow's actual support for selective stage reruns, UI reconnection while
  Langflow remains live, branch-local failure, conditional loops, cancellation,
  exact flow snapshots, and artifact/file references across component types.
- The owner and transport for inter-stage files between separate containers,
  including materialization into the receiving workspace and retention after
  containers are removed.
- The approval-request owner, identity, expiry and unattended default; decisions
  D20-D22 state desired behavior but not an API.
- The writer-exclusion rule for shared local workspaces and the dependency and
  compatibility rules for shared or resumed native agent sessions.
- The owner of one target PR in multi-stage runs, discovery of its current head,
  and idempotence for PR creation in any later agent-container recovery design.
- The producer of failure reports when no agent result exists, plus the owner
  and enforcement point for a run-level budget across stages, loops and retries.
- Artifact destination defaults, overrides, controls, retention and handling of
  unsaved outputs. No storage system has been chosen.
- The exact execution-overview layout and telemetry content/retention policy.
- Wire formats, field names, error taxonomies, and where each proposed
  subsystem boundary lands in the implementation.

These records preserve the interview, including choices now contested by the
systems review. Reopen those choices before freezing dependent contracts; do
not silently treat a recorded preference as an implemented or verified guarantee.
