---
title: Local application execution and Langflow demonstration contract
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Local application execution and Langflow demonstration

Draft target contract for [release package two](../../../architecture/release-packages.md).
Confirmed: single-user local, Windows and Codex first; filterable issue graph with workflow
assignment; launch by issue/category; bottom stage-progress bars; navigation
to workflow/branch/PR; agent-node monitoring; explicit workflow editing separate
from execution/monitoring. macOS, Linux and OpenCode follow. The [owner interview](../../../decisions/0006-release-packages.md)
records these choices and the remaining question map. These
requirements must be carried into reviewed
Draw.io. This prose does not define screen geometry, UI states or transitions,
and is not authority to implement new controls absent from that design.

## Issue graph and workflow assignment

Reuse [Work Graph](../contract/work-graph.md) for source snapshots, provenance,
dependency edges, complete-graph readiness and dispatch binding. Filters may
hide an open blocker visually but must not make the dependent ready. Keep
GitHub issue state, readiness and execution state distinct.

The board should make the assigned workflow and its revision discoverable for
an issue. Confirmed resolution: an explicit per-issue assignment wins over a
label-based default. Categories are GitHub labels, including actions (research,
implementation, fix) and areas (UI, backend, data). Among labels that have a
configured workflow default, use alphabetical label priority: the first matching
label selects the default. Labels without a default do not participate. Show
the winning label and assignment source so the choice is explainable. For
example, with defaults for both backend and research, backend wins unless the
issue has a direct assignment. Alphabetical case/Unicode normalization still
needs a documented deterministic rule before implementation.
Workflow assignment is configuration,
not authorization to launch and not a modification to source issue text.

The workflow selector should list action-oriented presets such as Research and
Implement alongside user-created workflows. Users can clone an existing graph,
edit the clone or create a graph from scratch in explicit editing mode. These
are confirmed capabilities; dropdown geometry and interaction transitions still
need the owning Draw.io. Preset contents and assignment persistence are not yet
decided.

## Workflow tags and frozen revisions

Confirmed: workflow selectors use tags, following the user's container-tag
analogy. An assignment selecting `latest` automatically picks up the current
published revision on its next launch. An assignment selecting a specific
version keeps that version until explicitly changed. `latest` follows published
updates automatically. An editable draft is not a published update; creating
one does not change assignments or running graphs. This selector behavior was
already decided and is not reopened by the release interview.

Resolve the selector once before dispatch and record both the requested tag
and the exact graph/component revisions and content hashes. Moving `latest`
never changes an active or historical run. Missing versions refuse launch
without silently falling back. This follows the existing launch-time freeze
in [subsystem handoffs](../../../architecture/subsystem-handoffs.md).

## Direct Laomedo chat assistant

Confirmed: Laomedo includes a chat in which the user communicates directly with
an agent that helps them interact with Laomedo. One intended task is creating a
new workflow that combines existing graphs, such as Research and Implement,
instead of relying on the alphabetical label winner.

Confirmed authoring handoff: the assistant saves an editable draft, then asks
whether the user wants to switch to the graph editor. It navigates there only
after agreement. Creating the draft does not publish a version or start a run.
Proposed assistance includes inspecting selected revisions and explaining stage
ordering, inputs/outputs, skills and stopping conditions. Combining graphs is
an authoring operation, distinct
from automatically launching both matching defaults. Chat alone must not be
treated as evidence that a graph was saved, tagged or executed.

The assistant's permitted actions beyond that draft handoff, context access,
provider/session lifetime and monitoring remain to be specified. This brief does
not introduce another sign-in or activate the retired approval authority.
Chat layout and transitions need the owning Draw.io before implementation.

## Functional reference

