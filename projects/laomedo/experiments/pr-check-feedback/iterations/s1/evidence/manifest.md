---
title: PR-check feedback S1 evidence
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

All artifacts below are public sanitized committed bytes at Laomedo
`4ab1d55cf0efed6de96ebbb045b808044cfa31cb`; no private state is needed.
This support directory belongs to S1, not an independent collection.

| Artifact | Producer and identity | SHA-256 / verification | Access |
| --- | --- | --- | --- |
| [Controller report](https://github.com/amadou-6e/laomedo/blob/4ab1d55cf0efed6de96ebbb045b808044cfa31cb/experiments/exp123/observation-s1.json) | Frozen probe, exp123-S1 | `747466ac11396d62e7e2c995f44e54fff382bd50eaf7071b5255307f778abf49` | Public; derived, not primary engine evidence |
| [Raw journal](https://github.com/amadou-6e/laomedo/blob/4ab1d55cf0efed6de96ebbb045b808044cfa31cb/experiments/exp123/evidence/S1/journal.jsonl) | Fixture store and graph component events | `ad6501e525535349f403d073350678ffb0117ce9804c7594c60ccc9fae0f7f29` | Public; LF bytes |
| [Seven case and seven flow snapshots](https://github.com/amadou-6e/laomedo/tree/4ab1d55cf0efed6de96ebbb045b808044cfa31cb/experiments/exp123/evidence/S1) | Controller capture of worker outputs | All fourteen byte hashes in controller report; flows match pre-arun graph_started hashes, cases reconstruct from journal | Public; no tokens or personal sessions |
| [Read-only replay test](https://github.com/amadou-6e/laomedo/blob/4ab1d55cf0efed6de96ebbb045b808044cfa31cb/experiments/exp123/test_evidence.py) | Post-run check, not new runtime evidence | Verifies all15 capture hashes, report hash, source assessment, terminal node and branch order | Public; never writes observations |
