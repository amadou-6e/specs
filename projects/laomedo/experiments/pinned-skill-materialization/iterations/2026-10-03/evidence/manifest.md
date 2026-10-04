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
[`0ed7dfac`](https://github.com/amadou-6e/laomedo/commit/0ed7dfac634b8c650b7022edcfb390e35b8c40e1).

| Artifact | Scope | SHA-256 |
| --- | --- | --- |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/0ed7dfac634b8c650b7022edcfb390e35b8c40e1/experiments/exp08/observation.json) | LF/CRLF source, actual clone Git status/add/clean, checkout conversion and effective hashes | `8aca9dffc785a1e9b5145e1210e3a2d3c0dabeffdf091fc80f316ff25b17bc00` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/0ed7dfac634b8c650b7022edcfb390e35b8c40e1/experiments/exp08/probe.py) | Synthetic Git-clone fixture and rejection checks | `dcf5eb0896d851e22d1452186b8b428508a95f2174894e6c52f18fe279f68442` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/0ed7dfac634b8c650b7022edcfb390e35b8c40e1/experiments/exp08/test_probe.py) | Invariant test | `ea1ad049052b2f530255394473542116ce6a6b40e65b88c14a519db09a1ef4d2` |

Hashes are of the committed Git blobs, not Windows working-tree copies.
The probe's `--record` mode writes LF explicitly. Temporary Git repositories
and skill stores contained only synthetic bytes and were removed. No native
agent trace exists, so there is no read/use evidence to attach.
