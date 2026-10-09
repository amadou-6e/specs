---
title: Host join and real visible Stop bounded result
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded result

The [published continuation result](https://github.com/amadou-6e/laomedo/blob/266536fefa856c02d2482445387b83289ad069d1/experiments/exp22/PHASE-G-CONTINUATION-RESULTS.md)
records `real_join_visible_stop_passed`: one real active-command cancellation
and the durable host/Langflow/native identity join passed in the same local
run. This addresses the combination missing from the previous failed turn.

| Criterion | Observation | Assessment |
| --- | --- | --- |
| Exact dispatch | One browser Send, one authenticated bridge start and one native runner start; host/native request digest and run identity matched | Observed; shared ledger 8/12 |
| Visible Stop attribution | One visible Stop after the native long command began; exact bridge client cancel before exact runner cancel; terminal observation before browser closure | Observed in one bounded real turn |
| Native cancellation | Native `interrupted`, terminal runner `cancelled` with confirmation, exact container absent, delayed sentinel absent | Positive active-command cancellation |
| Durable join | Fresh child reopened the exact host binding after bridge shutdown; recreated Langflow retained one trace linked by saved-flow UUID and reported graph-run ID in a span | Positive identity join across restart; graph execution not attested |
| Redispatch | One native start total, zero new starts after restart | No redispatch observed |
| Partial evidence | 87 private native events, including interruption, retained and hashed | Partial trace preserved |
| Credential and token handling | Content-free agent `auth.json` read denied at event index 45; neither local token occurred in sanitized result, pins, teardown or route audits | Tested exact read denial and publication check; login still mounted inside the non-split stage |
| Cleanup | Exact runner cleanup verified; disposable Langflow absent; bridge and runner servers stopped | Observed |

This establishes the bounded local cancellation-and-join path. It does not
attest the executing editor graph, semantic task success, hosted isolation,
real-agent timeout effects, runner/lease joint-outage behavior or real push
credential revocation under #93. The copied-login lifecycle stays unresolved
under specs #129. The broader target contract is not marked fully accepted;
no issue state or decision maturity is changed by this evidence update.

The pre-thread Stop point was not composed with this durable join. Its earlier
Phase F observation remains a separate result; this continuation covers the
active-command point only.
