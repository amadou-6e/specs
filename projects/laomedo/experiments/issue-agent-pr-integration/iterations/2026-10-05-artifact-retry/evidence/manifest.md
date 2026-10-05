---
title: EXP-19 artifact retry evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Artifact | Producer | Location | Access |
| --- | --- | --- | --- |
| Historical 6/6 ledger and additional four-turn grant | Explicit user grant and private runner | Private runner state; bounds in [execution](../execution.md) | Private files and repository summary |
| First attempt's missing-directory command result | Read-only inspection of private native trace | Failed run `4c6e709f-aa19-40c3-a4e5-695f68988d00`; sanitized finding in [execution](../execution.md) | Private raw trace and repository summary |
| Agent-originated nested-write canary at turn 7/10 | Private Codex runner | Native run `b1aeca41-3efb-4e34-8142-5ca86530dde4`; outcome in [results](../results.md) | Private raw trace and repository summary |
| Output-parent fixture and source-integrity regression | Laomedo `42c8a5f` | Checked-in source fixture and test | Repository |
| New issue/graph/flow plan and Langflow run | Read-only preparation and turn 8/10 | Private plan, imported flow, run and trace; sanitized IDs in [execution](../execution.md) | Private files and repository summary |
| Verified report and `test/49` draft PR | Agent output and trusted host publisher | [Draft PR #71](https://github.com/amadou-6e/laomedo/pull/71), commit `769b47b36572251f702cf7e84674f96316d8bdde`; private byte-for-byte comparison | Repository report and private binding |

The turn 7 canary was disposable diagnostic output and was not published. Only the verified turn 8 report appears in PR #71. Raw rollouts and login material remain private.
