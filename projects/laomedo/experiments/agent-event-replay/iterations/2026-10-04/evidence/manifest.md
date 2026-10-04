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
[`ff743ce`](https://github.com/amadou-6e/laomedo/commit/ff743ce228b9a419d68f2674d3dc0e7e3931f28e).

| Artifact | Scope | SHA-256 of committed Git blob |
| --- | --- | --- |
| [PROTOCOL.md](https://github.com/amadou-6e/laomedo/blob/c3b46f9a1f9ef4e2b35d5e6a7102615e9eb632de/experiments/exp09/PROTOCOL.md) | Frozen question, cases and falsifiers | `eae4ae54e714df0b6a0993c67289181d0f624d40702bec53af29dd3a5141fdae` |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/ff743ce228b9a419d68f2674d3dc0e7e3931f28e/experiments/exp09/observation.json) | Deterministic sanitized readback | `24aa1338744a1d8b13add1b05045a56e5703961b5334aa5c4510a64020bc4f1d` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/ff743ce228b9a419d68f2674d3dc0e7e3931f28e/experiments/exp09/probe.py) | Synthetic ingest and uncertainty projection | `566dcdafc6f735f45a09832a3a1487d5b2fe7c9a6f0073b0d0e2d90be2d8823b` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/ff743ce228b9a419d68f2674d3dc0e7e3931f28e/experiments/exp09/test_probe.py) | Five acceptance checks and evidence immutability | `d629ee3939e561d118b991f87603d453e89f86f772ab5e056bc2e3cb42ba26da` |

Hashes were computed from Git blobs, not Windows working-tree copies.
`experiments/** text eol=lf` fixes committed line endings. Temporary SQLite
databases were removed by the fixture; no raw model transcript, credential,
personal file or native session was produced.
