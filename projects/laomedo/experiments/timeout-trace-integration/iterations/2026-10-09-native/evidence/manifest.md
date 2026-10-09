---
title: Native reconciliation prospective pins
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Prospective pins

| Artifact | Pin / access |
| --- | --- |
| Frozen protocol/source | Laomedo add96614a73f19d6dd64c321635d5100a96d5aa9; experiments/exp66/NATIVE-PROTOCOL.md and native_probe.py |
| Current pre-review implementation | [b2e98a0](https://github.com/amadou-6e/laomedo/commit/b2e98a0b9266ef9aecfd67e8a8536a818af2ab00); no native execution yet |
| Base | develop bd285cf792c5faa20d5effe7e55aa720a2c833b6; no unmerged #97/#105 dependency |
| Runtime/model | Codex0.159.2, gpt-6-luna/low, approved private non-split profile |
| Timing | Host monotonic resolution and wall bracket, no cross-machine inference |
| Ledger | Shared cap12, used10; one case each, no retries |

Raw native events, credentials, profiles, runner stores and tokens stay outside
Git. Publish sanitized findings, hashes and exact cleanup verification. Preserve
negative/inconclusive outcomes. No semantic success, global effect completeness,
production login lifecycle or #93 outage/real-push revocation claim.
