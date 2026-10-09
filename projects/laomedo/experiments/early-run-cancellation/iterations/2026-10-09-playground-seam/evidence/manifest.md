---
title: Visible Playground host-bridge seam evidence
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
| Design, probe and bounded result | [Laomedo `6c6bf37`](https://github.com/amadou-6e/laomedo/commit/6c6bf37558fbafb2697f6e6c279a19cdcad49a5c) |
| Pinned Langflow image | `langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` |
| Probe source | SHA-256 `f04ba933c49f619519db37878862d32db8d832d9533b2467a00b4f362882ee5b` |
| Five-node flow | SHA-256 `58fb018b5043c645744b375d0b2f015130b2d84ca0ccf99946bfd40b7ada69ed` |
| Sanitized summary | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-g-seam-20261009-c/sanitized.json`; SHA-256 `65e0e570031b7a06e67eadd13e2d3904919543f9d4146b375e0f77b03f331126` |
| Teardown | Private `teardown.json`; SHA-256 `79117d2947f6a5fe30930df59b989c3d992a201df004db7c7abede5e0ee53af5`; container absent and fake bridge stopped |
| Shared authorization ledger | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; unchanged at 6/12, with zero model calls for this iteration |

The private state includes the disposable bridge token, browser profiles and
SQLite data. The sanitized summary and teardown were checked not to contain
the token. No raw browser trace or credential is committed.
