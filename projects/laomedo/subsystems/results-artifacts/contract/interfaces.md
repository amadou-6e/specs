---
title: Results and artifacts interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results and artifacts interfaces

Results combine three inputs by run identity. A missing input is recorded as
missing or incomplete, not fabricated from another source. Exact field names
and storage destinations remain open. See the [interface map](../../README.md).

## IF-09/IF-10/IF-11 — assemble a run result

| Provider | Minimum input | Result responsibility |
| --- | --- | --- |
| [Langflow integration](../../langflow-integration/contract/interfaces.md) (IF-09) | Run identity, exact launch configuration/graph revision, terminal or incomplete workflow status | Preserve what was requested and whether the workflow finished |
| [Agent execution](../../agent-execution/contract/interfaces.md) (IF-10) | Invocation identity, final/partial output refs, artifact type/location and known saved/published state, PR reference when produced | Inventory outputs without assuming they are co-located with run storage |
| [Run traces](../../run-traces/contract/interfaces.md) (IF-11) | Trace and digest refs, event completeness and correlation identity | Link inspection evidence without copying raw events into the summary |

The result exposed to the user carries status, a semi-structured summary,
trace/digest links, artifact inventory, and PR reference if known. A terminal
workflow may still have partial or unknown artifacts. An agent-created PR is
recorded as an external GitHub reference; this subsystem does not perform the
PR write or infer that a PR exists from a local diff.

**Contested/unverified:** the payload below does not yet represent the
confirmed fate-shared `crashed` state; IF-09's producer enum also lacks it.
Manifest supersession, artifact retention, effects absent from IF-10, and
report provenance have unresolved choices and tests. See
[decision readiness](../design/decision-readiness.md#question-triage); do not
interpret the current enum or summary as complete crash behavior.

## IF-12 — reviewed failure-to-issue proposal

For an unsuccessful run, expose an editable report of completed work, failure,
evidence and remaining work. A user selects, reviews and may edit a proposed
follow-up issue. Only then send that reviewed proposal and prior-run references
to [issue integration](../../issue-integration/contract/interfaces.md). If
publication fails, keep the draft's review state and report the failure.
Exact draft retention and duplicate-write handling remain open with issue
integration; see [decision readiness](../design/decision-readiness.md#choices-requiring-user-decision).

## IF-13 — follow-up run context

When the user requests another run, give
[Langflow integration](../../langflow-integration/contract/interfaces.md) the
prior run link, existing PR reference if supplied, and the user's explicit
existing/new session choice. The next run gets its own run and trace identities
while retaining links to the PR and previous run.

For the first slice, only a new session is proposed. Existing-session
follow-up and selective stage reruns remain deferred in
[decision readiness](../design/decision-readiness.md#question-triage).

Selected findings may be stored separately as durable project knowledge with
source/run links. This is optional and does not imply GitHub publication.
Artifact placement, ownership, retention and unsaved-output behavior await the
[later experiment](../../../architecture/user-traversal.md#boundaries-and-open-choices).

## Approximate payloads

IF-09 and IF-11 use the producer sketches in
[Langflow integration](../../langflow-integration/contract/interfaces.md#approximate-payloads)
and [run traces](../../run-traces/contract/interfaces.md#approximate-payload).
The assembled result and downstream handoffs are approximately (see
[notation](../../README.md#payload-sketch-conventions)):

```text
RunResult {
  run_id: string, context: RunContext, trace?: TraceLink,
  output_manifests: OutputManifest[],
  summary: { status: "completed" | "failed" | "interrupted" | "incomplete",
             completed_work: string[], findings: string[],
             failure?: string, remaining_work: string[] },
  target_pr?: Ref, missing_inputs: string[]
}

IF-12 ReviewedIssueProposal = Issue integration's IF-12 payload
IF-13 FollowUpRunRequest = Langflow integration's IF-13 payload
```

IF-10's shape is in the agent-execution
[per-exchange file](../../agent-execution/contract/schemas/if-10-output-manifest.md).
`RunResult` is a user-facing assembled projection, not an extra direct
subsystem edge. `missing_inputs` makes partial assembly visible. IF-12 and
IF-13 are defined once at their receiving boundaries to avoid diverging
copies; this subsystem produces those same shapes after user review/selection.
