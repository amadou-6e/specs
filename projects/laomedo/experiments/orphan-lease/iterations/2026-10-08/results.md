---
title: Integrated Codex and orphan lease results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-08
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded results

The [Laomedo result](https://github.com/amadou-6e/laomedo/blob/e4b493988b06dcc6448ebd77c1e8cff25dbdd209/experiments/exp22/PHASE-C-RESULTS.md) records the tested implementation commits and the two observations. The two submissions used 2/4 authorized model turns. Both agent-originated attempts to read `auth.json` were denied. This is a direct-runner, single-user local observation with a fake GitHub transport, not proof of hosted credential isolation or a real GitHub write.

| Criterion | Observation | Assessment |
| --- | --- | --- |
| Active native cancellation | Early `prepared` ID, one confirmed fake update, native `turn/completed: interrupted`, final `cancelled` with confirmed teardown, exact container absent and delayed sentinel absent | Passed for direct runner; Langflow UI Stop and full trace join untested |
| Service survival and revocation | Independent host survived the runner-tree kill; grant revoked after 4.562 seconds; host-originated late request rejected without provider call | Passed inside the selected 60-second bound for synthetic grant |
| Independent work and restart | Other run's distinct grant confirmed a fake write after the killed run's revocation; lookalike container survived; startup sweep recorded `interrupted` with one attempt and no redispatch | Passed at local test scope |
| Service-attributed removal | The lease cleanup watch finished 9.671 seconds after kill; the exact container was already absent when the service first looked (`never_observed`) | Inconclusive; absence does not prove service performed removal or the exact removal time |
| Agent-originated post-revocation denial | No agent request was observed after revocation; a separate host-originated control was denied | Inconclusive; host control is not agent evidence |

No receipt for the killed run appeared after its revocation. Two fake-provider receipts matched confirmed journal rows, with no confirmation after an unknown result. The active and kill raw-event hashes are recorded in the [evidence manifest](evidence/manifest.md). Neither #22 nor #93 should be closed solely from this attempt. The current Docker self-removal route cannot observe the two remaining #93 criteria without a different test arrangement or a reviewed change to the acceptance boundary.
