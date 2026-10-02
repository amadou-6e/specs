---
title: Orphan lease results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

The user selected a 60-second maximum exposure window and an independent stage lease supervisor plus startup sweep. The zero-model disposable Docker probe passed that bound on 2026-10-02 with the pinned Langflow 1.12.3 image. The accepted-write events show the consequence of the measured delay: three synthetic writes succeeded after the backend kill was requested and before grant revocation. The supervisor then revoked the grant and killed the worker.

| Check | Observation |
| --- | --- |
| Grant lifetime after kill request, conservative upper bound | 599.670 ms, under 60 seconds |
| Worker lifetime after kill request, conservative upper bound | 1207.478 ms, under 60 seconds |
| Post-death write using same disposable grant | HTTP 403 |
| Worker state after supervisor action | `exited` |
| Restart sweep | One synthetic run marked `crashed`; one dispatch attempt, incomplete evidence, no redispatch |
| Cleanup | No named EXP-07 containers, volumes or network remained |

The [redacted observation](https://github.com/amadou-6e/laomedo/blob/feat/37/experiments/exp07/observation.json) and [supervisor report](https://github.com/amadou-6e/laomedo/blob/feat/37/experiments/exp07/supervisor-report.json) contain the timing and event evidence. They contain no grant value or personal credential. The harness launched the test worker directly; it did not use the production Langflow stage adapter. This result supports the chosen orphan-control mechanism for a local prototype, but it does not prove that a real Git push credential, every external-write route or a production stage is governed by the same lease. The first live writable stage remains blocked on those integration and protection checks, including [EXP-18](https://github.com/amadou-6e/laomedo/issues/48).
