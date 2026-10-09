---
title: Detached-stage evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-08
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Artifact | Pin and access |
| --- | --- |
| Frozen implementation, amendment and probe inputs | Laomedo commit `bc842f9`; [amendment](https://github.com/amadou-6e/laomedo/blob/bc842f9/experiments/exp22/PHASE-C-DETACHED-AMENDMENT.md), [preflight](https://github.com/amadou-6e/laomedo/blob/bc842f9/experiments/exp22/PHASE-C-DETACHED-PREFLIGHT.md) |
| Published result | [Laomedo `bfc6289`](https://github.com/amadou-6e/laomedo/blob/bfc6289c9741791cc4728e7bc9906356fb392ce9/experiments/exp22/PHASE-C-DETACHED-RESULTS.md) |
| Container image | `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239` |
| Third-turn sanitized observation | Run `09dc64d0-5328-4376-8271-7925e6c557f8`; private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-kill-detached-bc842f9/kill-sanitized.json` |
| Raw event integrity | SHA-256 `31b27c21a40ecf34a00edaa35cf23f772fea374d7ed5682e0c4972d48961b66c`; raw events private, not committed |
| Shared turn ledger | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; cap 4, used 3 |
| Host suite | 354 passed, 9 skipped before model submission; focused tests passed after final wording correction |

No token, grant, raw trace, login file or provider response is published.
