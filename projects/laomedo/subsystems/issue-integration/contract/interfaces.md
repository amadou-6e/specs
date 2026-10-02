---
title: Issue integration interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue integration interfaces

These are proposed boundaries from the [interface map](../../README.md), not
deployed endpoints. A reference identifies a GitHub resource without asserting
that its text was frozen at selection time.

## IF-01 — selected-issue context for run setup

- **Provider / consumer:** Issue integration →
  [Langflow integration](../../langflow-integration/contract/interfaces.md).
- **Trigger:** a user selects an issue. A later issue-opened event may use this
  exchange only after a trigger service supplies an actual issue reference.
- **Minimum handoff:** repository and selected-issue identity, plus a PR
  reference only when the user supplied one. The launch layer adds its own
  run identity and version selection.
- **Rule:** the agent retrieves current issue content and checks open PRs while
  executing. A related open PR does not silently become the target PR. Missing
  or inaccessible GitHub content remains an error/unknown, not an empty issue.
- **Boundary:** direct-prompt and timer launches have no issue and bypass
  IF-01. A PR-opened event has a PR subject, and a failed Actions event has
  a workflow-run subject; neither fabricates an issue. The proposed
  [launch-context union](../../langflow-integration/contract/interfaces.md#approximate-payloads)
  holds those subjects when a future trigger service is defined.
- **Open:** trigger-service ownership and event deduplication, GitHub
  authorization binding and whether the selected issue is revalidated before
  dispatch. Timer/PR/Actions event launches are outside the first slice.

## IF-12 — reviewed follow-up issue publication

- **Provider / consumer:** [Results and artifacts](../../results-artifacts/contract/interfaces.md)
  → Issue integration; Issue integration then writes to GitHub.
- **Trigger:** user reviews and edits a failure-to-issue draft and requests
  publication.
- **Minimum handoff:** target repository, reviewed title/body, prior run and
  trace/artifact references, the user's publication decision, and a unique
  reconciliation marker included in the exact body presented for review.
- **Proposed rule:** an unsuccessful run alone does not publish an issue. Before
  any create request, issue integration persists the reviewed request bytes or
  their recoverable reference and hash, marker, target, reviewer decision, and
  one attempt identity. It marks an attempt as possibly sent before contacting
  GitHub. An acknowledged, uniquely identified remote issue may be reported as
  `published`; a definitely unsent attempt may be `failed`. A lost response,
  timeout, process death, or inconclusive remote lookup remains `unknown`, not
  `failed` or `published`.
- **Reconciliation proposal:** find the marker in GitHub issue bodies and verify
  exact equality, not just a search hit. Bind an issue reference only if exactly
  one matching issue is confirmed. Zero matches do not establish non-creation;
  multiple matches are a conflict. Neither result triggers an automatic second
  POST. Persistent absence or conflict requires a user decision before any new
  publication attempt. The reviewed draft remains available throughout.
- **Open:** B04's user-resolution controls and any explicitly authorized retry
  semantics, B05 publication identity/permissions, production pagination and
  filtering, and exact draft/intent retention. The experiments establish no
  exactly-once guarantee or safe retry timeout.

GitHub PR creation remains an [agent-execution](../../agent-execution/README.md)
activity. This subsystem may surface issue and PR references for selection but
does not own a PR-delivery workflow.

## Approximate payloads

These are data sketches, not finalized wire schemas; see the
[shared notation](../../README.md#payload-sketch-conventions).

```text
IF-01 IssueContext {
  repository: { host: "github", owner: string, name: string },
  issue: { number: integer, url: string },
  selection: { kind: "user_selected" | "issue_opened_event",
               delivery_id?: string, occurred_at?: timestamp },
  supplied_target_pr?: { number: integer, url: string },
  auth_context_ref?: Ref
}

IF-12 ReviewedIssueProposal {
  proposal_id: string,
  target_repository: { host: "github", owner: string, name: string },
  title: string, body: string, reconciliation_marker: string,
  reviewed_by: Ref, reviewed_at: timestamp,
  source: { run_id: string, trace_ref?: Ref, artifact_refs: Ref[] },
  publication_decision: "publish"
}
IF-12 IssuePublicationResult {
  proposal_id: string, attempt_id: string,
  status: "published" | "failed" | "unknown",
  issue?: { number: integer, url: string },
  error?: { code: string, message: string }
}
```

IF-01 contains references, not frozen issue text; a discovered PR is not
`supplied_target_pr`. IF-12 returns `issue` only after confirmed publication;
`unknown` has no issue reference, even if GitHub may already hold the issue.
The marker is immutable for one reviewed request and must appear exactly once
in its final body; an edit requires renewed review before publication.
IF-01 does not carry unrelated trigger subjects. Duplicate-write handling and
exact authorization binding remain open. A
public repository can be read without `auth_context_ref`; publication still
requires an authorized GitHub identity.
