---
title: Pinned skill materialization evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

Pinned Laomedo revision:
[`839f2bb`](https://github.com/amadou-6e/laomedo/commit/839f2bbaa41f4bf0d3801f3f2e34796a6e57314b).

| Artifact | Scope | SHA-256 |
| --- | --- | --- |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/839f2bbaa41f4bf0d3801f3f2e34796a6e57314b/experiments/exp08/observation.json) | LF/CRLF source, actual clone Git status/add/clean, checkout conversion and effective hashes | `8aca9dffc785a1e9b5145e1210e3a2d3c0dabeffdf091fc80f316ff25b17bc00` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/839f2bbaa41f4bf0d3801f3f2e34796a6e57314b/experiments/exp08/probe.py) | Synthetic Git-clone fixture and rejection checks | `bbddd9033f83410472427c1b34b1444467d02e9622ac83fc3fb70faf30451cf5` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/839f2bbaa41f4bf0d3801f3f2e34796a6e57314b/experiments/exp08/test_probe.py) | Invariant test | `ea1ad049052b2f530255394473542116ce6a6b40e65b88c14a519db09a1ef4d2` |

Hashes are of the committed Git blobs, not Windows working-tree copies.
The probe's `--record` mode writes LF explicitly. Temporary Git repositories
and skill stores contained only synthetic bytes and were removed. No native
agent trace exists, so there is no read/use evidence to attach.
