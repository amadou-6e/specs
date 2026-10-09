---
title: Installed Langflow graph cancellation result
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded result

The [Laomedo published result at `a0a25d3`](https://github.com/amadou-6e/laomedo/blob/a0a25d304a18466e3f1446cbd10e317a303e3525/experiments/exp22/PHASE-D-RESULTS.md) records the final shared submission, 4/4. The installed graph task ended `cancelled`. Its authenticated private route audit observed one start, one lookup on the acknowledged request ID, and one cancel on the same run ID. The host's fallback cleanup used an in-process call after classification and cannot satisfy that HTTP audit.

| Criterion | Observation | Assessment |
| --- | --- | --- |
| Agent command boundary | Agent-originated content-free `auth.json` read denied at native event index 46; provider profile still mounted in stage | Pass for this local command route, not controller-only credential custody |
| Native cancellation | Long command started before graph Stop signal; native `turn/completed: interrupted`; runner terminal `cancelled`, `cancel_confirmed=true` | Passed for installed in-process Langflow graph to real runner |
| Identity and retry | One persisted runner run; exact start, lookup and cancel route identity; shared ledger 4/4 | Passed for this case, no redispatch observed |
| Partial evidence and effects | 55 raw native events retained; exact owned container and Langflow graph container absent; delayed sentinel absent after original command delay | Passed for this case |

This does not prove a **visible Playground Stop** click reaches a real Codex turn. EXP-94 proved that click path only against a synthetic runner. The test also did not create a durable Langflow invocation-to-runner cross-store trace join. Those are separate #22/Q11 limits. #93's real GitHub grant and joint runner-plus-lease-service outage limits are unchanged. Neither issue is closed by this result alone.
