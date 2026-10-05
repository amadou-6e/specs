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
Observation, probe and checks: Laomedo
[`dee05c2`](https://github.com/amadou-6e/laomedo/commit/dee05c2532de264796cccdc0543b658b0770d966).

| Artifact | Scope | SHA-256 of committed Git blob |
| --- | --- | --- |
| [PROTOCOL.md](https://github.com/amadou-6e/laomedo/blob/e4f4685e0a58d3825ab6c6c7175e57fff3ca116a/experiments/exp10/PROTOCOL.md) | Frozen cases, limits and falsifiers | `f24c66929a17111db16a9ac9fd1acf89b35962a2d576cb2e145cb16864d77879` |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/dee05c2532de264796cccdc0543b658b0770d966/experiments/exp10/observation.json) | Sanitized caller responses, UTC effects and effective timeout | `c69701f13fc01b2081e201d81a0ca7c5b19a5412aa0205bedcb094eeed71e486` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/dee05c2532de264796cccdc0543b658b0770d966/experiments/exp10/probe.py) | Pinned Docker/Langflow harness and compact capture | `1fe67f4da0624af43ce5fb557a290a695cb35b91163dde8ef8b93208958b82e2` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/dee05c2532de264796cccdc0543b658b0770d966/experiments/exp10/test_probe.py) | Four evidence and falsifying-mutation checks | `6002566e7fe33a9b45ad3a15e513886d5546dcc763139c5ded5bca04d18a5a56` |

Hashes were computed from committed Git blobs, not local Windows working-tree
copies. The temporary SQLite database, synthetic token, auto-login state and
runner journal were removed with the disposable named volume. No model
transcript, personal credential or private session was retained.
