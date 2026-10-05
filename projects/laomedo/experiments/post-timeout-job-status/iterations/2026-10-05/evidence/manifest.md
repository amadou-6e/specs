---
title: Post-timeout status evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

Hashes below are SHA-256 of **committed Git blob bytes**, not Windows
working-tree copies. The first observation is historical and lacks the
status error code; the amended replication is the direct-capture result.

| Artifact | Revision | SHA-256 | Purpose |
| --- | --- | --- | --- |
| [PROTOCOL.md](https://github.com/amadou-6e/laomedo/blob/c5f2f68df9f869656707c26fa4e08ccbe2ef4ce8/experiments/exp65/PROTOCOL.md) | `c5f2f68` | `d58c03fc20cce2720ecbe779d274cc290f36c991171a2c5bde9059bd5dbd7fcb` | Prospective case, limits, poll schedule |
| [First observation](https://github.com/amadou-6e/laomedo/blob/95e991b5033e88a49fcbbdfe67746d7c8bef743e/experiments/exp65/observation.json) | `95e991b` | `e679860020314f2a3fdb59263b354e6e8bf06f132cf89a16dbbbcb3e684ab9b1` | Four 500s, late effect; code omitted |
| [AMENDMENT-01.md](https://github.com/amadou-6e/laomedo/blob/1c6790a63000bd114278bdf88b04ddff38ef8529/experiments/exp65/AMENDMENT-01.md) | `1c6790a` | `6c963f6b13670aaedf83a4d478bd1471342bf51e6e4a45bd77ff92d0a689597b` | Prospective diagnostic limit |
| [Direct observation](https://github.com/amadou-6e/laomedo/blob/3543a669857fe78f747f94737b3a3f4aba444290/experiments/exp65/observation.json) | `3543a66` | `933e57aed5b58663fe6c20b457cf37e3a99c2b9a692e687632fb37080573a487` | Four `JOB_FAILED` codes and late effect |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/3543a669857fe78f747f94737b3a3f4aba444290/experiments/exp65/probe.py) | `3543a66` | `1cbb29fd752594f440bbe3cfb815e14ac2dc9c6c9d020696816356e8813eec32` | Exact amended capture code |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/3543a669857fe78f747f94737b3a3f4aba444290/experiments/exp65/test_probe.py) | `3543a66` | `04cefc74706979a0a264522a6a18ab3a545ee72ce74175f43982fac631079881` | Four evidence/falsifier checks |

The temporary SQLite database, synthetic token, auto-login state and runner
journal were removed with each disposable named volume. No private raw trace
or credential is committed. The observation preserves response categories,
error codes, UTC/monotonic timing, clock calibration and runner events.