The user selected [shdennlin/issue-graph](https://github.com/shdennlin/issue-graph)
as an example. Its [README](https://github.com/shdennlin/issue-graph#readme),
inspected on 2026-10-10, describes dependency views, label grouping, multi-select
filters and saved views. It currently documents a Linear data source, with
GitHub Projects described as future work in the repository summary. These are
documentation observations, not a tested GitHub connector or execution engine.

Use its graph exploration and filtering as behavioral inspiration. No adoption,
runtime compatibility or feature-parity claim is made. Pin a source revision
before a reuse evaluation. GitHub Actions is the separate visual reference;
the particular screen and reference captures remain unresolved.

## Launch and durable correlation

For each launch resolve the issue/work key, dependency snapshot, workflow
revision, component code, pinned skills, provider/model/effort and run budgets.
Show unresolved or stale inputs and apply the existing dispatch contract rather
than bypassing it from a convenient UI button. Retain both the graph used for
readiness and the revision bound to execution when they differ.

Record run, graph run, stage invocation, native request/thread, trace and
branch/PR references through the existing owners. A connection failure must
not blindly submit another run with a new identity. A client stopping its wait is not
confirmed remote cancellation. No source issue is closed just because an
executor exits successfully. Existing #22/#93/#104 limits remain applicable.

The selected workflow must create its draft PR automatically through configured
scoped GitHub access, subject to the publication integration gate below. There
is no separate click-to-publish requirement for that
successful path. This does not select automatic PR merging or issue closure.
An agent-reported task failure is handed to the graph, where configured routing
can send it to a reviewer or human-in-the-loop step instead of publication.

## Output Contract, correction and retention owners

The canonical [Output Contract](../../agent-execution/contract/output-contract.md)
owns the separate node's validation, agent-side precheck, one configurable
continuation default and distinction from graph-routed task failure. This
contract composes those outcomes into the demonstration below, rather than
introducing a second evaluator or retry policy.

Infrastructure recovery remains a separate desired mechanism with unresolved
bounds and uncertain-effect reconciliation; deferred crash rules are not lifted.
No new 20/50-turn or 30/60-minute execution default was selected.

Interrupted changes are governed by [results/artifacts retention](../../results-artifacts/contract/interfaces.md#interrupted-work-retention-selected-in-the-release-interview);
partial traces by [run-trace retention](../../run-traces/contract/interfaces.md#interrupted-trace-retention).
Both preserve the original run's evidence until explicit deletion; storage and
disk-pressure handling remain unresolved.

## Progress and navigation

The bottom strip is proposed as a compact projection of actual stage activity.
The user's green running bars need text/icons and an accessible equivalent;
color alone must not convey state. Planned stages, active invocations, terminal
outcomes and stale/unknown observations must remain distinguishable in the
owning Draw.io. Concurrent stages cannot be collapsed into one assumed active
stage. Display semantic failure independently from graph-process completion.

Expanding progress should reveal the exact workflow revision for that run.
Branch/PR navigation uses recorded references; absent or uncertain publication
must not produce an invented link. Selecting an agent invocation should retain
that run/stage/attempt while opening its monitoring information.

## Explicit workflow editing

Execution and monitoring inspect frozen run snapshots. Editing is an explicit
action on a workflow definition, not on the historical run. Saving produces
a new definition revision; an active run stays on its original graph/component
identities. A later launch follows its selected `latest` or pinned tag. Editing
alone does not launch or resume anything. Define draft/version storage,
stale-editor conflicts and whether editing is embedded or opens a separate local Langflow
surface before writing the UI contract.

## Agent monitoring

Consume [run-trace records](../../run-traces/contract/interfaces.md) and
[result references](../../results-artifacts/contract/interfaces.md), not
uncorrelated UI logs. Proposed inspection content:

- Native agent events and messages, with provider/thread/turn/invocation identity.
- Tool start, arguments, results and outstanding-command state; an agent answer
  does not imply its shell commands finished or artifacts are ready.
- Measured per-request model/effort and input/output/cache counters where exposed.
  Missing usage is unknown, not zero; estimates are labelled separately from
  billed charges and subscription consumption.
- Timing, cancellation requests versus confirmation, partial/completeness
  markers and provenance/ownership of raw versus projected records.

Raw events can contain sensitive material. Define local access, redaction,
export behavior and retention for other record classes before enabling broad
trace downloads. Interrupted changes and partial traces use the explicit
retain-until-deleted choice above. Inspecting
raw traces is not permission to publish them. AGENTVIZ integration is not needed
for the first UI slice unless separately selected.

## Proposed first vertical slice and acceptance

Owner-selected first success scenario: open a repository's issue graph, select
an implementation issue, choose its workflow, run the agent, inspect progress
and tool traces, then open its automatically created draft PR.

Proposed bounded implementation slice: one repository, one selected issue,
one assigned versioned workflow, one Codex agent stage and an Output Contract,
with graph routing for success, task failure and validation rejection. Reopen
the UI and inspect the same recorded run without implying workflow recovery.
Explicit editing saves a new revision without changing the active or historical
run. Start with synthetic fixtures; live acceptance needs its own scope/budget.

## Next requested demonstration: the complete Langflow graph

Publication integration gate: [decision 0005](../../../decisions/0005-active-run-pr-feedback.md)
uses an active agent stage's revocable write grant. This demonstration instead
places publication after downstream validation. A trusted active handoff or
separately scoped publisher capability must be specified/tested before that
route can launch; neither is selected here. Do not reuse a revoked agent grant,
extend its lifetime implicitly, or assign publishing to Results by implication.


The owner's next expected deliverable is a running, inspectable Langflow
workflow, not only these documents or separate component checks. It must show
issue ingestion, a Skill node connected to the Agent node, explicit contract
outputs, failure behavior, conditional routing after the Output Contract and
automatic draft PR creation on the successful route.

Proposed demonstration wiring, subject to reviewed graph design:

```text
Issue ingestion ── task and frozen issue context ──► Codex Agent
Skill Reference ── pinned skill reference ─────────► Codex Agent
Codex Agent ── structured submission ──────────────► Output Contract
Output Contract ── validation and task outcome ────► Conditional routing
  accepted + success ──► scoped draft PR creation ──► recorded PR reference
  accepted + task failure ──► reviewer or human-in-the-loop destination
  rejected submission ──► configured correction/review destination
```

This text records dataflow intent, not authoritative UI geometry. In this
demonstration, PR publication belongs after validation on the success route;
the task/skill must not publish a PR before that route executes. The agent's
precheck uses the contract requirements before handoff; the separate contract
node makes the downstream decision. Trace/run outputs remain inspectable even
when the submission or task fails.

| Case | Evidence needed from the actual imported graph |
| --- | --- |
| Valid success | Ingested issue identity/body snapshot, pinned skill/run identity, accepted contract output, selected success route and actual draft PR reference with verified published bytes |
| Valid task failure | Failure is accepted as a well-formed outcome, failure route executes, success route does not publish a PR |
| Invalid submission | Contract emits rejection with check errors, rejection route executes, no success publication |
| Precheck correction | Agent sees requirements and check feedback during its request; corrected submission reaches downstream validation |
| Exhausted correction | Evidence distinguishes precheck continuation from downstream routing; no hidden unlimited agent retry |
| Agent/runtime interruption | Partial evidence and changes retained; infrastructure error does not become a fabricated task success or an unverified PR reference |

Start with credential-free fixtures executed through the same imported graph,
not a separate script that merely reproduces routing. Then run the authorized
real Codex success path and bounded failure/correction probes. Simulated PR
publication must be labelled simulated; it cannot establish the draft-PR gate.
Publish only through an explicitly scoped test repository/branch and write
capability, with an agreed model-turn cap. No new live cap or external-write
grant was supplied by the owner's request to see this demonstration.

Implementation inventory checked at Laomedo `develop`
`6882fc8ea7a90bcaf310fa6c38f8a049789797e5` on 2026-10-10: existing Skill and
Codex components and flow builders can be reused. No Output Contract component
is present in that component inventory. The current Codex component raises
known failures and does not emit a failure Data output, so graph-consumable
outcomes need explicit integration. Issue-context and GitHub mediation code
exist, but their composition into this demonstration is not yet verified.

Required work: specify/implement Output Contract and its agent precheck;
expose structured routable outcomes without losing run/trace identity; connect
read-only issue ingestion and conditional publication; export/import the flow;
test the three routes; collect bounded real-run and draft-PR evidence. This
does not depend on building the separate Laomedo application UI first.

Candidate checks for the later reviewed UI/adapter implementation:

| Scenario | Expected property |
| --- | --- |
| Filter hides an open blocker | Complete-graph readiness remains blocked |
| Direct assignment and label default both exist | Direct assignment selects the workflow |
| User clones a preset | Editing the clone does not change the source preset or an active run |
| Multiple labels have workflow defaults | Alphabetically first matching label wins; direct assignment still overrides |
| Selected workflow version is missing | Launch refused without fallback |
| `latest` moves after assignment | Next launch resolves new revision; existing runs remain frozen |
| Specific version assigned and `latest` moves | Next launch retains the assigned version |
| Assistant proposes a combined graph | Inspectable draft; original graphs and issue assignment remain unchanged until applied |
| Assistant saves draft; user declines screen switch | Draft retained; current screen unchanged; no publication or execution |
| Agent precheck rejects a form | Feedback permits correction in the same request; default one continuation available if needed |
| Contract rejects handed-off output | Conditional routing receives rejection; no forced agent rerun |
| Agent reports task failure in valid output | Failure route receives outcome; not treated as a malformed submission |
| Workflow successfully produces code | Draft PR created automatically through scoped access; no automatic merge or issue closure |
| Run fails or is stopped | Uncommitted changes and partial traces retained until user deletion |
| Double launch/response lost | Stable identity and reconciliation; no hidden duplicate model run |
| Workflow edited during execution | Old run remains bound; new launch receives selected new revision |
| Active command after final agent message | No premature artifact readiness or successful stage claim |
| Late event from another attempt/head | Does not overwrite the selected invocation or trigger an unbounded correction |
| No measured token usage or disconnected progress | Unknown/stale is distinguishable from zero/completed |
| User opens another node/run | Trace ownership remains explicit; private paths/credentials are not rendered as links |

Open decisions and engineering work: reference screens and source pin;
assignment persistence and alphabetical normalization; assistant action/context
scope beyond the confirmed draft handoff; infrastructure retry bounds and
uncertain-effect reconciliation; execution deadline policy; output-check types
and precheck wiring; draft/version storage; trace redaction/export and storage
for retained work; progress presentation; navigation to historical execution
versus editable definition. Windows/Codex first, automatic installation,
selector behavior and interrupted-work retention are settled product choices.
Multi-user hosting and arbitrary workflow-cycle support
are not part of the confirmed first release.
