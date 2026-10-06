---
title: Work Graph contract
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Work Graph

Status: proposed for [issue #151](https://github.com/amadou-6e/specs/issues/151).

Work Graph is Laomedo's capability for inspecting repository work and its
dependencies, then handing selected work to agent runs. The initial slice
imports and inspects work. Execution follows the existing
[component contracts](../../agent-execution/contract/README.md) and
[local pilot gates](../../../research/runner-feasibility/README.md).

This page defines data and execution contracts. View geometry, controls,
interaction states, and transitions require a reviewed Draw.io specification
under `subsystems/work-graph/design/ui/` before UI implementation.

## Graphs and ownership

The work graph describes tasks and prerequisites. A Langflow definition graph
describes the agent steps used to carry out a task. A run trace records what
actually happened. These graphs have linked identities and separate owners.
Work Graph may reference a versioned flow definition; the runner owns sessions,
execution and workspace snapshots, and monitoring owns raw events and their
projections.

The Issue Atlas fork is an implementation reference for GitHub ingestion,
filtering and graph rendering. The existing preview combines changes from
[PR #2](https://github.com/amadou-6e/github-issue-dag-viewer/pull/2),
[PR #4](https://github.com/amadou-6e/github-issue-dag-viewer/pull/4), and
[PR #6](https://github.com/amadou-6e/github-issue-dag-viewer/pull/6).
They need a scoped reuse decision before entering Laomedo, including the
Libavoid dependency license and its worker boundary. The prototype's graph
layout supplies no scheduling or authorization policy.

## Source and snapshot records

| Record | Required meaning |
| --- | --- |
| `WorkItemRef` | Provider, stable provider item ID, repository/project identity and source URL |
| `WorkItemSnapshot` | Immutable fetched title, body or body ref, labels, source state, update marker and provenance |
| `WorkDependency` | Prerequisite and dependent refs, relationship type, source evidence and resolution status |
| `WorkGraphSnapshot` | Immutable item and edge refs, fetch time, connector and projection versions, completeness and freshness metadata |
| `WorkRunBinding` | Work and graph snapshot refs, frozen input ref, definition revision where used, Laomedo run ID and earlier-run ref where applicable |

For GitHub, preserve the stable issue ID alongside `owner/repo#number` and
URL. Cross-repository edges retain both endpoints. An inaccessible endpoint
remains unresolved; a failed or partial fetch is recorded explicitly.
Refreshing creates a new graph snapshot and preserves snapshots referenced
by earlier runs.

For the first connector, native GitHub blocker relationships are authoritative.
References in issue text are contextual links unless a later reviewed
connector policy assigns them dependency meaning. Record evidence and
provenance for every edge. Inferred relationships cannot establish readiness.

Source ticket state, graph readiness and agent execution state remain separate
fields. A closed issue is source evidence, not proof of an agent's result.
Completed agent execution does not satisfy a dependent task's acceptance
criteria or change the source issue automatically. Cycles and unresolved
prerequisites prevent automatic readiness; filter and layout choices cannot
change that decision.

Filtering derives an inspection projection from the complete snapshot.
Matching items remain part of that projection even when they have no matching
neighbors. A linked-only projection records its omission policy and counts
separately. Dependency checks always use the source graph, including hidden
or unresolved prerequisites. This prevents a state or label filter from making
blocked work appear runnable.

## Binding work to execution

Before dispatch, freeze the selected work and graph snapshots, task/input,
source workspace, skill revision, definition revision where applicable,
provider, model/effort, permission grant and limits. These become a valid
`AgentRunSpec`; allocation and retention of the run ID follow the shared
runner contract. Validate freshness and prerequisite evidence again at
dispatch. If the source changed, require an explicit choice of the pinned or
refreshed snapshot, recorded in the binding.

The launch adapter re-fetches through the read-only source connector inside
the launch operation; a caller-supplied earlier `current` snapshot is not a
freshness check. For launch-time comparison, hash the selected work and its
transitive prerequisites, including item update/body markers and native dependency
edges. The fetch timestamp is excluded: a re-fetch of unchanged content
does not require a new choice merely because the snapshot ID changed.
When content changes, `pinned` keeps the selected earlier work, graph and
input while checking eligibility on the complete current graph;
`refreshed` binds current work, graph and input. Persist both the bound graph
snapshot ID and the current authorization graph snapshot ID, their relevant
content digests and the explicit choice. This makes a pinned run's different
input and authorization graphs reconstructible.

Graph readiness is an input to dispatch eligibility. Eligibility also requires
a valid run definition, supported runner settings, a recorded grant and
explicit operator authorization. Any prerequisite override must identify
the affected edge and rationale. Automatic scheduling is a later policy
decision; selecting a node does not authorize execution.

The launch adapter refuses missing or incomplete current source, unavailable
selected work, unresolved/cyclic prerequisites, and an open blocker before
reservation. An override applies only to the exact known open edge with a
nonempty rationale; multiple or unknown open edges cannot be collapsed into
one override. A trusted grant authority must verify the grant reference,
operator authorization, selected work, bound graph, runner, stage scope,
expiry and effective limits before reservation. A self-asserted grant in
the request is insufficient. Keep secrets out of the persisted binding.

For a bounded single-user, zero-turn check, the host may issue one-use grants
from a private ledger outside Git and every stage mount. Its CLI requests a
typed work-key confirmation; the ledger binds the selected work key and
relevant content digest, runner, scope, expiry and limits, while retaining the
reviewed graph snapshot ID as evidence. The content digest covers the selected
work and transitive prerequisites and excludes fetch time. A `pinned` launch
compares the grant with the frozen selection; a `refreshed` launch compares it
with the newly fetched selection. To authorize `refreshed`, the host first
fetches and presents current content, issues a grant from that reviewed
snapshot, then re-fetches at launch and refuses any relevant content change
before redeeming the grant. A matching reference is atomically redeemed before
run reservation. Grants issued under the older snapshot-ID-only rule cannot
be redeemed by the content-bound route. This local mechanism does not by
itself make untrusted stage code
safe: the issuer must remain outside the stage's process and filesystem view,
and effective time and model-turn limits must be enforced by the runner. The
typed confirmation alone does not authenticate an operator. Until
those boundaries are verified, the grant remains a fixture-only authorization
check and cannot authorize a model-backed Work Graph launch.

The local zero-turn route keeps the GitHub login, disposable Langflow API token,
grant ledger and durable run store on the host. It fetches the saved flow once
and passes only that frozen export and package code to a network-disabled
Docker worker using read-only mounts and scratch tmpfs. The worker builds the
pinned Langflow graph and reports graph/component hashes. The host verifies
them against the export before reserving the run, then records one dispatch
attempt before sending one execute command. A timeout stops the named worker
container and leaves the run outcome `unknown` without automatic replay.
The local CLI exposes fetch, grant issue and launch operations. This route
requires a disposable loopback Langflow server with auto-login enabled; its
token is held only in host memory. The worker uses a locally present pinned
image without pulling it at launch and runs as a numeric non-root user. The
worker's hash report checks that it loaded the host-supplied flow bytes; it
does not attest arbitrary custom component behavior. Grant redemption occurs
before that hash check, so a failed check consumes the grant without reserving
a run. The future approval/retry policy belongs to #95, and adversarial
component isolation belongs to #96. This route
does not grant a model turn, prove operator identity beyond the local session,
or establish safe protocol behavior against malicious custom component code.

For the #96 control boundary, the host controller derives the frozen graph
and component-code digests directly from the saved export before reservation.
It never accepts a component-supplied `ready`, digest, `complete`, or `failed`
line as control evidence. A disposable validation container may check whether
the pinned Langflow runtime can build the export, but its stdout is discarded
and its exit status is only a compatibility check. After successful validation,
the host reserves the run and starts a separate executor container once. The
host determines process termination from Docker, not executor stdout; stdout
is untrusted result data. A nonzero exit is failure, and timeout or lost
container status remains unknown with no automatic replay. The Docker image,
numeric user, network restriction, mounts, and capability policy do not widen.

This boundary prevents custom component writes to inherited or discovered
container descriptors from impersonating the host's control messages. It
attests the frozen input bytes the host supplied, not faithful execution of
arbitrary component code. A malicious component may choose its own output or
terminate its own executor process; a zero exit therefore means only that the
executor process ended successfully, not that its result is truthful. Do not
promote process completion to a model-backed, hosted, or adversarial semantic
correctness claim.

For this Docker route, `completed` records only a zero executor-process exit.
The durable run records `completion_basis: process_exit` and leaves
`evidence_complete: false`. No consumer may treat this status or untrusted
stdout as semantic graph success without separate output verification.
Validation builds the flow in a disposable container and can execute custom
component construction code; it is not a passive parse or an attestation.

The runner supplies status and results. Work Graph associates each run with
its frozen work snapshot and exposes references to output, file changes and
[trace evidence](../../run-traces/contract/README.md). Preserve partial results on
failure, cancellation, timeout or interruption. Missing fields remain unknown.
Source write-back, PR creation and merging need their own explicit operations.

A rerun receives a new run ID and preserves previous results and traces.
Record which input, skill, definition and workspace refs were reused or
changed. Use a fresh native session by default. Resume is a separate runner
operation bound to the last post-run workspace snapshot. A graph refresh
cannot silently change a rerun's captured inputs.

## Delivery and verification

| Slice | Deliverable and acceptance |
| --- | --- |
| 1. Read-only work model | GitHub connector and immutable graph records; fixtures prove stable identities, cross-repository/unresolved edges, cycles, partial fetches, refresh preservation and filtered isolated matches |
| 2. Work Graph view | Reviewed view-owned Draw.io and a scoped frontend integration; browser evidence proves filtering, dependency context and graph readability against that design |
| 3. Explicit launch | Bind pinned work to the accepted local runner; prove stale-source handling, prerequisite checks, invalid grants, runner refusal and retained run/trace refs with credential-free tests first |
| 4. Run inspection and rerun | Preserve linked run histories and partial results; prove a rerun creates new evidence and resume validates the saved workspace |

The launch slice depends on accepted
[runner issue #8](https://github.com/amadou-6e/laomedo/issues/8) and, when a
skill is selected, [revision issue #9](https://github.com/amadou-6e/laomedo/issues/9).
[Langflow issue #10](https://github.com/amadou-6e/laomedo/issues/10) and
[pilot issue #11](https://github.com/amadou-6e/laomedo/issues/11) provide the
flow handoff and its evidence. Implementation issues must pin the governing
spec commit. Model-backed acceptance runs require a separately authorized
budget and retained ledger. Hosted execution remains subject to
[authentication issue #129](https://github.com/amadou-6e/specs/issues/129).

## Decisions still needed

- Freeze the view-owned design and the exact Issue Atlas modules to reuse.
- Choose persistence/schema versions and refresh behavior for partial sources.
- Define acceptance evidence that can satisfy prerequisites beyond source
  ticket closure, before enabling automatic scheduling.
- Specify source write-back and automatic scheduling separately from the
  initial explicit-launch path.
