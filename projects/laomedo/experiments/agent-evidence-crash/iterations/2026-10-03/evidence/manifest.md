---
title: Agent evidence crash evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

All links pin Laomedo source revision
[`e274903`](https://github.com/amadou-6e/laomedo/commit/e274903242a4f1724fc598ba50de9cff4f433690).
The temporary SQLite databases were deleted after inspection; only sanitized
synthetic readback is retained.

| Artifact | Producer / scope | SHA-256 |
| --- | --- | --- |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/e274903242a4f1724fc598ba50de9cff4f433690/experiments/exp05/observation.json) | Seven child exit/readback cases, including raw/projection correlation | `7c10c154b0571a71a71681c4ef14bfca5dfa2a9b28ef2f1baa445912ad44b7e7` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/e274903242a4f1724fc598ba50de9cff4f433690/experiments/exp05/probe.py) | Child kill points and assertions | `b48d4f1eb9f1eb6b180e4b42fb5c79689aad233a9dff1b8ff53e90a007e79d15` |
| [evidence.py](https://github.com/amadou-6e/laomedo/blob/e274903242a4f1724fc598ba50de9cff4f433690/experiments/exp05/evidence.py) | Synthetic SQLite invocation/raw/projection store | `961ea01de74243da2422e3fb98deca08c72d942adbdb67663c464be26cc0b1a2` |
| [unit tests](https://github.com/amadou-6e/laomedo/blob/e274903242a4f1724fc598ba50de9cff4f433690/experiments/exp05/test_evidence.py) | Identity refusal, native-ID conflict, keyless source preservation, repeat sweep | See pinned source |

No raw model transcripts, provider secrets, or personal file content are in
these artifacts. UUIDs in the observation are synthetic and randomly created
per disposable database.
