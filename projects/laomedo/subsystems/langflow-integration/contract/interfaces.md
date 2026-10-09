---
title: Langflow integration interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration interfaces

The [interface map](../../README.md) identifies direct Laomedo contacts. The
embedded Langflow runtime is an external dependency: its actual hooks and
durability must be verified before this becomes an implementable API. A run is
distinct from a stage invocation and from a native agent session.

## Run entry and definition resolution — H1-H4

- **Consumes IF-01** from [issue integration](../../issue-integration/contract/interfaces.md)
  only when a real issue was selected. Direct prompts and timer/PR/Actions
  events bypass IF-01; the latter three require a future trigger service.
- **Consumes IF-02** from [prompt and skill library](../../prompt-skill-library/contract/interfaces.md):
  exact prompt/skill revision references. A saved workflow configuration uses
  `latest` by default or a user-pinned revision; all selectors are resolved at
  launch and frozen for the run. This does not promise crash recovery.
- **Offers to Langflow:** selected graph definition/revision or one-agent
  graph, resolved stage configurations, user files and event/direct inputs,
  Laomedo run identity and correlation context. The `RunLaunchContext` union
  below distinguishes prompt, issue, timer, PR and failed-workflow subjects.
- **Failure:** an unavailable selected revision, invalid stage configuration,
  inaccessible required input, or failure to durably record run/trace identity
  prevents dispatch and yields a visible launch error. It must not silently
  substitute another revision or run without trace identity.

## IF-05/IF-06 — agent-node invocation and return

Langflow sequencing invokes [agent execution](../../agent-execution/contract/interfaces.md)
through this adapter. The command carries run, graph revision, configured
stage and invocation identities; frozen provider/model/effort/prompt/skill
references; user and upstream file/artifact refs; session choice; and
workspace choice. A loop creates a new invocation identity for the same
stage. The outcome returns that invocation identity, status, output refs and
error classification to Langflow. The Langflow-specific mechanism for all
component types to exchange artifact refs is open.
For the first fresh Codex slice, the durable [runner correlation](runner-correlation.md)
binds the separate runner run ID and raw-event reference to the already
reserved invocation; a runner acknowledgement without that binding is not
a complete IF-06/07 handoff.

Predictable simultaneous use of one session is a pre-launch warning, not a
launch block for the later multi-stage design. Actual concurrent use errors
at invocation. The first slice has one agent, isolated checkout and fresh
session; cross-stage reuse and local mounts are not first-slice support.
Independent-branch continuation after an error and Stop/cancellation semantics
remain unverified Langflow capabilities, not guaranteed by this draft.

## IF-07 — workflow events to run traces

Send workflow start, stage/invocation lifecycle, completion, error and
interruption events to [run traces](../../run-traces/contract/interfaces.md).
Each event carries run, graph revision, stage and invocation correlation where
applicable, plus source event identity when Langflow provides it. Missing
native IDs are recorded as unknown rather than fabricated. Receipt order is
not a producer-stable deduplication key; IF-07 replay policy is open.
When the source is the local runner, include its namespaced run identity only
after the [binding](runner-correlation.md) is durable. Retain a pending or
uncertain observation when the acknowledgement is missing; never infer the
runner ID from timing.

## IF-09 — run context to results and artifacts

Before dispatch, durably supply [results and artifacts](../../results-artifacts/contract/interfaces.md)
the exact resolved configuration reference, run identity and graph revision.
At terminal state, supply workflow outcome and end time or an explicit
incomplete/unknown state. Results combines this context with IF-10 and IF-11;
it cannot reconstruct the exact launch selection solely from tool events.

## IF-13 — follow-up run context

Consume a user-requested follow-up from results: prior run identity, existing
PR reference when supplied, and explicit existing/new session selection.
Create a new linked run with separate invocation identities and trace. The
agent receives a hint that PR comments exist and fetches them itself. A
selective stage rerun using prior upstream outputs is desired but not part of
this interface until Langflow feasibility is verified. Existing-session mode
also remains deferred until the prior workspace basis, current PR head and
provider compatibility can be checked; first-slice follow-ups are fresh.

