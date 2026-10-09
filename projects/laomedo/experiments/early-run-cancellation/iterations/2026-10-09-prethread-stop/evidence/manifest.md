---
title: Visible pre-thread Stop evidence
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
| Frozen tested source and protocol | Laomedo `0b3053f2029fd754eb2e9abb2f720be397ab97e3`; [Phase F protocol](https://github.com/amadou-6e/laomedo/blob/0b3053f2029fd754eb2e9abb2f720be397ab97e3/experiments/exp22/PHASE-F-PRETHREAD-PROTOCOL.md), [preflight](https://github.com/amadou-6e/laomedo/blob/0b3053f2029fd754eb2e9abb2f720be397ab97e3/experiments/exp22/PHASE-F-PREFLIGHT.md) |
| Published result | [Laomedo `6d9dbc8`](https://github.com/amadou-6e/laomedo/blob/6d9dbc8076bf7e41b64c55cfb662f07db6ee2fa9/experiments/exp22/PHASE-F-RESULTS.md) |
| Pinned images and skill | Codex `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239`; Langflow `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`; skill `sha256:a12c212a57a9bc8fa3f0ecd834c09f9576a37ee89e21c62a096b1213fcc2bef8` |
| Run and request | Run `c7125957-1958-4158-a4d3-187f068b1a36`; request `f43ad59d-5087-4f5f-901a-2c3b7a6da2cd`; no native raw events or runner turn-ledger file |
| Sanitized result and teardown | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-f-live-0b3053f/`; `sanitized.json` SHA-256 `6885d478e567fbccad079a434aa4559c44b0394d78acc1d6eecef0a68d29ef7d`; `teardown.json` SHA-256 `fe1b8ab0870dbf91cb953159d0fb26caf3321b98d838ad677547c48ce738dcc4` |
| Route audit and pins | Private `runner-routes.jsonl` SHA-256 `5415fb4f941a75d38fa6824295399bb4c499467df846754019c3f57b22f3cb6f`; `pins.json` SHA-256 `ffa00c79c05a7b507b81de2ee9f121642c49d8a29efae9bcb3a1b4864278fbfc` |
| Shared authorization ledger | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; cap 12, used 6, zero native model calls in this entry |

Raw browser state, runner token and provider login are not committed. The private browser log/result and sanitized result/teardown were scanned for the runner API token without publishing it; none contained the token.
