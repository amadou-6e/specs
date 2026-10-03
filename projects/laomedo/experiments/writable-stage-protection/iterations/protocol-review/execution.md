---
title: E05 create-only execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

EXP-07 passed its synthetic 60-second bound. The reviewer approved E05 steps 1-2, so the [create-only probe](https://github.com/amadou-6e/laomedo/blob/feat/48/experiments/exp18/probe_create_only.py) built disposable fixture roots, verified the pinned image ID, created an internal test network, and called `docker create` for an exact request and the writable-skill mismatch. It inspected both containers without starting either. A third `docker create` with a missing seccomp profile failed before a container existed. The probe removed the containers and network and recorded a sanitized [observation](https://github.com/amadou-6e/laomedo/blob/feat/48/experiments/exp18/create-only-observation.json).

No Docker stage process, agent, model, personal credential or production repository was used. Steps 3-6 remain unapproved pending review of the amended protocol and verifier; no command/tool denial or network observation exists yet.
