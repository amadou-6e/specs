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