## PR-head check gate (target)

The [active-run PR decision](../../../decisions/0005-active-run-pr-feedback.md)
allows a graph to put a GitHub check gate after an agent invocation. Agent
execution first delivers the PR while its grant is live, reads it back, and
returns the exact repository, PR number and head SHA. The gate subscribes to
that **head**, not merely to a PR number or branch name. It waits for the
configured check set and either routes success forward or passes a bounded
failure result to a **new** agent invocation. The graph must show the wait,
failure and each invocation separately. An unresolved check, missing delivery
or exhausted loop budget yields an explicit incomplete/failed outcome under
a configured policy, never an inferred success.

An unresolved `unknown` push or PR effect from the prior invocation fences
automatic corrective dispatch. The gate records incomplete delivery until
read-only reconciliation and the existing Q16 resolution/approval rules
resolve that uncertainty; a new invocation or effect ID cannot bypass the
fence. A corrective invocation receives a newly authorized run grant bound
to the approved repository, branch and target PR. It cannot substitute a
new branch or PR merely to avoid the previous effect's state.

The approximate handoff is:

```text
PRHeadCheckRequest {
  run_id: string, graph_revision_ref: Ref, gate_id: string,
  prior_invocation_id: string, repository: Ref,
  pr: { number: integer, head_sha: string },
  required_checks_ref: Ref, loop_iteration: integer,
  max_iterations: integer, wait_deadline: timestamp
}
PRHeadCheckObservation {
  run_id: string, gate_id: string, repository: Ref,
  pr_number: integer, head_sha: string,
  source_delivery_id: string, source_check_id: string,
  observed_status: "pending" | "passed" | "failed" | "unknown",
  failure_artifact_ref?: Ref, observed_at: timestamp
}
```

The ingress boundary must authenticate and durably identify the external
delivery before it reaches Langflow. A redelivery for the same check identity
must not create another agent invocation. For one check identity, `pending`
may advance to its first final `passed` or `failed` result. A later matching
final delivery is a duplicate; a contradictory final result remains visible
as a conflict and cannot dispatch another invocation or replace the decision.
A genuine check rerun has a new source check identity; which rerun belongs
to the configured required check set remains part of check-selection design.
An `unknown` observation does not decide or dispatch; the gate waits until
a known final observation or its configured deadline. A matching observation
recorded before the gate began waiting must be considered when the gate
starts, subject to these same identity and conflict rules. A result for an old
head SHA cannot decide the current head. A corrective commit creates a new
head/check wait and consumes another configured loop iteration. Agent-caused
events must not trigger unbounded new runs. The ingress/process owner,
check-set semantics and stable-delivery source are still open decisions.
Stop while a gate waits ends that wait and prevents a later observation from
dispatching another agent invocation in the stopped run.

