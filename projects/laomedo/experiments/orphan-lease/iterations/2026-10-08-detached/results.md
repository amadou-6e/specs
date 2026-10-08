---
title: Detached-stage bounded results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-08
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded results

The [Laomedo result](https://github.com/amadou-6e/laomedo/blob/bfc6289c9741791cc4728e7bc9906356fb392ce9/experiments/exp22/PHASE-C-DETACHED-RESULTS.md) records the third submitted turn. The tested implementation pin is `bc842f9`.

| Criterion | Observation | Assessment |
| --- | --- | --- |
| Login read | Agent-originated `auth.json` read denied, native event index 74 | Pass for this route; profile remains mounted in stage |
| Independent revocation | Lease host survived runner-tree kill; grant revoked 4.328 seconds after kill | Pass inside selected 60-second synthetic-grant bound |
| Exact cleanup | Lease service returned `removed_after_loss` and `cleanup_verified=true`; exact container absent, same-prefix lookalike alive | Pass for service-attributed local cleanup; cleanup watch finished at 9.437 seconds, not a measured removal time |
| Held request | Agent wrote and bridge held `phase-c-kill-1` before kill; processing after revocation returned `grant_unavailable` with no fake-provider call | Pass for held agent-written request; a newly initiated post-revocation agent action remains untested |
| Independent work and recovery | Other run continued; two fake receipts matched confirmed rows; startup sweep kept one attempt and no redispatch | Pass at bounded local scope |

This result resolves the earlier Docker self-removal ambiguity for the revised detached route. It does not prove real GitHub credential revocation, joint runner-and-service outage cleanup, hosted isolation, Langflow UI Stop, or a new request initiated by an agent after revocation. It does not change the historical [first attempt](../2026-10-08/results.md) or close #93 or #22 on its own.
