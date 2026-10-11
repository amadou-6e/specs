---
title: S3 evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-11
applies_to: [laomedo]
supersedes: null
related: []
---

# S3 evidence manifest

| Artifact | Producer / immutable pin | Hash / access |
| --- | --- | --- |
| Original machine observation | Probe, [original](https://github.com/amadou-6e/laomedo/blob/1024ce3a27a4868e97c3cd114d5fdacaf3e791e0/experiments/exp93/real-stage-s3-observation.json) | SHA256 f5ac3861beb6750a3df46b4251687201761281e15dd277e9a48272aa4c5ea1f8; exact original LF bytes |
| Protocol | Coordinator, [frozen protocol](https://github.com/amadou-6e/laomedo/blob/1024ce3a27a4868e97c3cd114d5fdacaf3e791e0/experiments/exp93/REAL-STAGE-S3-PROTOCOL.md) | Commit596b356 preceded source93009f4; runtime SHA2567d71c019f399da5a7bb7eeb4950d068effe52567ae93dbc6c6706d330943e8e2 |
| Producer report | Coordinator, [results](https://github.com/amadou-6e/laomedo/blob/1024ce3a27a4868e97c3cd114d5fdacaf3e791e0/experiments/exp93/REAL-STAGE-S3-RESULTS.md) | Derived interpretation, not primary capture |
| Native partial stream | Native runner, private raw-events.jsonl | SHA256843d510eeb2d06b99e9603182f10551b6f86ad554344a8723b9bef6a3826aee8;37events, private audit retention |

Named reservation/label values and native transcript remain in private durable state, not public artifacts. Exact original container ID is public.73 selected private files scanned with0secret hits, not a global credential audit. OriginalS1/S2/D1 remain unchanged. Coordinator checked hashes/chronology; reviewer read originals and interpreted bounded result but did not independently hash/fetch earlier records.
