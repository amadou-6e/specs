---
title: Langflow graph freeze evidence manifest
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
| [observation.json](https://github.com/amadou-6e/laomedo/blob/feat/33/experiments/exp03/observation.json) | Synthetic probe against pinned server | Full synthetic responses, graph/component hashes, no secrets |
| [probe.py](https://github.com/amadou-6e/laomedo/blob/feat/33/experiments/exp03/probe.py) | Reproducible harness | Import, pause, patch, release, rerun |
| [build_flow.py](https://github.com/amadou-6e/laomedo/blob/feat/33/experiments/exp03/build_flow.py) | Installed 1.12.3 component APIs | Saved-flow fixture generation |

The source links use the experiment branch until an implementation commit is pinned. A reviewer should verify that branch revision before treating the evidence as immutable.
