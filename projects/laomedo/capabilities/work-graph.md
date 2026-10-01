# Work Graph

Status: proposed for [issue #151](https://github.com/amadou-6e/specs/issues/151).

Work Graph is Laomedo's capability for inspecting repository work and its
dependencies, then handing selected work to agent runs. The initial slice
imports and inspects work. Execution follows the existing
[component contracts](../components/contracts.md) and
[local pilot gates](../feasibility/124.md).

This page defines data and execution contracts. View geometry, controls,
interaction states, and transitions require a reviewed Draw.io specification
under `views/work-graph/ui/` before UI implementation.

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

Graph readiness is an input to dispatch eligibility. Eligibility also requires
a valid run definition, supported runner settings, a recorded grant and
explicit operator authorization. Any prerequisite override must identify
the affected edge and rationale. Automatic scheduling is a later policy
decision; selecting a node does not authorize execution.

The runner supplies status and results. Work Graph associates each run with
its frozen work snapshot and exposes references to output, file changes and
[trace evidence](../monitoring/run-traces.md). Preserve partial results on
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
