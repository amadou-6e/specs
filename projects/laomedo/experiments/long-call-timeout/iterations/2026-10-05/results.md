---
title: Long-call timeout results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Boundary | Caller result | Effect relative to caller response |
| --- | --- | --- |
| Control: 0.2 s endpoint, 8 s component limit | HTTP 200 in 1.016 s | Before success |
| Outer caller: 1 s limit, 4 s endpoint | `TimeoutError` in 1.016 s | About 3.1 s **after** timeout |
| Component: 2 s HTTP limit, 5 s endpoint | HTTP 500 in 5.375 s; message says remote execution may still be active | Before the 500 response; runner response was disconnected |
| Langflow v2 sync: verified 3 s ceiling, 6 s endpoint | HTTP 408 `EXECUTION_TIMEOUT` with job ID in 3.032 s | About 3.1 s **after** 408 |

The [sanitized observation](evidence/manifest.md) retains UTC timestamps,
caller durations, response categories and runner records. Each case had one
runner entry and one effect. The outer caller and v2 server timeout **did not
stop** the synthetic side effect. The component's error wording preserved
uncertainty, but its configured 2-second socket timeout did not produce a
2-second whole-graph response in this run. These are distinct timeout layers;
the v2 server ceiling does not describe the v1 route.

This is a **first-slice hazard, not a safe-timeout pass**. The probe did not
query the v2 job after HTTP 408, capture IF-06/07 partial trace state for
failed calls, run a real Codex container or prove cancellation. Those missing
checks prevent claiming that Laomedo currently preserves an effect-aware
terminal run record. A production timeout outcome must not mean the external
action stopped without evidence. EXP-10 provides a counterexample for that
assumption under this pinned runtime; a separate integration check remains.
