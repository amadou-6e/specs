---
title: E05 direct no-model evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence

| Artifact | Observation | Limit |
| --- | --- | --- |
| [Sanitized stage observation](https://github.com/amadou-6e/laomedo/blob/f897f41/experiments/exp18/stage-observation.json) | Sidecar inspect, pinned images, engine 27.3.1, runner 401, stage preflight, direct command results, routes, sweep, lease/revocation, before/after hashes and cleanup | Revision-pinned; no raw grant or credential is retained |
| [Harness](https://github.com/amadou-6e/laomedo/blob/f897f41/experiments/exp18/probe_stage.py) and [fixed sidecar](https://github.com/amadou-6e/laomedo/blob/f897f41/experiments/exp18/runner_probe_sidecar.py) | Reproducible no-model probe with stage lifetime bounded by its command and an expiring/revocable grant | Not a production launch path |
| [Real downgrade review](https://github.com/amadou-6e/laomedo/pull/58#pullrequestreview-5406644179) | Correct request passed and all 30 Docker downgrade variants were rejected at create/inspect without starting | The review did not execute the stage |
| Agent-originated command/tool events | None | Step 5 needs separate nonpersonal credential and turn-budget authorization |

The first two stage attempts had incomplete file sweeps and are recovered, inconclusive runs. The final sweep covered 6,009 files and 679,212,708 bytes with `incomplete=false`. Absence from the tested paths and scanned files is narrower than proof against every container escape.
