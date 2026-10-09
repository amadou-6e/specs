---
title: Host join and Stop evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Artifact | Pin and access |
| --- | --- |
| Protocol before submission | [Laomedo `85ddbf998e5248a5acd9f6dd74ebc21b10171b80`](https://github.com/amadou-6e/laomedo/commit/85ddbf998e5248a5acd9f6dd74ebc21b10171b80); substantive amendment at `26e37ad`, followed only by a historical-count wording clarification |
| Result and diagnosis | [Laomedo `266536fefa856c02d2482445387b83289ad069d1`](https://github.com/amadou-6e/laomedo/commit/266536fefa856c02d2482445387b83289ad069d1) |
| Langflow image | `langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` |
| Codex image | `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239`, CLI 0.159.2 |
| Sanitized result | Private `sanitized.json`, SHA-256 `c0354838ad5857f1e014256af929a1a662d8a7eaa42dc19564cf3ca2e5c21416` |
| Teardown | Private `teardown.json`, SHA-256 `c1c6fee74f805ca1f4f3e166f550faefc1f48bb803391dff3a8cad6b5d53a57c` |
| Pins | Private `pins.json`, SHA-256 `b05f7060cc85fecab947651839005161b9231b7cfc25a5efb74881f4e245e948` |
| Bridge route audit | Private `bridge-routes.jsonl`, SHA-256 `14a49192e19e1bf6ae356415c1372a74d30d3019f1f0d39c4079bb636615507b` |
| Runner route audit | Private `runner-routes.jsonl`, SHA-256 `54660716460bed59466cca67518007574a735b37317b9f7cd58f3adc77247078` |
| Native event file | Private, 87 events, SHA-256 `e428fb5551b30db636fa22d9196fb2795ac36fe23606eb8425ab12d5d2c3ba23` |
| Shared ledger | Private EXP-22 ledger, result `real_join_visible_stop_passed`, 8/12; one fresh submission after the retained failed attempt |

Run artifacts are under
`%LOCALAPPDATA%/Laomedo/exp22-phase-g-live-20261009-b/`. Credential and browser
profile contents, raw provider responses and native transcripts are not
published. The trace match is corroboration, not graph-execution attestation.
