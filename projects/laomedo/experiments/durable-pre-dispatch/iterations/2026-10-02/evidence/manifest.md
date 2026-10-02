---
title: Durable pre-dispatch evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

| Artifact | Producer | Scope |
| --- | --- | --- |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/feat/34/experiments/exp04/observation.json) | Six subprocess crash phases | Persisted IDs/revisions, counters, status before/after sweep |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/feat/34/experiments/exp04/probe.py) | Synthetic fault injector | Exact exit phases and SQLite readback |
| [test_workflow_run_store.py](https://github.com/amadou-6e/laomedo/blob/feat/34/tests/test_workflow_run_store.py) | Unit tests | Refusal, one attempt and no-replay sweep |

The links use the branch pending a pinned implementation commit. SQLite databases were temporary and contained only synthetic graph/config data.
