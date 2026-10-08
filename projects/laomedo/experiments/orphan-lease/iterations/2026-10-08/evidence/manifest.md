---
title: Integrated Codex and orphan lease evidence
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-08
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Artifact | Producer and revision | Location and access |
| --- | --- | --- |
| Phase C protocol and probes | Laomedo commits `fca851a`, `2dcb19b`, `e054a98` | [Protocol](https://github.com/amadou-6e/laomedo/blob/fca851a/experiments/exp22/PHASE-C-PROTOCOL.md) and [probe folder](https://github.com/amadou-6e/laomedo/tree/e054a98/experiments/exp22); source commits precede their corresponding turns |
| Active-turn sanitized observation | Local runner and fake host at `2dcb19b`; run `4efedca5-3a28-4d1e-bb64-c6862d729ea1` | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-active-2dcb19b/active-sanitized.json`; raw trace SHA-256 `35e1f52d2b5d130d5668e460c877f7196d3d0fbd6be702661bd9136e09ca715c` |
| Kill-turn sanitized observation | Local runner, lease service and fake host at `e054a98`; run `907533a4-6e04-46e7-ba73-dd744709246b` | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-kill-e054a98/kill-sanitized.json`; raw trace SHA-256 `93b3c2c516299aa802773af38a16fdc685575b8398adaec99973aae87c23d723` |
| Shared turn ledger | Bounded probe; cap 4, used 2 | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; counts only are published |
| Host regression suite | Laomedo `e054a98` | `python -m unittest discover -s tests -q`: 352 tests passed, 9 skipped |

The private folders also hold raw events, input pins and credential state. They are intentionally not committed. The summary publishes no token, raw trace, provider response or credential-bearing file.
