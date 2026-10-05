---
title: EXP-19 phase-zero results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

The credential-free phase passed its five frozen conditions at Laomedo commit `af87e6ccd91876f510789afece1cf7dc8cd8c033`:

| Condition | Observed result |
| --- | --- |
| Ready issue | One dispatch; run completed; two raw receipts and two projections; frozen work key, source marker, input digest, graph snapshot, run ID, trace ID, component revision and candidate commit matched the saved result binding; local Git commit `a119e3da725aac78dd378bf22e9bd4a868006998` on a unique branch; zero remotes and no target PR. |
| Changed source body and update marker | Refused before any run reservation or dispatch with `source_snapshot_changed`; no candidate. |
| Opened prerequisite | Refused before dispatch with `source_not_ready`; no candidate. |
| Incomplete blocker connection | Refused before dispatch with `source_not_ready`; no candidate. |
| Fake agent fails after first event | One dispatch; run failed; one committed raw receipt and projection retained as a partial trace; no candidate. |

The local commit existed only in the disposable checkout and was independently compared with `git rev-parse HEAD` before cleanup. The saved observation is [SHA-256 pinned in the evidence manifest](evidence/manifest.md). The run used zero model turns and zero GitHub writes. This establishes local library composition only. It does not establish a Langflow graph run, native agent event fidelity, live Work Graph source correctness, production grant isolation, agent-created remote PR, or full EXP-19 acceptance. EXP-18's agent-originated boundary check remains deferred with 0/4 historical model turns used.
