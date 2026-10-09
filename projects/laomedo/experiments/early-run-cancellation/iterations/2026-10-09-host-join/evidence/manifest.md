---
title: Playground host join evidence manifest
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
| Reviewed one-turn implementation, protocol and result | [Laomedo `74a2c13f37d8bb3463aff990aca76c06e7504d33`](https://github.com/amadou-6e/laomedo/commit/74a2c13f37d8bb3463aff990aca76c06e7504d33); pre-submission code at `aa12af6` |
| Target contract | [Merged specs `6e7887387c5a0dec786ac2acbf29ee8e640e653f`](../../../../../subsystems/agent-execution/contract/early-run-cancellation.md); this iteration does not mark it accepted |
| Pinned Langflow image | `langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` |
| Sanitized result | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-g-live-20261009-a/sanitized.json`; SHA-256 `ce50e8ecfb91d1755ff3bcf0dbf13ff1d3156bb2eac0685a22ae7fed6a646761` |
| Teardown | Private `teardown.json`; SHA-256 `6bcf12ea19459955330e912d91b1b101a429725eeb975c22c94983609e83f256` |
| Pins and route audits | Private `pins.json` SHA-256 `35b5cca3d1f296bc468f8d8e80ae4db37b158783df8042200cfa9e6897b4043d`; bridge routes `1415cf0cba9896ea04f49624c1da03c5bfd95d6fc6f357a0b82180f4b90a5c27`; runner routes `b480f442ceb46d20f8e161076859c030a0a5904d336bad6ce9756dcd41ff92e5` |
| Native event file | Private, 25 raw events; SHA-256 `63396d5b94d116adbaeaa031b549bddb707c7b0bc4a5c8de9ca006e64804b8f7`; contents not committed |
| Shared ledger | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; one new attempt recorded `real_join_inconclusive`, total 7/12 |

The private directory also contains the disposable bridge and runner tokens,
browser profile and SQLite stores. No raw transcript, token value, credential
file or browser profile is published.
