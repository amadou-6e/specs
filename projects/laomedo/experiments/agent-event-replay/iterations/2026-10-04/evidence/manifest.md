---
title: Agent-event replay evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

The prospective protocol was committed at Laomedo
[`c3b46f9`](https://github.com/amadou-6e/laomedo/commit/c3b46f9a1f9ef4e2b35d5e6a7102615e9eb632de)
before execution. Probe, tests and observation are pinned to
[`3115d5b`](https://github.com/amadou-6e/laomedo/commit/3115d5bec3f15f250f5b1605873185e537cbe3d4).

| Artifact | Scope | SHA-256 of committed Git blob |
| --- | --- | --- |
| [PROTOCOL.md](https://github.com/amadou-6e/laomedo/blob/c3b46f9a1f9ef4e2b35d5e6a7102615e9eb632de/experiments/exp09/PROTOCOL.md) | Frozen question, cases and falsifiers | `eae4ae54e714df0b6a0993c67289181d0f624d40702bec53af29dd3a5141fdae` |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/3115d5bec3f15f250f5b1605873185e537cbe3d4/experiments/exp09/observation.json) | Deterministic sanitized readback including synthetic call IDs | `e7ba27636180aa8e005cb138a388a0fc1df29092ad411f8ea900541b696b6b7a` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/3115d5bec3f15f250f5b1605873185e537cbe3d4/experiments/exp09/probe.py) | Synthetic ingest and uncertainty projection | `cbf7260b853d488524968eaf67158dad8d772358b775bae7f4472f1baf28969d` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/3115d5bec3f15f250f5b1605873185e537cbe3d4/experiments/exp09/test_probe.py) | Five acceptance checks and evidence immutability | `672f2c34d66c85a14617c0c935f22f97194107f87bbeb581d5aa6cf399b636d7` |

Hashes were computed from Git blobs, not Windows working-tree copies.
`experiments/** text eol=lf` fixes committed line endings. Temporary SQLite
databases were removed by the fixture; no raw model transcript, credential,
personal file or native session was produced.
