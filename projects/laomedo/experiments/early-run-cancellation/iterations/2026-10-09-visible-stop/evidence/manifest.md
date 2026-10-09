---
title: Visible Playground Stop evidence
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
| Frozen tested implementation and protocol | Laomedo `35a7d3c3f5518e5479b18b9d78a2f67c9b9394ac`; [Phase E protocol](https://github.com/amadou-6e/laomedo/blob/35a7d3c3f5518e5479b18b9d78a2f67c9b9394ac/experiments/exp22/PHASE-E-UI-PROTOCOL.md) and [preflight](https://github.com/amadou-6e/laomedo/blob/35a7d3c3f5518e5479b18b9d78a2f67c9b9394ac/experiments/exp22/PHASE-E-PREFLIGHT.md) |
| Published result | [Laomedo `7460da3`](https://github.com/amadou-6e/laomedo/blob/7460da39ee4d2922469e04895adf4d56de32615c/experiments/exp22/PHASE-E-RESULTS.md) |
| Pinned images | Codex `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239`; Langflow `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` |
| Skill and identity | Skill `sha256:a12c212a57a9bc8fa3f0ecd834c09f9576a37ee89e21c62a096b1213fcc2bef8`; run `448e4385-fca4-41cb-8f2f-d5e4815357e7`; request `062358bd-3e02-48d9-8f82-37d780e5152f` |
| Native events | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-e-live-35a7d3c/runner/runs/<run-id>/raw-events.jsonl`; 61 records, SHA-256 `483362dee4e51c398f195c942bbf7a115f058838afbaa64504b6e78ec32ef6f1` |
| Sanitized result and teardown | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-e-live-35a7d3c/`; `sanitized.json` SHA-256 `67ba03cbf71baf41f67c7324954e1a161f770339af93f7eb7e2f9b5a7493f837`; `teardown.json` SHA-256 `897931ae5e8daef0e39519890410fefe0ba412a58da93a9ea8bf24d665af4c65` |
| Route audit and pins | Private `runner-routes.jsonl` SHA-256 `8c9f6a2896e57691ee81015bf79dfde90a9579d42f43b8b4b8eb35ff3ab5160f`; `pins.json` SHA-256 `131bc8da4a2b198d3c1d87f708dbe1cecdffde2190e59cec725e135fd213564e` |
| Shared turn ledger | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; cap 12, used 5 |

Raw traces, browser profile, runner token and provider-login state are not committed. The private browser log/result and sanitized result/teardown were scanned for the runner API token without publishing its value; none contained it. This scan does not establish hosted credential isolation.
