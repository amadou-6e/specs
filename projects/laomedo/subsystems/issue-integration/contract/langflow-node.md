---
title: Live GitHub Issue Langflow node
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-13
applies_to: [laomedo]
supersedes: null
related: []
---

# Live GitHub Issue Langflow node

Tracking: specs #374, Laomedo #160. Owner decisions: [0009](../../../decisions/0009-live-github-issue-node.md).

## Controls and selection

The visible node is GitHub Issue. Repository URL accepts an HTTPS github.com
owner/repository root, without credentials/query/fragment or arbitrary API paths.
Labels is a searchable multi-select of actual repository labels. Issue is a
searchable dropdown showing number and title. All selected labels must match.
Open issues are the initial default; an advanced State selector supports open,
closed or all. These state defaults are implementation proposals, not additional
owner interview answers. PRs never appear as issues. Discovery is bounded and
paginated; an incomplete result is a refusal, not an apparently complete empty list.

Changing repository clears labels and issue. Changing labels or state clears
issue. Refresh preserves a still-valid exact issue identity. Unavailable or
changed selection never silently substitutes another issue. Failed, empty and
loading states are visible; a late old response cannot overwrite current controls.
The [editable states](../design/github-issue-node.drawio) are the UI authority.

## Execution and outputs

Without Operation, execution retrieves the current selected issue. It revalidates
repository, issue identity, state and ALL label predicates using fresh data.
Issue Data carries repository/number/URL, current title/body/state/labels/update
marker and fetched-at evidence. Task Message provides readable issue context for
an agent, treating issue text as task data rather than permission to execute it.
An unavailable issue or failed/unknown operation stops the Task branch, so an
error message is not dispatched as an agent prompt. Operation Result remains
routable. The same cached execution result serves all outputs of one node invocation.
No model call is made by this node.

An internal fetched-content hash is evidence, not a permanently frozen picker.
The historical base64 FrozenIssue fixture remains separate. Migrating a live demo
must explicitly adapt its downstream context/task bindings and preserve its budget;
renaming the old fixture alone does not establish a live connection.

## Incoming Operation

An optional Issue Reference input can receive the identity from an earlier node,
so a separate downstream instance can apply an operation without creating a graph
cycle. It must match the configured repository and any explicit picker selection.
It carries identity, not permission or authoritative current issue content.

Operation is optional Data:

```json
{"action":"modify","request_id":"opaque-effect-id","grant_ref":"host-capability-reference",
 "changes":{"title":"Updated title","body":"Updated body","labels":["implementation"]}}
```

Close uses action close and no changes. Repository and issue target come only from
the node's selected identity; incoming target overrides, extra fields and arbitrary
API methods are refused. Modify patches only supplied title/body/labels; labels
replace the complete issue label set, with [] explicitly clearing it. Empty body
is allowed, empty title is refused. Labels must exist in the selected repository.

The opaque grant reference resolves only on the host to an existing run-scoped,
expiring capability. Grants enumerate permitted issue numbers and issue_update
operation; no ambient host login or raw credential enters graph fields or the
agent. Merely connecting Operation does not mint a grant. Expiry, revocation and
connection-generation guards remain authoritative. No write is allowed when the
host cannot resolve the exact capability/target.

The host rechecks grant expiry/revocation immediately before PATCH, after any
preceding reads. It cannot retract a request already sent to GitHub.
The host re-reads the issue and sends an expected content/update marker with the
narrow patch. Transport compares current content before PATCH and verifies
acknowledgement/readback. This is an optimistic check, not GitHub atomic CAS;
a concurrent change after the comparison remains a documented race.

Operation Result distinguishes not_requested, succeeded, failed and unknown.
A durable request/effect identity is recorded before dispatch. Re-evaluating an
output or retrying the same identity returns its prior result; changing payload
under that identity is refused. Timeouts, lost acknowledgements, process death or
inconclusive readback remain unknown and do not trigger another PATCH. A successful
close/label change returns the confirmed updated issue even when it leaves the
original filter; subsequent reads must choose a matching issue again.

