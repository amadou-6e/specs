---
title: Orphan lease evidence
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

| Artifact | Producer | Status |
| --- | --- | --- |
| [observation.json](https://github.com/amadou-6e/laomedo/blob/feat/37/experiments/exp07/observation.json) | Disposable Docker probe | Produced; timings, event list, restart state |
| Canary accepted/denied write events | Synthetic external-write service | In observation; three accepted after kill request, one denied after revocation |
| [supervisor-report.json](https://github.com/amadou-6e/laomedo/blob/feat/37/experiments/exp07/supervisor-report.json) | Independent host supervisor | Produced; revocation and worker stop |
| Durable run after backend restart | Laomedo startup sweep | In observation; `crashed`, one dispatch attempt, incomplete evidence |

The published evidence contains no grant value, personal credential or production repository path.
