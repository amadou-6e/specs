---
title: GitHub PR selection, inspection and incoming operations
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-15
applies_to: [laomedo]
supersedes: null
related: []
---

# GitHub PR node

User-selected work: align PR selection, viewing and operations with the
[GitHub Issue node](langflow-node.md). Inspected specs base `ab29aa2` and
Laomedo develop `c29c93f`. This contract records the requested behavior; local
test evidence is separate from deployment or live GitHub-write acceptance.
The [editable interaction model](../design/github-pr-node.drawio) owns controls,
states and transitions. The [operation graph](../design/pr-operation.drawio)
shows the bounded modify example.

## Selection and outputs

Display GitHub PR. Repository URL, searchable Labels multi-select, searchable
PR dropdown, refresh, Discovery status and advanced State (open/closed/all)
follow the Issue node pattern. All selected labels must match. Only real PRs
appear, with number/title. Discovery is bounded to ten 100-item pages and a
60-second deadline; incomplete discovery is refused. Empty, failed and loading
states are distinct. Changing repository clears labels and PR; changing labels
or state clears PR. Refresh preserves the same number if still valid and updates
its title. Obsolete responses cannot replace a newer selection.

Inputs: optional PR Reference and Operation. Outputs: PR, Task and Operation
Result. PR Reference supplies repository/number from an upstream PR node; it
must match the configured repository and any explicit picker selection. It is
identity, not permission. With no Operation, execution reads current content,
revalidating selection and filters. All outputs share one cached invocation.
Failure/unknown stops Task rather than sending errors as an agent prompt.
Neither discovery nor inspection makes a model call.

PR records contain repository, number, exact `/pull/<number>` URL, node ID,
title, body, labels, state, draft/merged state, updated marker, head repository,
branch and SHA, and base branch. Operation Result includes fetched-at evidence,
content digest and operation status. Fork PRs may be inspected; the initial
write implementation requires a same-repository head on the granted branch.

## Operations and permissions

Operation Data uses the Issue node envelope:

```json
{"action":"modify","request_id":"pr-demo-1","grant_ref":"host-capability-reference",
 "changes":{"title":"Updated PR title","body":"Updated description","labels":["research"]}}
```

Close uses `action: close` with no changes. Modify accepts supplied title/body/
labels only. Labels replace the full set; [] clears labels. Empty body is valid;
empty title is refused. Target overrides, arbitrary API paths, merge, reopen,
base changes and draft conversion are outside this first slice.

The host resolves the opaque grant to an existing run-scoped expiring capability
enumerating `pr_node_update`, approved PR number/base and approved head branch.
The node never mints a grant or receives provider credentials. Existing
`pr_update` publication semantics remain intact. The host checks expiry,
revocation and connection generation immediately before each mutation, and
checks current identity, head SHA and content against its recorded digest.
Merged PRs and foreign head repositories cannot be modified in this slice.

Title/body/close use the pulls endpoint; labels use the issue-label endpoint
after validating that the number is a PR. A combined operation may require two
remote writes. It is not atomic: partial success, lost acknowledgements or
inconclusive readback are unknown and are never automatically repeated.
Concurrent edits after the optimistic content comparison remain a race.
Success requires current readback matching requested values and unchanged PR
identity/head/base. The whole effect is durably recorded before dispatch.
Repeated request identities return the previous result; payload changes under
the same identity are refused, including after process restart.

Statuses match Issue: not_requested, succeeded, failed, unknown. An updated PR
leaving the original label/state filter still returns its confirmed result;
later reads must select a matching PR. Title/body/bundle bounds match the Issue
node (256 characters, 256 KiB UTF-8, 1 MiB request/response envelope).

## Viewing and external link

Replace Code on this node with PR viewer and Open in GitHub; other node actions
retain their owners. Viewer shows title/body, labels, state, draft/merged state,
head → base and update/fetch markers in a read-only panel. It reads the exact
picker identity and current filters through authenticated inspection with
operation=None. Selection changes or closing the panel abort/ignore older reads.
Loading, missing selection and read refusal have explicit states; Refresh repeats
only a read. Markdown omits HTML and images; safe HTTP(S) links require a click.
Open in GitHub uses only the verified repository/number URL, with
noopener/noreferrer. Without picker identity it is disabled; a runtime-only
reference does not become an invented saved selection.

The [fixture viewer screenshot](../design/references/github-pr-viewer.png) is
derived inspection evidence. It does not replace the editable model or prove
an active GitHub connection.

## Operation example and acceptance

