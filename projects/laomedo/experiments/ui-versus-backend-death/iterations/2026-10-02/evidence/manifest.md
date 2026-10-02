---
title: UI versus backend-death evidence manifest
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
| [observation.json](https://github.com/amadou-6e/laomedo/blob/feat/36/experiments/exp06/observation.json) | Pinned Langflow and Laomedo synthetic store | Client outcomes, run/trace IDs, container states and startup sweep |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/feat/36/experiments/exp06/probe.py) | Deterministic harness | Client close, flow reopen, hard kill, restart and checks |
| [stage_component.py](https://github.com/amadou-6e/laomedo/blob/feat/36/experiments/exp06/stage_component.py) | Synthetic custom node | Reserve, dispatch attempt and gate |

The test volume with its temporary auto-login state was removed after sanitized evidence capture. Branch links await a pinned commit.