This is an **in-run** external-event gate, distinct from `RunLaunchContext`'s
future PR-opened or failed-workflow launch variants. A fate-shared backend
crash still ends the graph run; an event received afterwards cannot resume it.
Whether pinned Langflow can wait, correlate and route these events within one
live graph is unverified and belongs to the bounded [#123 experiment](https://github.com/amadou-6e/laomedo/issues/123).
Until that evidence exists, this is a target interface, not a supported
Langflow component or a promise of CI-driven automatic repair.

## Run-state ownership and open gates

Langflow owns live graph sequencing. Laomedo's Langflow integration owns the
durable run identity/status record, frozen launch context and restart sweep;
it is **not** a second graph scheduler. A fate-shared Langflow/Laomedo backend
crash ends the run and leaves partial or unknown evidence. Closing only the
UI does not end a live backend run. The restart sweep cannot by itself stop
an independently surviving, writable agent container during the outage; its
bounded orphan-stop owner and test remain open. Stable flow snapshots (flow
JSON plus component-code identity) must be resolved and run, not just hashed;
that mechanism is unverified. Timer/event ownership, approval expiry, Stop
fencing and run-level budget remain later design gates.

## Approximate payloads

See the [shared notation](../../README.md#payload-sketch-conventions).
IF-05/IF-06 reuse the agent-execution [stage invocation](../../agent-execution/contract/schemas/if-05-stage-invocation.md)
and [invocation outcome](../../agent-execution/contract/schemas/if-06-invocation-outcome.md)
sketches rather than defining a second command format here. IF-01/IF-02 are
defined by their providers.

```text
RunLaunchContext =
  { kind: "prompt", prompt_input_ref: Ref }
  | { kind: "selected_issue", issue_context_ref: Ref }
  | { kind: "issue_opened", issue_context_ref: Ref,
      delivery_id: string }
  | { kind: "timer", schedule_id: string, slot_id: string,
      delivery_id: string }
  | { kind: "pr_opened", repository: Ref, pr: { number: integer,
      url: string, head_sha: string }, delivery_id: string }
  | { kind: "workflow_failed", repository: Ref,
      workflow_run: { id: string, name: string, head_sha: string,
                      ref: string, url: string }, delivery_id: string }

IF-07 WorkflowEvent {
  run_id: string, graph_revision_ref: Ref, stage_id?: string,
  invocation_id?: string, source_event_id?: string,
  runner_run_id?: string,
  transition: "run_started" | "stage_ready" | "invocation_started"
            | "invocation_completed" | "invocation_failed"
            | "run_completed" | "run_failed" | "run_interrupted"
            | "run_crashed",
  observed_at?: timestamp,
  detail_ref?: Ref
}

IF-09 RunContext {
  run_id: string, graph: { definition_id: string, revision_ref: Ref },
  launch: RunLaunchContext,
  resolved_config_ref: Ref, resolved_config_hash: string,
  started_at: timestamp,
  terminal?: { status: "completed" | "failed" | "interrupted"
                    | "crashed" | "incomplete", ended_at?: timestamp,
               reason?: string }
}

IF-13 FollowUpRunRequest {
  prior_run_id: string, target_pr?: { repository: Ref, number: integer, url: string },
  sessions: [{ stage_id: string, mode: "new" | "existing",
               native_session_ref?: Ref,
               workspace_basis?: { pr_head_sha: string,
                                    post_run_workspace_ref: Ref } }],
  requested_by: Ref, configuration_ref: Ref,
  reviewer_comment_hint: boolean
}
IF-13 FollowUpRunCreated {
  prior_run_id: string, new_run_id: string, target_pr?: Ref
}
```

The `RunLaunchContext` variants are alternatives, not optional fields on an
issue. Only `selected_issue` invokes IF-01 in the first slice. Issue-opened,
timer, PR-opened and workflow-failed launch are future variants whose trigger-service owner,
deduplication and event feedback-loop guard are unresolved. `delivery_id`
must be stable for redelivery but its producer and enforcement remain open.
IF-09 is persisted before dispatch with `terminal` absent and updated with a
terminal or explicitly incomplete state; it is not reconstructed from IF-07 alone.
For a native runner wait deadline, IF-09 emits `status: "incomplete"` and
`reason: "runner_result_pending"`. The reason identifies this timeout layer;
it is not proof that the native run stopped. Results preserves that reason
without inventing a completed or failed native outcome.
IF-13 makes the choice per agent stage: `native_session_ref` is required for
`existing` and absent for `new`. The later `existing` mode also requires a
checked `workspace_basis`; it is not first-slice support.
The hint tells the agent to inspect PR comments; it does not copy potentially
stale comments into the run. Langflow transport and safe flow-snapshot
execution remain unverified. Run traces assigns IF-07 receipt time and sequence
on ingest, but that sequence cannot deduplicate a redelivered event. The
producer-stable key policy remains open; absent source IDs are not fabricated.
