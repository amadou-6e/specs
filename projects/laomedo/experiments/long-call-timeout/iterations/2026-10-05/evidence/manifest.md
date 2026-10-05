---
title: Long-call timeout evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

Prospective protocol: Laomedo
[`e4f4685`](https://github.com/amadou-6e/laomedo/commit/e4f4685e0a58d3825ab6c6c7175e57fff3ca116a).
Historical first-run observation, probe and checks: Laomedo
[`dee05c2`](https://github.com/amadou-6e/laomedo/commit/dee05c2532de264796cccdc0543b658b0770d966).

The first observation below was manually condensed after its live capture.
It is preserved as historical evidence, not represented as a direct output
of the final capture code.

| Artifact | Scope | SHA-256 of committed Git blob |
| --- | --- | --- |
| [PROTOCOL.md](https://github.com/amadou-6e/laomedo/blob/e4f4685e0a58d3825ab6c6c7175e57fff3ca116a/experiments/exp10/PROTOCOL.md) | Frozen cases, limits and falsifiers | `f24c66929a17111db16a9ac9fd1acf89b35962a2d576cb2e145cb16864d77879` |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/dee05c2532de264796cccdc0543b658b0770d966/experiments/exp10/observation.json) | Sanitized caller responses, UTC effects and effective timeout | `c69701f13fc01b2081e201d81a0ca7c5b19a5412aa0205bedcb094eeed71e486` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/dee05c2532de264796cccdc0543b658b0770d966/experiments/exp10/probe.py) | Pinned Docker/Langflow harness and compact capture | `1fe67f4da0624af43ce5fb557a290a695cb35b91163dde8ef8b93208958b82e2` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/dee05c2532de264796cccdc0543b658b0770d966/experiments/exp10/test_probe.py) | Four evidence and falsifying-mutation checks | `6002566e7fe33a9b45ad3a15e513886d5546dcc763139c5ded5bca04d18a5a56` |

## Direct-capture replication

Amendment 01 was committed at
[`8ceb50d`](https://github.com/amadou-6e/laomedo/commit/8ceb50de3c9e820b04268543bba9410dd82c31f1)
**before** the separate four-call run. The current compact observation was
written directly by the probe and committed at
[`1fc002a`](https://github.com/amadou-6e/laomedo/commit/1fc002a2837dc8e4c86c6c6c1cddf2e48c578bb8).

| Artifact | Scope | SHA-256 of committed Git blob |
| --- | --- | --- |
| [AMENDMENT-01.md](https://github.com/amadou-6e/laomedo/blob/8ceb50de3c9e820b04268543bba9410dd82c31f1/experiments/exp10/AMENDMENT-01.md) | Prospective replication limit and rationale | `6c6ddcea057fc46ec717a5380bfcd3eb0d4e068629904252b5847cebd1fbbdf5` |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/1fc002a2837dc8e4c86c6c6c1cddf2e48c578bb8/experiments/exp10/observation.json) | Direct compact capture, distinct run IDs and timestamps | `98a0fcb4a7c9fb07b439d60958af25e834d3e6280e79dfa9987df9b67569f244` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/1fc002a2837dc8e4c86c6c6c1cddf2e48c578bb8/experiments/exp10/probe.py) | Executed capture code, unchanged from first-run source | `1fe67f4da0624af43ce5fb557a290a695cb35b91163dde8ef8b93208958b82e2` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/1fc002a2837dc8e4c86c6c6c1cddf2e48c578bb8/experiments/exp10/test_probe.py) | Four checks run against current observation | `6002566e7fe33a9b45ad3a15e513886d5546dcc763139c5ded5bca04d18a5a56` |

Hashes were computed from committed Git blobs, not local Windows working-tree
copies. The temporary SQLite database, synthetic token, auto-login state and
runner journal were removed with the disposable named volume. No model
transcript, personal credential or private session was retained.
