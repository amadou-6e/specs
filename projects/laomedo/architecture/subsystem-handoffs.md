---
title: Proposed subsystem handoffs
status: draft
kind: architecture
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Proposed subsystem handoffs

The [editable Draw.io graph](subsystem-handoffs.drawio) has two pages: launch and
execution, then outputs and follow-up. The numbered arrows below describe the
minimum information passed between boundaries. The diagram is a proposed
architecture derived from the [user traversal](user-traversal.md) and subsequent
2026-10-02 design discussion. It is neither implemented behavior nor a reviewed
wire protocol. The [launch](subsystem-handoffs-launch.mmd) and
[follow-up](subsystem-handoffs-followup.mmd) Mermaid files are generation
provenance; edit the Draw.io source for reviewed geometry changes.
Arrow IDs `H1`–`H16` resolve to the edge inventory below; short IDs keep the
rendered graph legible.

Blue nodes are proposed Laomedo boundaries, green nodes have existing draft
subsystem contracts, and orange nodes are external inputs or systems. Purple
marks user review. Colors indicate documentation maturity, not process
placement. Langflow owns workflow definitions and sequencing. Laomedo's
Langflow integration launches and correlates runs; agent execution owns provider
dispatch, session and workspace binding, and stage containers. Run traces own
stored events and projections. Results own summaries and artifact references;
produced files need not live in a run directory.

## Edge inventory

| Edge | Producer → consumer | Kind and minimum payload |
| --- | --- | --- |
| H1 | Direct request, timer or GitHub event → Langflow integration | Command: trigger type, saved configuration reference and version selector, input, event reference where applicable. `latest` is the default selector; an exact version is optional. |
| H2 | Issue integration → Langflow integration | Reference: selected issue identity and repository; the agent reads current GitHub content and checks for open PRs. |
| H3 | Prompt and skill library → Langflow integration | Reference: exact configuration, prompt and skill revisions resolved at run start, including those selected through `latest`. They stay fixed through the run and its recovery attempts. |
| H4 | Laomedo Langflow integration → Langflow runtime | Command: selected graph revision or single-agent graph, run input, Laomedo run identity and correlation context. |
| H5 | Langflow runtime → Agent execution | Command: stage and invocation identities, agent configuration, input and file/artifact references, workspace and session selection. Each invocation may span many turns; a loop creates another invocation. |
| H6 | Agent execution → Langflow runtime | Outcome: invocation identity, status, output/artifact references or error. An errored invocation blocks dependent stages; independent branches continue unless the configured end-on-error setting stops them. |
| H7 | Langflow runtime → Run traces | Event: workflow and invocation lifecycle/status with run, stage and invocation identities. |
| H8 | Agent execution → Run traces | Event: agent telemetry and native session identity correlated to invocation and run. Repeated invocations remain separately inspectable. |
| H9 | Agent execution → Results and artifacts | Reference: produced artifact type, location and available saved/published state; no assumption that files are inside the run record. |
| H10 | Run traces → Results and artifacts | Reference: trace and digest location plus correlation identity for the completed or stopped run. |
| H11 | Agent execution → GitHub | External write: create or update a PR. A supplied PR reference means continue that PR; otherwise the agent opens a new PR and reports any related open PR it found. |
| H12 | GitHub → Results and artifacts | Reference: created or updated PR identity and review context. |
| H13 | Results and artifacts → User review | Read model: run summary, status, trace/digest links, PR reference and artifact inventory. |
| H14 | User review → Issue integration | Command: reviewed and edited failure-to-issue proposal; publication is a separate user action. |
| H15 | Issue integration → GitHub | External write: publish the reviewed follow-up issue. |
| H16 | User review → Run entry | Command: requested follow-up run, existing PR reference and explicit existing/new session choice. The agent receives a hint about PR comments and retrieves them itself. |

The exact field names and serialization are open. At minimum, the handoffs need
stable run, workflow-definition, stage, invocation, session, trace and artifact
identities where applicable. The run records the exact resolved revisions so a
later change to `latest` does not silently alter an active run.

## Interface decisions still needed

1. Decide which persisted workflow state is authoritative while Laomedo is
   closed. Langflow performs sequencing, but the existing
   [shared contracts](shared-contracts.md) still assign broad execution ownership
   to a Laomedo runner. Reconcile those words before freezing H4, H6 and H7.
2. Verify how all Langflow component types can exchange file and artifact
   references with agent stages. The required handoff is known; the actual
   component/API mechanism is not yet established.
3. Specify the cross-cutting external integration approval handoff. Run-scoped
   grants, auto-approval, user escalation and denial text are confirmed design
   intent, but their transport and identity are not defined in this graph.
4. Verify Langflow's selective-stage-rerun and reconnection capabilities before
   adding those commands to the interface inventory. Desired behavior alone is
   not evidence of support.

This graph does not turn workspace management or PR delivery into separate
subsystems. Chat-assisted navigation and configuration use the same subsystem
operations as the UI. The agent creates and updates PRs directly through GitHub.
