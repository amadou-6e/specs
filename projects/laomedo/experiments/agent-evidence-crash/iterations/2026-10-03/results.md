---
title: Agent evidence crash results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Child boundary | Dispatch attempts | Invocation / native ID after restart | Raw / projected receipts | Terminal evidence |
| --- | ---: | --- | ---: | --- |
| Before invocation reserve | 0 | none / none | 0 / 0 | Run crashed; invocation absent |
| After invocation reserve | 0 | present / unknown | 0 / 0 | Crashed; stream unknown |
| After dispatch, before native ID | 1 | present / unknown | 0 / 0 | Crashed; stream unknown |
| After native-ID receipt | 1 | present / known | 0 / 0 | Crashed; stream unknown |
| After raw-event flush | 1 | present / known | 1 / 1 | Crashed; stream partial |
| After projection | 1 | present / known | 1 / 1 | Crashed; stream partial |
| Normal control | 1 | present / known | 1 / 1 | Completed; stream complete |

After the raw-event-flush kill, the projection count was **zero before**
restart and one after restart. Its receipt sequence matched the single
committed raw record. The restart sweep did not restart an invocation or add
an event. A native ID was retained only when its receipt had been committed;
earlier phases left it unknown. A second sweep/project did not duplicate a
projection in the unit test. This supports the bounded synthetic persistence
claim, not a claim that real provider events have stable IDs or complete
streams.

This fixture holds run storage and invocation in one killed process. It is a
synthetic analogue of a fate-shared backend crash, **not** a container crash
with the backend still running. It cannot verify the separate first-slice
container-crash rule, which should end the invocation as `failed`.

The first-slice rule remains terminal on backend crash. An absent source
event ID remains absent; receipt sequence is not a deduplication key. EXP-09
must test a selected T07 replay policy before repeated/reordered events are
interpreted as distinct actions. Full-backend integration, provider timing,
power loss, and real-agent mid-turn recovery remain untested.
