---
title: Issue inspection and bounded agent operations
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-13
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue inspection and bounded agent operations

Tracking: specs #376, Laomedo #162. Owner-interview inventory retains decision
0009 (ALL-label filtering, live connection, close/title/body/labels operations).
Goal/map for this small clarification: inspect the selected issue -> open its
GitHub page -> observe a real agent-directed operation. UI choices were supplied
directly by the owner; only the exact mutation/cap approval was asked.

Confirmed: replace Code on GitHub Issue with a viewer tab and an open-in-browser
tab. The owner explicitly approved changing disposable issue #15 to title
"Filter demo: agent updated", adding question and appending a short
"Agent operation verified" section, then closing disposable #12, under four
submitted Codex turns including timeouts with the existing subscription login.
Repository: ga84jog/laomedo-exp104-disposable-20261007. No other mutation is covered.

The [node contract](../subsystems/issue-integration/contract/langflow-node.md)
and [editable states](../subsystems/issue-integration/design/github-issue-node.drawio)
own the UI. The configuration for the real demonstration must be prepared,
reviewed and approved separately; the current read-only connection stays disabled
for writes until that step. User approval is a bounded local campaign decision,
not a new production authentication policy.
