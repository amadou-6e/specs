---
title: Develop-based integration evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Artifact | Pin / location |
| --- | --- |
| Frozen protocol and implementation | [Laomedo source 7b5d009](https://github.com/amadou-6e/laomedo/tree/7b5d009b6a3fe8ffc84c167e901f64587bfe1a91/experiments/exp117); initial protocol 8923e1f, reviewed guards aa850f2 |
| Machine findings | Published with Laomedo #117 at experiments/exp117/observations.json; retains original summaries, pins, teardown, private artifact hashes and retrospective amendment |
| Native CLI | Codex 0.159.2 image ID sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239 |
| Langflow | 1.12.3 image langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0 |
| Pre-thread native event file | Empty; SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| Active native event file | 78 private events; SHA-256 e6ce882bb633fc6e90b1a72d3ddccb547f6a89694a95089c8ee58187bb7fe465 |
| Retrospective public-output equality | SHA-256 c0d66b6fbffe7b2b64a6d9978e5b91fae071d6fbe87d07c3689dfbc8228a4aa4; no raw event published |
| Shared ledger | Preserved original categories; 10/12, no repeat or redispatch |

Private producer artifacts are under %LOCALAPPDATA%/Laomedo/exp117-prethread-20261009-a/
and exp117-active-20261009-a/. Credentials, native transcript bodies, browser
profiles and databases are not public artifacts. The joined saved-flow UUID
and reported graph-run ID are corroboration, not graph-execution attestation.
