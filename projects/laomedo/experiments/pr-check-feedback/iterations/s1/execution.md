---
title: PR-check feedback S1 execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

Windows host, Docker Linux worker, pinned Langflow image. Python 3.14 was a
coordinator build-only observation, not a field captured by S1.
Command: `python -m experiments.exp123.probe --record S1 --source-commit
f5b2e9a257fe59e3f281300358d209c41546b76a`. Source bytes were checked against
Git before dispatch. Independent read-only Claude execution approval was posted
on [Laomedo #124](https://github.com/amadou-6e/laomedo/pull/124) before running.

Disposable labelled container/volume `laomedo-exp123-s1-20261009`; only experiment
source and disposable state were mounted. Port published on host loopback;
bridge outbound access remained available and telemetry was not explicitly disabled.
Each case called Graph.arun once. Stop cancelled the existing task; crash killed
the exact labelled worker and restarted it once, without restarting its graph.
The controller captured journal/case/flow bytes before exact cleanup, checked
their consistency and verified container/volume absence. No retry or replication.
Private credentials, host paths and reusable tokens were not captured.
