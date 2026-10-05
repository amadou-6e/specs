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
| Agent-originated nested-write canary at turn 7/10 | Private Codex runner | Native run `b1aeca41-3efb-4e34-8142-5ca86530dde4`; outcome in [results](../results.md) | Private raw trace and repository summary |
| Output-parent fixture and source-integrity regression | Laomedo `42c8a5f` | Checked-in source fixture and test | Repository |
| New issue/graph/flow plan and Langflow run | Pending preparation and dispatch | Private state outside Git | Not yet observed |
| Verified agent report and `test/49` draft PR | Pending exact artifact gate and host publication | None | Not yet observed |

The canary file is disposable diagnostic output. It is not the selected issue report and must not be published.