## Verification and activation

Credential-free transport and native tests cover AND filtering, pagination,
PR exclusion, stale selection, current reads, close/title/body/labels patches,
foreign/expired/revoked grants, duplicate output evaluation and uncertain delivery.
Browser checks use an imported source-only graph with a fake GitHub transport.
No live issue edits are inferred from this implementation request.
Live activation needs a reviewed connection/configuration draft; actual close/
modify acceptance requires explicitly scoped disposable issue write permission.

## Transport bounds and source references

The implementation scans at most ten 100-row pages with a 60-second discovery
budget; reaching a full last page refuses an incomplete result. Label selection
is bounded to 100 names, each at most 100 characters. Modify title is at most 256
characters, body at most 256 KiB UTF-8. These are application bounds, not claims
about GitHub's maximum supported sizes. The request, response and persisted
request-hash envelope remain bounded to 1 MiB. The backend supports one explicitly
configured repository connection per service instance; no ambient gh login fallback.
Without host grant bindings, writes are unavailable, not silently performed.

Primary API references checked 2026-10-13: [repository labels](https://docs.github.com/en/rest/issues/labels)
and [issue reads/updates](https://docs.github.com/en/rest/issues/issues).
GitHub's issues API also contains PRs, so the transport explicitly excludes them.
The node uses the existing pinned Langflow 1.12.3 MultiselectInput and Data ports.


## Issue viewer tabs

Owner-selected update 2026-10-13, specs #376 / Laomedo #162: the node toolbar
replaces Code with Issue viewer and Open in GitHub. Other nodes retain their
existing controls. Issue viewer opens a read-only panel with current title,
body, labels, state, number and update/fetch markers. It uses the exact configured
repository and issue number, revalidates current filters, and never performs an
operation or model call. Closing or changing selection aborts/ignores old reads.
Empty selection, loading and read refusal have explicit states. Retry repeats
only the read. Issue text is data: raw HTML, scripts and remote images never run
or load. Markdown links require an explicit user click and safe HTTP(S) URLs.

Open in GitHub opens the exact selected issue URL in a separate browser tab with
noopener/noreferrer. It is disabled when the selected identity is absent or
invalid; it never opens an arbitrary URL supplied in issue text. An instance
fed only by a runtime Issue Reference without a configured picker reports that
no inspectable UI selection is available rather than guessing an issue.


## Saved GitHub account connections (#286)

Owner-selected on 2026-11-16 in implementation issue
[laomedo#286](https://github.com/amadou-6e/laomedo/issues/286): both Issue and PR
nodes use saved GitHub accounts for reads and the existing scoped modify/close
operations, including private repositories. The **Saved accounts** page of each
node's Draw.io owns GN286-S01 through GN286-S07 and the approval screen. Earlier
pages retain the explicit configured-host-service path.

The Connection selector precedes Repository URL. It lists only connections owned
by the active local profile, with their verified account names and availability.
Selecting a different connection clears discovered labels and Issue/PR choices.
An explicit Configured host connection option retains the existing operator-owned
service path, shown disabled with "Not configured" when unavailable. A saved
connection owned by another profile appears only as "Connection unavailable",
without its account name. An empty selection asks the user to choose a connection. A selected
saved account never falls back to that host service or another account.

Before discovery and execution, revalidate the current profile/browser lease,
connection generation, numeric repository identity, exact consented repository name
and live GitHub access. Account possession or a repository URL alone is not consent.
Disconnect, expired admission, a stale generation, missing provider permissions or
an unconfirmed rename/transfer refuses new reads and effects. Recovery selects or
reconnects that same account; an ambiguous GitHub 404 never proves a private
repository exists. Tokens stay in host custody, outside graph parameters, browser
storage, exports and Agent workspaces.

### Run admission, history and writes

The user selected normal local-profile run history, including private Issue/PR text.
Disconnect stops future GitHub access but does not erase history already acquired
by that profile. Native flow, job, trace, build-history and message reads must be
restricted to that owning profile. Exported flow definitions must omit private
runtime output. A public/shared execution route cannot acquire a profile's GitHub
access. Downstream Agents may receive the authorized Issue/PR text, never its
credential or reusable browser admission.

The host binds each private graph run to its initiating profile/lease, exact graph,
job, vertex, selected connection generation and repository. That binding remains
host-only and expires; a serialized graph, restart or copied job identifier cannot
reconstruct it. Native background execution, event delivery and cached results
must enforce this binding, not merely the browser's dropdown request. Logout or
lease expiry stops the next provider read/write. A write already dispatched keeps
its confirmed, failed or unknown outcome; losing admission never triggers a retry.
Previously acquired history remains owner-scoped rather than requiring a live
GitHub connection to read it.

A successful routine credential renewal may continue an already admitted run
only through host-proven refresh continuity for the same account and unchanged
repository consent. Matching metadata alone is insufficient. Reconnect, consent
change, revocation and an uncertain refresh break that continuity. Neither a
restart nor a serialized graph restores it. Buffered browser reads retain their
exact-generation response-release fence.

Canvas Run, node Run and playground execution share the same host admission.
If any reachable Issue/PR node has a connected operation input or an Agent feedback
edge, show one combined approval dialog for the run, listing every saved account,
repository, exact permitted Issue/PR target and permitted modify/close operation
kind. This is an upper bound, not a preview of Agent-generated patch content.
Current picker targets are mandatory for write-capable saved-account nodes;
no target means "Choose an Issue/PR before allowing changes", with no job dispatch.
Runtime references must match those approved targets. Downstream references cannot
expand them. Runtime operations outside the envelope fail before dispatch with
`github_node_operation_not_approved` and a failed outcome, never unknown.

A run with no reachable connected operation input or feedback edge is read-only
and bypasses approval. It receives no mediation write grants. An unexpected write
attempt still fails before dispatch with the same named error. Connecting an
account or pressing a read-only Refresh grants no writes. Several Issue/PR nodes
share one combined dialog; the user approves once rather than once per node.
Cancel dispatches no job or change.

The plan is consumed once when starting the exact graph job. Within that run it
covers all permitted effects on the listed targets, not just the first effect.
Changing connection, repository, target or executable graph requires a new plan.
Each effect still uses the existing mediated exact-target grant, optimistic content
verification, connection-generation fence and durable request identity. Repeated
evaluation of the same effect cannot dispatch twice. Unknown delivery is not
silently replayed; a new run requires new approval and cannot erase an existing
unknown effect record. Approval cannot authorize arbitrary endpoints, PR merge
or issue creation.

New account-owned private Apps request Issues and Pull requests write, alongside
Contents/Metadata read. Existing Apps have an explicit permission-update path to
their own GitHub settings and installation approval, then current access is
rechecked. Never replace an App automatically, borrow another account's App or
claim permissions before GitHub confirms them. The node's "Review GitHub access"
action opens Settings for that selected connection. Settings shows the required
Issues/PR permissions, "Open App settings" and "Check access". After the owner
updates and approves permissions on GitHub, Check access verifies them online;
"Back to node" restores the same graph selection without starting a run. GitHub permission is only an upper
bound; it never replaces the narrower per-run approval.

### Acceptance for saved accounts

Use the real authenticated UI and an owner-approved disposable private repository:
select each account, discover actual issues/PRs, view details, run reads, approve a
bounded reversible modify/close operation and verify its acknowledgement/readback.
Verify account/repository mismatch, missing permissions, cancelled approval,
expired/revoked admission, generation rotation, stale choices, repeated evaluation,
unknown delivery, owner-scoped history/cache/events and output-free exports.
Credential-free tests support these controls but are not live acceptance. A source
or layout review does not establish that native graph execution is integrated.
