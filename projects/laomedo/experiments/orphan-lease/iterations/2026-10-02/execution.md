---
title: Orphan lease execution plan
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution plan

The user selected a 60-second maximum exposure window. From Laomedo `feat/37`, run `python experiments/exp07/probe.py --max-exposure-seconds 60`. The 2026-10-02 run used pinned `langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`, named disposable backend, worker, canary, private network and volumes, and no model calls. It reserved synthetic run `7bee948f-df1a-4e17-aec2-f38e74707710`, started external-write attempts, hard-killed the backend, observed supervisor revocation and worker exit, made a denied post-death grant attempt, then restarted and inspected the sweep. The probe's `finally` cleanup completed, and a subsequent Docker resource-name query found no EXP-07 resources.
