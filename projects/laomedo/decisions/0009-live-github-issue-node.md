---
title: Live GitHub Issue selection and incoming operations
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-13
applies_to: [laomedo]
supersedes: null
related: []
---

# Live GitHub Issue selection and incoming operations

Tracking: [specs #374](https://github.com/amadou-6e/specs/issues/374),
[Laomedo #160](https://github.com/amadou-6e/laomedo/issues/160).

## Context and source

The owner rejected the saved Frozen GitHub Issue fixture as the product experience
on 2026-10-13. This is a reconstructed record of answers in the current Codex
conversation, not a claim that the earlier questions followed a complete interview.
The owner-interview skill was read before recording this in the visible docs/374 branch.
Existing IF-01 already distinguishes issue references from frozen text; decisions
0004 and 0008 retain mediation, lease/revocation and unknown-write constraints.

Goal/map: live selection -> filtered issue -> current data -> graph operation.
The owner supplied the scenario and settled the two implementation-blocking choices.

## Confirmed decisions

- Name the product node GitHub Issue. Use a live GitHub connection and a repository
  URL rather than base64 issue/task inputs.
- Discover labels into a multi-select dropdown. Filter selectable issues by ALL
  selected labels, not any label. Empty labels impose no label restriction.
- An incoming node can supply an operation for the selected issue, including close
  and modify. Modify includes title, body and labels.
- Preserve run evidence internally, but do not require the user to prepare frozen
  issue content as the connection mechanism.

## Consequences and boundaries

The [node contract](../subsystems/issue-integration/contract/langflow-node.md) owns
payloads and outcomes. The [editable node states](../subsystems/issue-integration/design/github-issue-node.drawio)
own the controls. Live reads and scoped writes are distinct; a selected issue or
incoming message alone does not confer a GitHub write capability. Existing host
connection and expiring grants apply, without a second approval sign-in.
The historical FrozenIssue fixture and its prior evidence are not relabelled live.

## Open/later

Webhooks, auto-dispatch from new issues, delete/reopen/comment operations and bulk
issue operations are outside this slice. No new live issue write is authorized by
this design record. Concrete deployment and disposable write acceptance are gated.
