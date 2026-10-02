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

The pinned image and synthetic harness are prepared. After the user selects the maximum exposure window, launch only the named disposable backend, worker, canary, private Docker network and private volumes. Reserve a synthetic durable run, start external-write attempts, hard-kill the backend, observe supervisor revocation and worker death, make a post-death grant attempt, then restart and inspect sweep. Record timestamps and raw canary events before cleanup. No run has been executed yet, so container IDs, run IDs, timings and outcomes are unavailable.
