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

## Release-interview target coverage

[Community distribution](contract/community-distribution.md) requires
Codex/Windows-first automatic setup with Docker available and provider login.
No installer or supported clean-environment acceptance was run in this
interview repair. The
[complete Langflow demonstration](../work-graph/contract/application-execution.md#next-requested-demonstration-the-complete-langflow-graph)
needs an actual imported graph showing Skill/Agent/Output Contract, conditional
routes and real draft publication. The new component and grant-safe downstream
publication seam are unimplemented/unverified. Separate historical node and
publication checks below do not constitute that composed acceptance.

The target boundary is not product-validated. Bounded Langflow 1.12.3
synthetic experiments exist; they do not establish full first-slice behavior.

| Interface | Check before acceptance | Evidence status |
| --- | --- | --- |
| Entry and resolution | `latest` and pinned revisions resolve once; a changed library revision does not alter an active run | Not executed |
| Launch variants | Direct prompt and selected issue work without fabricated issue context; later timer, issue-opened, PR-opened and failed-workflow variants retain their actual subject and stable delivery identity | Not executed; event trigger service, dedup and loop guard are not selected |
| In-run PR-head check gate | An agent delivers and reads back its PR while active; an authenticated check for the exact head decides one waiting gate; a failed check starts only a bounded new invocation, while stale/duplicate/self-triggered events do not cause extra invocations | [EXP-123 S1](../../experiments/pr-check-feedback/iterations/s1/results.md) passed seven synthetic cases on pinned Langflow 1.12.3 using custom polling wait/router components within one Graph.arun per case and an unrolled two-agent cap. Early/pending/final, duplicate/conflict/stale, controller Stop and backend-death controls are captured with byte hashes. Zero model turns or GitHub writes. This is not built-in webhook waiting, arbitrary cycles, visible UI Stop, production ingress authentication or real-agent PR delivery/readback evidence. Those portions of [decision 0005](../../decisions/0005-active-run-pr-feedback.md) remain unverified. |
| IF-05/IF-06 | One-agent and multi-agent graphs invoke agents with correlated stage/invocation IDs; dependent failure behavior is observed | Not executed |
| Native runner correlation (IF-05/06/07/09) | A reserved invocation and runner request ID precede dispatch; an exact native acknowledgement binds once; status/cancel/effect receipts retain the same trace, and a runner wait deadline remains `incomplete` with reason `runner_result_pending` | [Merged Laomedo #85](https://github.com/amadou-6e/laomedo/commit/517d89419c6b8bdb4403f72359c5702d8aa74b34) adds a local authenticated HTTP test using a fake agent transport plus store-level conflict, reopen, rejection and deadline tests. The full host suite and Python 3.10/3.13 CI passed. This is synthetic correlation evidence, **not** a real-model, Langflow UI Stop, agent-container teardown or orphan-cleanup pass; Q11 remains open. |
| IF-07/IF-09 | Workflow events and exact launch context survive UI closure with correct run identity; inability to persist run/trace identity refuses dispatch; backend crash ends the run with partial evidence | Not executed; live Langflow graph is not resumed after crash, orphan-stop mechanism open |
| Runner-crash cleanup | A backend/runner crash must not treat `interrupted` as proof that its native container is gone; exact owned-container identity and confirmed termination must be available after restart | [EXP-91 pinned synthetic result](https://github.com/amadou-6e/laomedo/blob/f67909dd3e8db9c45d7b93adab518a576fce2f6f/experiments/exp91/RESULTS.md) and [committed observation](https://github.com/amadou-6e/laomedo/blob/f67909dd3e8db9c45d7b93adab518a576fce2f6f/experiments/exp91/observation.json) (SHA-256 `c76fbe2abb6911531af44f3609118213d1aaba73638e6e0c425d1ff69f4beb07`) show a saved run changed from `running` to `interrupted` after a hard runner kill, while its exact synthetic Docker container stayed running. The name was not saved in the record. Zero model turns; the labelled test container was removed exactly after observation. Crash cleanup is **not satisfied**; Q11 stays open. |
| IF-13 | A fresh-session follow-up uses the supplied PR with a distinct run/trace identity; later existing-session mode verifies workspace basis and provider | Not executed; existing-session mode deferred |
| Playground Stop propagation after EXP-94 | A visible Stop click during pending acknowledgement and during a blocking fresh call must reach only the bound run; a late click must not cancel a completed run | [Draft Laomedo #94 evidence at `7d37ff6`](https://github.com/amadou-6e/laomedo/blob/7d37ff6/experiments/exp94/RESULTS.md) records four one-shot browser cases against pinned Langflow 1.12.3 and a loopback synthetic runner. Machine files and hashes are in that result. Cases A/B each sent one exact cancel after a matching request lookup; the late-click control sent none. No model turn or real container teardown was tested; browser capture did not identify the upstream Stop endpoint. This supersedes the prior negative EXP-89 result only for the revised synthetic component, not for Q11 real-agent acceptance. |
| Installed graph Stop to real Codex runner | Graph cancellation must target only its acknowledged run, retain native partial events, and report remote cancellation only after terminal runner confirmation | [2026-10-09 Phase D result](../../experiments/early-run-cancellation/iterations/2026-10-09/results.md) observed one real Codex turn through the pinned Langflow in-process graph: one authenticated start, matching request lookup and cancel, native `interrupted`, confirmed runner `cancelled`, exact-container absence and retained raw events. This did not use the visible Playground Stop or establish a durable Langflow invocation-to-runner cross-store trace join; Q11/#22 remain open. |
| Visible Playground Stop to real Codex runner | A browser Stop click during an active native command must reach only the bound run, and terminal native/runner evidence must precede browser disconnect | [2026-10-09 Phase E result](../../experiments/early-run-cancellation/iterations/2026-10-09-visible-stop/results.md) observed one real Codex turn through the pinned disposable Langflow server. The visible `button-stop` click preceded one exact authenticated request lookup and cancel; native status was `interrupted`, runner status was confirmed `cancelled`, and the owned container and delayed sentinel were absent. This passes the bounded UI-to-real-agent composition. The browser observer did not identify the exact frontend Stop endpoint, and no durable Langflow invocation-to-runner cross-store trace join was created; Q11/#22 remain open. |
| Visible Playground Stop before native thread | A Stop click while an async runner acknowledgement is held must cancel the exact prepared run without dispatch or redispatch | [2026-10-09 Phase F result](../../experiments/early-run-cancellation/iterations/2026-10-09-prethread-stop/results.md) observed one visible Stop to a real prepared runner run. One matching lookup and cancel made it terminal before acknowledgement release; no native thread, event, container or runner turn-ledger file exists. The authorization ledger reserved one slot but no native model call occurred. The durable cross-store trace join remains unverified; Q11/#22 remain open. |
| Langflow-side execution identity | Distinguish saved flow, configured stage, graph execution and Laomedo invocation before making a cross-store runner binding | [2026-10-09 Phase G result](../../experiments/early-run-cancellation/iterations/2026-10-09-server-identity/results.md) observed two distinct graph run IDs from two API invocations of one saved flow, with the same flow and stage IDs, using a fake runner and zero model turns. A private SQLite snapshot contained both graph ID strings in message/span fields, but the tested default database was inside the disposable container and restart was not exercised. No Laomedo invocation-to-runner request binding exists on this path; Q11/#22 remain open. |
| Playground first-call bridge seam | A visible Send reaches a host-owned persistence point before a real runner request, and Stop can address the same invocation even before acknowledgement | [2026-10-09 seam result](../../experiments/early-run-cancellation/iterations/2026-10-09-playground-seam/results.md) observed a visible Send and ordered Stop lookup/cancel against a fake bridge. A synthetic binding and cancel receipt reopened from host SQLite. The fake did not make a runner POST or exercise the before-ack cancellation race; Langflow restart, executing-graph attestation and cross-store join remain untested. Q11/#22 remain open. |
| Opt-in host join to real Codex at failed-turn scope | A visible Send must reserve a durable host binding before one native POST; distinguish saved-flow and reported graph identity from executing-graph attestation | [2026-10-09 host-join result](../../experiments/early-run-cancellation/iterations/2026-10-09-host-join/results.md) records one real Codex start through the bridge, the exact host/native request and raw-event binding reopened after disposable Langflow restart, and one Langflow trace linked by saved-flow UUID plus reported graph ID in a span. The native turn failed before a shell call or visible Stop; this is not an active cancellation pass, executing-graph attestation or full Q11/#22 acceptance. |
| Long synchronous call timeout | Caller, component and server timeout outcomes distinguish late effects from confirmed cancellation; IF-06/07 preserve partial/unknown state | [EXP-10 synthetic result](../../experiments/long-call-timeout/iterations/2026-10-05/results.md) observed late effects after caller and v2 server timeouts. [EXP-65](../../experiments/post-timeout-job-status/iterations/2026-10-05/results.md) observed `500 JOB_FAILED` before **and after** a late synthetic effect. [EXP-66](../../experiments/timeout-trace-integration/iterations/2026-10-05/results.md) observed a live synthetic call with a durable partial Laomedo trace and no redispatch after store reopen. [Merged Laomedo #70](https://github.com/amadou-6e/laomedo/commit/352a98146674ac8dbcdc76e1155054a78cdacb12) adds regression tests for effects before timeout/after crash and non-downgrade after a lookup error; these fixes were **not** exercised by a new live call. The [proposed reconciliation contract](contract/timeout-reconciliation.md) is only partially exercised: real agent and cancellation remain untested; first-slice gate not accepted |
| Langflow Playground Stop to native runner | A visible Stop click during an active graph must correlate to the bound native run and produce a native cancellation request; the UI disappearing alone is not cancellation proof | [EXP-89 pinned result and five machine-file hashes](https://github.com/amadou-6e/laomedo/blob/a97ad507fcd41af332e3d9ff77d2b0ef0b907487/experiments/exp89/RESULTS.md), [machine-written Case A](https://github.com/amadou-6e/laomedo/blob/a97ad507fcd41af332e3d9ff77d2b0ef0b907487/experiments/exp89/evidence/case-a.json) SHA-256 `24baf9d36276f01b7068e5832ed57f14f73dcae8b916d69d6b36a69cad597abe`, and [complete runner journal](https://github.com/amadou-6e/laomedo/blob/a97ad507fcd41af332e3d9ff77d2b0ef0b907487/experiments/exp89/evidence/journal.jsonl) SHA-256 `9902f3058cfaac0e3cc8cd146795001fdc554a130724d7dc2934c3288eecf31c`; the [derived summary](https://github.com/amadou-6e/laomedo/blob/a97ad507fcd41af332e3d9ff77d2b0ef0b907487/experiments/exp89/observation.json) is not the primary evidence. In pinned Langflow 1.12.3, the visible Playground Stop click completed while a synthetic runner acknowledgement was held, but no runner cancel arrived in eight seconds and the acknowledgement still arrived. This **fails propagation for the tested `start` path**. Whether Langflow signalled the component is **unknown**. The blocking `fresh` case did not complete a visible Stop click and is inconclusive; the completed-run control had no active Playground Stop. Zero model turns. Real-agent Stop, native turn status and crash cleanup remain unverified; Q11 is open. |
| Langflow feasibility | Verify all components remain usable, artifact refs can cross node types, and selective rerun capability before promising it | Not executed |

Related observations in [shared contracts](../../architecture/shared-contracts.md)
do not establish these new target guarantees. Pin the Langflow version and
test environment when recording actual evidence.

## Bounded host-join continuation, 2026-10-09

The [fresh continuation](../../experiments/early-run-cancellation/iterations/2026-10-09-host-join-stop/results.md)
passed visible active-command Stop and the durable identity join together:
one bridge start/cancel, one native start/cancel, native `interrupted`, confirmed
runner cancellation, exact-container absence, and the same host binding and
one Langflow trace after restart. Shared ledger 8/12, 87 private partial events,
zero redispatch. The earlier failed-turn row remains historical evidence. This
does not attest the executing editor graph or establish #93's outage/real
push-credential guarantees; no issue state or maturity changed.

The earlier rows are historical. The missing combined Stop-plus-join observation
is now addressed at active-command scope only; pre-thread Stop has not been
composed with this durable join.

## Develop-based combined observations, 2026-10-09

The [fresh develop-based integration](../../experiments/early-run-cancellation/iterations/2026-10-09-develop-join/results.md)
composes the durable host/native/Langflow join across restart with visible Stop
at both prepared and active-command points. The pre-thread case submitted no
native model call; the active case submitted one. Both retained exact cancel
attribution, clean host terminal receipts and no redispatch. The original active
classifier result remains inconclusive, with a separate retrospective failed-read
explanation. The conservative ledger is 10/12. Earlier paragraphs retain their
dated scope. This does not accept the broader target, attest the executing graph,
close #22/#93 or establish outage, timeout or production-login guarantees.

## Native host wait reconciliation, 2026-10-10

The [two one-shot #66 cases](../../experiments/timeout-trace-integration/iterations/2026-10-09-native/results.md)
passed real Codex cancellation before and during the named file effect after a
five-second host adapter wait timeout. IF-06 retains the timeout projection;
IF-07 retains partial receipts, the same durable invocation/native identity and
known FIRST effect after fresh-process reopen. Native interrupted and explicit
runner confirmation establish cancellation for that exact run, with verified
container absence and one start/cancel per case. Neither timeout nor cancellation
is interpreted as no effects. Shared ledger 12/12, no retries. This is bounded
host-wait evidence, not a new Langflow server 408, automated ingress, graph resume,
semantic success or full Q11/#93 outage and push-revocation acceptance. Historical
rows above keep their dates and limits.
