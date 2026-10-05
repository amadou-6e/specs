---
title: Langflow integration validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration validation

The target boundary is not product-validated. Bounded Langflow 1.12.3
synthetic experiments exist; they do not establish full first-slice behavior.

| Interface | Check before acceptance | Evidence status |
| --- | --- | --- |
| Entry and resolution | `latest` and pinned revisions resolve once; a changed library revision does not alter an active run | Not executed |
| Launch variants | Direct prompt and selected issue work without fabricated issue context; later timer, issue-opened, PR-opened and failed-workflow variants retain their actual subject and stable delivery identity | Not executed; event trigger service, dedup and loop guard are not selected |
| IF-05/IF-06 | One-agent and multi-agent graphs invoke agents with correlated stage/invocation IDs; dependent failure behavior is observed | Not executed |
| Native runner correlation (IF-05/06/07/09) | A reserved invocation and runner request ID precede dispatch; an exact native acknowledgement binds once; status/cancel/effect receipts retain the same trace, and a runner wait deadline remains `incomplete` with reason `runner_result_pending` | [Merged Laomedo #85](https://github.com/amadou-6e/laomedo/commit/517d89419c6b8bdb4403f72359c5702d8aa74b34) adds a local authenticated HTTP test using a fake agent transport plus store-level conflict, reopen, rejection and deadline tests. The full host suite and Python 3.10/3.13 CI passed. This is synthetic correlation evidence, **not** a real-model, Langflow UI Stop, agent-container teardown or orphan-cleanup pass; Q11 remains open. |
| IF-07/IF-09 | Workflow events and exact launch context survive UI closure with correct run identity; inability to persist run/trace identity refuses dispatch; backend crash ends the run with partial evidence | Not executed; live Langflow graph is not resumed after crash, orphan-stop mechanism open |
| Runner-crash cleanup | A backend/runner crash must not treat `interrupted` as proof that its native container is gone; exact owned-container identity and confirmed termination must be available after restart | [EXP-91 pinned synthetic result](https://github.com/amadou-6e/laomedo/blob/f67909dd3e8db9c45d7b93adab518a576fce2f6f/experiments/exp91/RESULTS.md) and [committed observation](https://github.com/amadou-6e/laomedo/blob/f67909dd3e8db9c45d7b93adab518a576fce2f6f/experiments/exp91/observation.json) (SHA-256 `c76fbe2abb6911531af44f3609118213d1aaba73638e6e0c425d1ff69f4beb07`) show a saved run changed from `running` to `interrupted` after a hard runner kill, while its exact synthetic Docker container stayed running. The name was not saved in the record. Zero model turns; the labelled test container was removed exactly after observation. Crash cleanup is **not satisfied**; Q11 stays open. |
| IF-13 | A fresh-session follow-up uses the supplied PR with a distinct run/trace identity; later existing-session mode verifies workspace basis and provider | Not executed; existing-session mode deferred |
| Long synchronous call timeout | Caller, component and server timeout outcomes distinguish late effects from confirmed cancellation; IF-06/07 preserve partial/unknown state | [EXP-10 synthetic result](../../experiments/long-call-timeout/iterations/2026-10-05/results.md) observed late effects after caller and v2 server timeouts. [EXP-65](../../experiments/post-timeout-job-status/iterations/2026-10-05/results.md) observed `500 JOB_FAILED` before **and after** a late synthetic effect. [EXP-66](../../experiments/timeout-trace-integration/iterations/2026-10-05/results.md) observed a live synthetic call with a durable partial Laomedo trace and no redispatch after store reopen. [Merged Laomedo #70](https://github.com/amadou-6e/laomedo/commit/352a98146674ac8dbcdc76e1155054a78cdacb12) adds regression tests for effects before timeout/after crash and non-downgrade after a lookup error; these fixes were **not** exercised by a new live call. The [proposed reconciliation contract](contract/timeout-reconciliation.md) is only partially exercised: real agent and cancellation remain untested; first-slice gate not accepted |
| Langflow Playground Stop to native runner | A visible Stop click during an active graph must correlate to the bound native run and produce a native cancellation request; the UI disappearing alone is not cancellation proof | [EXP-89 pinned result](https://github.com/amadou-6e/laomedo/blob/35801d0bd30df4d69ed38916c1e61903a8cdf620/experiments/exp89/RESULTS.md) and [sanitized observation](https://github.com/amadou-6e/laomedo/blob/35801d0bd30df4d69ed38916c1e61903a8cdf620/experiments/exp89/observation.json) (SHA-256 of committed bytes `7d36fe7906885b23e2036691617a7a657553debdcafa63be935e553d208cc726`): in pinned Langflow 1.12.3, the visible Playground Stop click completed while a synthetic runner acknowledgement was held, but no runner cancel arrived in eight seconds and the acknowledgement still arrived. This **fails propagation for the tested `start` path**. The blocking `fresh` case did not complete a visible Stop click and is inconclusive; the completed-run control had no active Playground Stop. Zero model turns. Real-agent Stop, native turn status and crash cleanup remain unverified; Q11 is open. |
| Langflow feasibility | Verify all components remain usable, artifact refs can cross node types, and selective rerun capability before promising it | Not executed |

Related observations in [shared contracts](../../architecture/shared-contracts.md)
do not establish these new target guarantees. Pin the Langflow version and
test environment when recording actual evidence.
