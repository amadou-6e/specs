---
title: Timeout trace integration evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

Hashes are SHA-256 of **committed Git blob bytes**, not Windows working-tree
copies. The first observation is historical and lacks the full source row;
the amended replication is the direct-capture result.

| Artifact | Revision | SHA-256 | Purpose |
| --- | --- | --- | --- |
| [PROTOCOL.md](https://github.com/amadou-6e/laomedo/blob/2a2a1ad/experiments/exp66/PROTOCOL.md) | `2a2a1ad` | `e9cd1ea610220b66974b3eed4635183bc6af07f536b7927bf85fdedc8af6d594` | Prospective question and limits |
| [First observation](https://github.com/amadou-6e/laomedo/blob/19f823d/experiments/exp66/observation.json) | `19f823d` | `d439f0dc6cc5e4044e1601ceda68b20fc3fe9273a99c9a76ea0751f857afad22` | Historical timeout, statuses and effect; source hash not independently verifiable |
| [AMENDMENT-01.md](https://github.com/amadou-6e/laomedo/blob/95c1121/experiments/exp66/AMENDMENT-01.md) | `95c1121` | `f49a48f3d488fe0906f00031755abaab59fea6342b179644a2dd68fd5d21255c` | Prospective source-row capture change |
| [Amended probe.py](https://github.com/amadou-6e/laomedo/blob/a885197/experiments/exp66/probe.py) | `a885197` | `09f165c9d40954f60ef0613751cafb0891cc3d4fa13a61c7468cea82cebc29e2` | Exact direct-capture code |
| [Direct observation](https://github.com/amadou-6e/laomedo/blob/076030c/experiments/exp66/observation.json) | `076030c` | `3a842e283fff276fe3293604e1c2d8e0c3fbc4df7c9e7166247d9becedf67695` | Eight durable receipts and source row |
| [Falsifying tests](https://github.com/amadou-6e/laomedo/blob/076030c/tests/test_exp66_probe.py) | `076030c` | `f8ee488aaaa103a1a9bd42b4c6d84b62b4417fc313c80912eeb0946b5d9e28fe` | Direct capture and mutation checks |

The temporary SQLite store, synthetic token, runner journal and disposable
Docker container/volume were removed. No credential or raw personal trace is
committed.
