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
[`1b6c1c6`](https://github.com/amadou-6e/laomedo/commit/1b6c1c6d1aee3f4e223900cf975ce7bc8e246bc0).

| Artifact | Scope | SHA-256 |
| --- | --- | --- |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/1b6c1c6d1aee3f4e223900cf975ce7bc8e246bc0/experiments/exp08/observation.json) | LF/CRLF source, effective, post-edit hashes and Git statuses | `63a17f274951feb5535fb307fc4820cf3338081c5f32d53851e7ee66edd1118a` |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/1b6c1c6d1aee3f4e223900cf975ce7bc8e246bc0/experiments/exp08/probe.py) | Synthetic fixture and rejection checks | `84c0ec6584c77e5c5502f97a1a7bedb43d426b6722642db96cd49863aeb6ff00` |
| [test_probe.py](https://github.com/amadou-6e/laomedo/blob/1b6c1c6d1aee3f4e223900cf975ce7bc8e246bc0/experiments/exp08/test_probe.py) | Invariant test | Pinned source |

Temporary Git repositories and skill stores contained only synthetic bytes
and were removed. No native agent trace exists, so there is no read/use
evidence to attach.
