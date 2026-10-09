---
title: Installed Langflow graph cancellation evidence
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
| Frozen tested implementation and protocol | Laomedo `bda5a6b9f4ac27a4f5be99fb4901496355d9907e`; [Phase D protocol](https://github.com/amadou-6e/laomedo/blob/bda5a6b9f4ac27a4f5be99fb4901496355d9907e/experiments/exp22/PHASE-D-LANGFLOW-PROTOCOL.md), [preflight](https://github.com/amadou-6e/laomedo/blob/bda5a6b9f4ac27a4f5be99fb4901496355d9907e/experiments/exp22/PHASE-D-PREFLIGHT.md) |
| Published result | [Laomedo `a0a25d3`](https://github.com/amadou-6e/laomedo/blob/a0a25d304a18466e3f1446cbd10e317a303e3525/experiments/exp22/PHASE-D-RESULTS.md) |
| Pinned images | Codex `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239`; Langflow `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` |
| Skill and run | `sha256:a12c212a57a9bc8fa3f0ecd834c09f9576a37ee89e21c62a096b1213fcc2bef8`; run `a736386d-1aae-4970-b7f8-32698eb4e442` |
| Raw native events | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-d-live-bda5a6b/runner/runs/<run-id>/raw-events.jsonl`; 55 records, SHA-256 `9bf7cf2f81f2f2c90ab021e0c6330bd3572e7bc38f346c78abe1afcd7a6ab26d` |
| Sanitized result and teardown | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-d-live-bda5a6b/`; `sanitized.json` SHA-256 `68be642a10ba9f3d22432fd044f760406af448a86590cb604ba7f8aa1eab29f4`; `teardown.json` SHA-256 `814a2f0a2b56bd44f538322d7f894ec6a2fea6627d5ab8d0f71b7a4979ec677d` |
| Route audit | Private `runner-routes.jsonl` SHA-256 `923863e79fd141869362d69f204c79b7ba63a1bd3b036afd559d9f1b25a1975d` |
| Shared turn ledger | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; cap 4, used 4 |

Raw traces, runner token and provider-login copy are intentionally not committed. The private graph log, graph result, route journal and sanitized outputs were scanned for the runner API token without publishing its value; none contained it. This scan does not establish hosted credential isolation.
