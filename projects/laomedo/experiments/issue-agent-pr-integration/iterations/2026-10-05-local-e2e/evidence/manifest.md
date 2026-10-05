---
title: EXP-19 local end-to-end evidence manifest
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
| Frozen issue, graph, flow, runner and skill pins | Read-only preparation at Laomedo `7697588` | Private plans and graph snapshots; sanitized hashes in [execution](../execution.md) | Private files and repository summary |
| Six-turn and one-draft-PR grant | Explicit user grant | Private `grant.json`; bounds summarized in [execution](../execution.md) | Private file and repository summary |
| Imported Langflow flow and exported graph digest | Isolated localhost Langflow | Private flow-import records; sanitized ID in [execution](../execution.md) | Private files and repository summary |
| Three native run records, raw events and cumulative turn ledger | Subscription-backed Codex runner | Private runner state outside Git; status and count in [results](../results.md) | Private only for raw events and credentials |
| Verified agent artifact and `test/49` draft PR | Not produced because all model turns failed | None | Not observed |

The private failed attempts are retained separately. No raw message, credential, runner token, or unreviewed generated text is committed.
