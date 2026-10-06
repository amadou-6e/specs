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
| Six native turn records, raw events and cumulative turn ledger | Subscription-backed Codex runner | Private runner state outside Git; status and count in [results](../results.md) | Private only for raw events and credentials |
| Safe fourth-turn error summary and fifth-turn direct success | Fixed-schema runner projection and private login refresh | Sanitized categories in [execution](../execution.md); private raw events retained | Repository summary and private evidence |
| Final completed native thread and failed artifact selection | Isolated Langflow flow and runner | Private workflow run `bad38e64-6558-4c91-8185-743f8527ab05`; sanitized outcome in [execution](../execution.md) | Private files and repository summary |
| Verified agent artifact and `test/49` draft PR | Not produced because the final turn left no output file | None | Not observed |

The private failed attempts are retained separately. No raw message, credential, runner token, or unreviewed generated text is committed.
