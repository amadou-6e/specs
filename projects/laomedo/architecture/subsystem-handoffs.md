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
marks user review. Dashed yellow nodes and edges mark later paths whose owner
or mechanism remains open; they are not working services. Colors indicate
documentation maturity, not process placement. Langflow owns workflow
definitions, sequencing and live run state. If the fate-shared Langflow/Laomedo
backend restarts or crashes mid-run, that run ends; this graph does not specify
transparent workflow recovery. Laomedo's Langflow integration owns a durable
run identity/status record and restart accounting, **not** a second graph
scheduler. It launches and correlates runs; agent execution owns provider
dispatch, session and workspace binding, and stage containers. Run traces own
stored events and projections. Results own summaries and artifact references;
produced files need not live in a run directory.

The first slice is one agent, launched by direct prompt or selected issue, with
an isolated writable checkout and fresh session. It must refuse dispatch if
the durable run/trace identity cannot be established. Timer/event triggers,
approval brokerage, inter-stage file transport, shared workspaces, session
reuse and automatic mid-turn crash recovery are **not** established by this
diagram. The dashed nodes expose their missing owners instead of representing
them as first-slice capabilities. No real-agent crash experiment was run here.

## Edge inventory

| Edge | Producer → consumer | Kind and minimum payload |
| --- | --- | --- |
| H1 | Direct request → Langflow integration | Command: direct prompt or selected-issue trigger, saved configuration reference and version selector, input and optional issue reference. `latest` is the default selector; an exact version is optional. Timer/GitHub-event ingestion is a later path with no selected service owner, deduplication or loop guard yet. |
| H2 | Issue integration → Langflow integration | Reference: selected issue identity and repository; the agent reads current GitHub content and checks for open PRs. |
| H3 | Prompt and skill library → Langflow integration | Reference: exact configuration, prompt and skill revisions resolved at run start, including those selected through `latest`. They stay fixed through the run. Any later recovery design must reuse them; first-slice crash recovery is deferred. |
| H4 | Laomedo Langflow integration → Langflow runtime | Command: selected graph revision or single-agent graph, run input, Laomedo run identity and correlation context. The integration must durably record identity and frozen selection before dispatch; failed persistence refuses dispatch. This is not graph reattachment after backend death. |
| H5 | Langflow runtime → Agent execution | Command: stage and invocation identities, agent configuration, input and user-file references, workspace and session selection. Each invocation may span many turns; a loop creates another invocation. Upstream artifact bytes across stage containers, local-mount exclusion, cross-stage session binding and retry identity remain unresolved; their absence must not be disguised as supported handoffs. |
| H6 | Agent execution → Langflow runtime | Outcome: invocation identity, terminal status, output/artifact references or error. Independent-branch continuation after an errored node, Stop/dispatch ordering and long-call cancellation depend on **unverified Langflow behavior**; the pilot node raises on error. A crashed first-slice invocation is not automatically restarted. |
| H7 | Langflow runtime → Run traces | Event: workflow and invocation lifecycle/status with run, stage and invocation identities. Stable source-event identity and deduplication across redelivery remain unverified; a trace is not resumable graph state. |
| H8 | Agent execution → Run traces | Event: agent telemetry and native session identity correlated to invocation and run. Repeated invocations remain separately inspectable. |
| H9 | Agent execution → Results and artifacts | Reference: produced artifact type, location and available saved/published state; no assumption that files are inside the run record. |
| H10 | Run traces → Results and artifacts | Reference: trace and digest location plus correlation identity for the completed or stopped run. |
| H11 | Agent execution → GitHub | External write: create or update a PR. In the first one-agent path, a supplied PR reference means continue it; otherwise the agent opens a new PR and reports related open PRs. Multi-stage target-PR ownership and replay-safe write identity remain open. |
| H12 | Agent execution → Results and artifacts | Reference: PR identity observed from the agent outcome. GitHub review context needs an explicit fetch/poll owner; GitHub is not assumed to push it to a local results service. |
| H13 | Results and artifacts → User review | Read model: run summary, status, trace/digest links, PR reference and artifact inventory. |
| H14 | User review → Issue integration | Command: reviewed and edited failure-to-issue proposal; publication is a separate user action. |
| H15 | Issue integration → GitHub | External write: publish the reviewed follow-up issue. |
| H16 | User review → Run entry | Command: requested follow-up run and existing PR reference. Existing-session reuse and its workspace/PR-head basis are later work; first-slice follow-ups use a fresh session. The agent receives a hint about PR comments and retrieves them itself. |

The exact field names and serialization are open. At minimum, the handoffs need
stable run, workflow-definition, stage, invocation, session, trace and artifact
identities where applicable. The run records the exact resolved revisions so a
later change to `latest` does not silently alter an active run.

The [individual decision record](../decisions/0002-subsystem-handoffs.md) preserves the
user's choices behind these edges, including editor scope, copied defaults,
container and session lifetime, recovery, approvals and PR behavior. This edge
inventory stays focused on information crossing subsystem boundaries.

## Interface decisions still needed

1. Define how the UI reconnects to a run while Langflow remains live, and how
   a Langflow restart/crash is detected and reported as a terminal run with
   partial evidence. The durable record is owned by Langflow integration but
   does not schedule or resume graph nodes. A surviving writable stage container
   also needs a bounded orphan-stop mechanism. The [shared contracts](shared-contracts.md) assign
   agent-invocation execution and session persistence to the runner, not
   workflow-state recovery.
2. Select the owner of a timer/GitHub-event service before enabling that path.
   It needs unattended operation, delivery/slot deduplication, concurrency and
   feedback-loop rules; none is supplied by H1's direct-request producer.
3. Select the owner of an approval broker before unattended escalation. Define
   persisted request identity, expiry, default on unattended timeout and the
   same-invocation grant handoff; no owner is selected in this diagram.
4. Select the durable byte owner and materialization boundary for files passed
   between separate stage containers. Then verify reference transport across
   relevant Langflow components; the current H5 reference alone moves no bytes.
5. Resolve H5/H6/H7's unverified execution semantics: writer exclusion on
   local mounts, symbolic cross-stage session dependencies, stable event keys,
   independent branch failure, Stop/dispatch races and cancellation. First-slice
   scoping avoids some of these but does not prove the later behavior.
6. Define a single target-PR owner for multi-stage runs, a review-context fetch
   owner for H12, and the workspace/PR-head basis for H16 existing-session
   follow-ups. Prompting the agent to inspect GitHub is not write idempotency.
7. Verify Langflow's selective-stage-rerun and reconnection capabilities before
   adding those commands to the interface inventory. Desired behavior alone is
   not evidence of support.

This graph does not turn workspace management or PR delivery into separate
subsystems. Chat-assisted navigation and configuration use the same subsystem
operations as the UI. The agent creates and updates PRs directly through GitHub.
