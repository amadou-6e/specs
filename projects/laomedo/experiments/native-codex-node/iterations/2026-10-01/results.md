---
title: Installed-node attempt results
status: complete
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Results and disposition

| Gate | Outcome | Evidence / limit |
| --- | --- | --- |
| Installed component catalog and flow round trip | Pass | Actual server API; no browser visual inspection |
| Fresh skill-based turn and structured outputs | Pass | Native command results, marker bytes, matching run/thread/hash in Langflow response |
| Restart/resume through node | Pass | Same native thread, requested exact input hash, prior marker read |
| Independent fresh workspace | Pass for host isolation | New thread and marker absent; agent fixture-path task failed, not relabeled success |
| Invalid inputs, missing snapshot, exhausted cap | Pass | Langflow errors; authoritative ledger unchanged |
| Real explicit cancellation | Inconclusive | Command started but native turn ended; no cancellation confirmation |
| UI Stop propagation | Unsupported in slice | Follow-up #22 |
| Outstanding command terminal semantics | Gap | Follow-up #24 |

Initial resume snapshot was sha256:11fa821f62d85f98a23751be5a41de6c81ee88358bb44f6f8f968e25fd9d9276.
New snapshot was sha256:a1076cd86e9260e3fa33a94717b7ff5e52a39b81d3a8d2883418b28cad8773cf.
Native thread was 01a0f881-dbdd-7a83-a6a5-03b56d2bcb41.

Go for bounded local fresh/resume trials with the recorded limits. No claim that
#21 is fully passed or merge-ready: cancellation remains unverified and the
sample fresh task failed. No hosted, multi-user, network isolation or production
auth conclusion. Component skill-use output remains offered even where external
native evidence shows reading.

[Cancellation lifecycle #22](https://github.com/amadou-6e/laomedo/issues/22) and
[outstanding-command semantics #24](https://github.com/amadou-6e/laomedo/issues/24)
track definitive limits. A follow-up issue does not waive an unmet gate.

