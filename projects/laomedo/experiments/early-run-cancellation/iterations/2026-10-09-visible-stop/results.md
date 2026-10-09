---
title: Visible Playground Stop bounded result
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded result

The [Laomedo published Phase E result](https://github.com/amadou-6e/laomedo/blob/7460da39ee4d2922469e04895adf4d56de32615c/experiments/exp22/PHASE-E-RESULTS.md) records one real submission and a shared ledger of 5/12. The browser clicked the visible Playground `button-stop` after native `sleep 30` command start. The authenticated private route audit recorded one async start, one lookup for the acknowledged request ID, and one cancel for that exact run after the click began. The runner was terminal before browser-context closure, so a cancellation caused only by disconnect cannot satisfy this pass. Host fallback cleanup used an in-process call after classification and cannot satisfy the HTTP audit.

| Criterion | Observation | Assessment |
| --- | --- | --- |
| Visible Stop and exact identity | One browser Send and visible Stop click; one start, one matching request lookup and one cancel to the same run, in click-to-terminal-to-close order | Passed for this bounded visible UI-to-real-agent composition |
| Native cancellation | Native `turn/completed: interrupted`; runner terminal `cancelled`, `cancel_confirmed=true` | Passed for this run, beyond a mere HTTP 202 request |
| Partial evidence and effects | 61 native raw events retained; exact owned container absent; delayed sentinel absent after the original command delay | Passed for this run |
| Credential boundary | Content-free `auth.json` read denied at native event index 52; provider profile still mounted in the stage | Pass for the tested command route, not controller-only credential custody or hosted isolation |

The browser's request observer saw the build monitor endpoint, not an exact frontend Stop request path. The click timing plus component-to-runner route and native result establish the observed composition, but no durable Langflow invocation-to-runner cross-store trace join was created. That #22/Q11 limit remains. #93's postrevocation and joint-outage limits are unchanged. Neither issue is closed by this result alone.
