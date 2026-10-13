---
title: GitHub PR selection, inspection and incoming operations
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-13
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

An importable Langflow graph wires a read node's PR output and a fixture
modify-operation output to a second PR node, then sends Operation Result to an
inspection node. It must execute through real node ports, gateway, mediation,
REST request shaping and durable journal against an injected fake provider.
Re-running the same request must not repeat the write. No model/provider turn
or real PR mutation is needed for this evidence.

Acceptance covers all-label discovery, bounded pagination, selection clearing,
refresh, stale-response guards, exact read-only viewer identity, reference
conflicts, current reads, close/modify, target/branch/base/grant refusals, expiry
before PATCH/PUT, restart replay, partial effects and uncertainty. Live deployment
and a real PR operation require their separately scoped configuration and target.
Browser/build evidence must be reported honestly rather than inferred from tests.

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