The user selected a two-node round trip: one GitHub PR node and one Agent.
PR Task feeds the Agent, whose selected Operation/answer output returns to the
same PR's Operation input. Operation supports both ordinary upstream input and
controlled feedback. A direct Task connection to the source of the incoming
Operation identifies the bounded round trip. An acyclic upstream Operation is
evaluated normally. Multiple Operation sources, feedback plus a literal
Operation value, or combined legacy infinity feedback and Operation are refused.
The Task output does not expose an infinity socket in newly generated nodes;
older saved infinity-feedback graphs remain readable for compatibility.
The PR node is the loop controller, with one initial read, exactly one Agent
body execution, one returned operation, and a terminal result. No third Loop
node or second PR node is required. The Task branch is stopped in the outer
graph; the native isolated subgraph runs the Agent once, rather than letting
the outer scheduler invoke it again. Multiple body nodes, fan-out or multiple
feedback sources are refused in this bounded first slice.

Freeze the selected repository/number and fetched content digest before calling
the Agent. Read refusal stops before the Agent. The feedback must be Data with
the existing operation envelope, or a Message containing that JSON object.
Read the exact connected return output, not an arbitrary first Agent output.
Missing/malformed feedback and Agent failure/cancellation refuse publication.
Revalidate the original PR digest before an initial mutation, so edits made
while the Agent runs cause refusal rather than overwrite. Existing host grants,
target/head/base checks and durable replay semantics still apply. No feedback
content may retarget the PR, mint a grant, or trigger another Agent invocation.
Unknown mutation stops the round trip without retry. Duplicate evaluation of
node outputs shares the same round trip and terminal operation result.

The importable example uses an explicitly labelled deterministic Agent fixture
and fake GitHub; it must run through actual Langflow loop handles, subgraph
execution, gateway and durable effects. It does not claim a real model turn.
Fixture examples are internal test material and require explicit user approval
before presentation. User-requested demonstrations use real agents and live
integrations; missing connections are reported as blockers.
Two graph runs with the same operation request identity must send one mutation.
Verify close/modify, exact feedback-port selection, failed reads, malformed or
missing feedback, Agent failure, concurrent edits and uncertain writes. Preserve
the older four-node evidence as history rather than relabel it as loop evidence.

Acceptance covers all-label discovery, bounded pagination, selection clearing,
refresh, stale-response guards, exact read-only viewer identity, reference
conflicts, current reads, close/modify, target/branch/base/grant refusals, expiry
before PATCH/PUT, restart replay, partial effects and uncertainty. Live deployment
and a real PR operation require their separately scoped configuration and target.
Browser/build evidence must be reported honestly rather than inferred from tests.

The intended Agent is the existing Laomedo Codex Agent and its trusted runner.
On 2026-10-15 the user explicitly selected removal of the separate PR-specific
CLI agent from the product. Historical checks of that adapter do not prove the
original runner's PR round trip. Docker unavailability is a blocker, not permission
to substitute another agent. Native provider/runner integration remains unverified.

The submitted operation envelope supplies request identity and opaque grant
reference; in feedback mode these may be model-authored. The gateway validates
them but does not stamp them. Host-side stamping remains an original-agent gate.
They are not evidence of model authority. The removed adapter took them from graph configuration, not
from a host-generated post-response identity. Grant references must be protected
as capabilities on this trusted single-user host; owner/flow binding is a gap.
Exact-payload durable replay prevents a duplicate effect, but a new graph run
still invokes the Agent and a different response with the same identity conflicts.
The deterministic replay test is not proof of model-free reuse across runs.

The controlled cycle must start at the PR in full editor builds and when
the Agent's play action is used, irrespective of node ordering or process hash
seed. Component initialization must bind the controlled feedback handling for
both payload-loaded and programmatically connected graphs.
Attaching a downstream Operation Result inspector must preserve that entry rule
and exactly one Agent invocation. This does not authorize arbitrary graph cycles.
The isolated feedback body currently contains only the returning Agent. An
additional upstream input to that Agent from another node is refused before
dispatch, rather than silently omitted. Configure its pinned skill and runner
directly on the existing Agent for this bounded topology.

Primary API references: [pull requests](https://docs.github.com/en/rest/pulls/pulls)
and [issue labels](https://docs.github.com/en/rest/issues/labels).

## Proposal: creating a PR before a reference exists

User clarification: creation means a new pull request. Proposed follow-up: the
same visible GitHub PR node has Existing and Create draft modes. Existing keeps
picker/reference inputs. Create draft disables the PR picker, viewer and external
link until confirmed creation. It accepts an accepted publication handoff from
Output Contract rather than inventing a PR number or accepting arbitrary branch
publication from the agent. The host owns the exact repository/head/base, staged
commit, title/body, capability and durable request identity.

Reuse the current trusted Draft PR Publisher's run-bound publication operation.
After confirmed creation, emit PR Reference (repository/number/URL) and the
confirmed result; the run inspector can open/view that returned PR without
mutating saved picker state. A downstream Existing instance consumes PR Reference
for later operations. Unknown creation yields no reference: reconcile the durable
publication marker and branch pair, never resend automatically. A missing/ambiguous
match remains unknown. Creation grant binding and any subsequent update grant are
separate; the new reference alone grants no writes. This mode and its run-result
viewer are a proposal, not implemented or accepted UI geometry in this change.
