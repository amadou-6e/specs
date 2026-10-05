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

## Amended negative-control evidence

Review identified a tautological uncertainty assertion. Amendment 01 was
committed at [`8bb8e5d`](https://github.com/amadou-6e/laomedo/commit/8bb8e5d)
before the revised probe ran. The amended artifacts are pinned to
[`e285068`](https://github.com/amadou-6e/laomedo/commit/e285068e0eba9f6750a0617591457e42cd230b6d);
the original evidence table above remains the historical first run.

| Artifact | Scope | SHA-256 of committed Git blob |
| --- | --- | --- |
| [AMENDMENT-01.md](https://github.com/amadou-6e/laomedo/blob/e285068e0eba9f6750a0617591457e42cd230b6d/experiments/exp09/AMENDMENT-01.md) | Prospective falsifying control | `6e1cec4fd1d05059fbe2d07b9bfd2e5c9fe485d49822c19e51c81bb4ac0cb92f` |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/e285068e0eba9f6750a0617591457e42cd230b6d/experiments/exp09/observation.json) | Revised deterministic readback and control failures | `e266575e16a15b947b02dbe2fa8ea6b0c4e9e84eb84b5e85940e4080d2c02ffe` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/e285068e0eba9f6750a0617591457e42cd230b6d/experiments/exp09/probe.py) | Shared oracle and historical comparator | `93ff92fa05ed91cde20eab104ddb68859bfa0220692176fb5b1d3efc798a894f` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/e285068e0eba9f6750a0617591457e42cd230b6d/experiments/exp09/test_probe.py) | Six checks, including rejection assertions | `fef852632b48d6b2b0a7d9a01571a3b3060576e60136099dc8de21c0b46d70b5` |
