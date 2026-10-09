---
title: Playground host join with a failed real Codex turn
status: draft
kind: experiment-iteration
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# 2026-10-09 host join

Read the [execution record](execution.md), [bounded result](results.md), and
[evidence manifest](evidence/manifest.md). Disposable fake-runner tests passed
the persisted host and Langflow restart join. One later real Codex request
traversed the visible Playground and host bridge, but failed before an agent
tool call; no visible Stop was clicked. This iteration uses 7/12 of the shared
EXP-22 ledger and does not close #22/Q11.
