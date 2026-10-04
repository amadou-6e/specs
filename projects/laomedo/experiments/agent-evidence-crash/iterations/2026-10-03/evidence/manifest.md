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
[`9e0bbca`](https://github.com/amadou-6e/laomedo/commit/9e0bbca7a35727be88d7815d2799c9d359a4a848).
The temporary SQLite databases were deleted after inspection; only sanitized
synthetic readback is retained.

| Artifact | Producer / scope | SHA-256 |
| --- | --- | --- |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/9e0bbca7a35727be88d7815d2799c9d359a4a848/experiments/exp05/observation.json) | Seven child exit/readback cases, including raw/projection correlation | `837b450971628bcbfc3d36fded2f36f13b3e4cf14bb46fb80bdd010a44177129` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/9e0bbca7a35727be88d7815d2799c9d359a4a848/experiments/exp05/probe.py) | Child kill points and assertions | `3f436cdff2d83087138d0b78bfa2ae9e9af1aea14fba90f27c756bd8122aa1da` |
| [evidence.py](https://github.com/amadou-6e/laomedo/blob/9e0bbca7a35727be88d7815d2799c9d359a4a848/experiments/exp05/evidence.py) | Synthetic SQLite invocation/raw/projection store | `961ea01de74243da2422e3fb98deca08c72d942adbdb67663c464be26cc0b1a2` |
| [unit tests](https://github.com/amadou-6e/laomedo/blob/9e0bbca7a35727be88d7815d2799c9d359a4a848/experiments/exp05/test_evidence.py) | Identity refusal, native-ID conflict, keyless source preservation, repeat sweep | `850f5df0d8651d47b65347f7a8867e4e9f48d5757b961cf044a721dc67a5a15f` |

No raw model transcripts, provider secrets, or personal file content are in
these artifacts. UUIDs in the observation are synthetic and randomly created
per disposable database. Hashes refer to committed Git blobs, not Windows
working-tree copies. The explicit `--record` mode writes LF line endings.
