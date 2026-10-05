---
title: Langflow integration validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
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
| IF-07/IF-09 | Workflow events and exact launch context survive UI closure with correct run identity; inability to persist run/trace identity refuses dispatch; backend crash ends the run with partial evidence | Not executed; live Langflow graph is not resumed after crash, orphan-stop mechanism open |
| IF-13 | A fresh-session follow-up uses the supplied PR with a distinct run/trace identity; later existing-session mode verifies workspace basis and provider | Not executed; existing-session mode deferred |
| Long synchronous call timeout | Caller, component and server timeout outcomes distinguish late effects from confirmed cancellation; IF-06/07 preserve partial/unknown state | [EXP-10 synthetic result](../../experiments/long-call-timeout/iterations/2026-10-05/results.md) observed late effects after caller and v2 server timeouts. [EXP-65](../../experiments/post-timeout-job-status/iterations/2026-10-05/results.md) observed `500 JOB_FAILED` before **and after** a late synthetic effect. [EXP-66](../../experiments/timeout-trace-integration/iterations/2026-10-05/results.md) observed a live synthetic call with a durable partial Laomedo trace and no redispatch after store reopen. The [proposed reconciliation contract](contract/timeout-reconciliation.md) is only partially exercised: real agent and cancellation remain untested; first-slice gate not accepted |
| Langflow feasibility | Verify all components remain usable, artifact refs can cross node types, and selective rerun capability before promising it | Not executed |

Related observations in [shared contracts](../../architecture/shared-contracts.md)
do not establish these new target guarantees. Pin the Langflow version and
test environment when recording actual evidence.
