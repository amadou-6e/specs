---
title: Native reconciliation result status
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded native result

Both one-shot cases passed. The actual timeout layer was the production host
adapter wait, not a new Langflow server 408. The original synthetic
408/JOB_FAILED/late-effect observations remain unchanged.

| Check | Before effect | During effect |
| --- | --- | --- |
| Native turn / runner status | interrupted / confirmed cancelled | interrupted / confirmed cancelled |
| File at 31-second window | absent | exact FIRST newline, no SECOND |
| Effect projection | unknown, not no effects | observed with trusted file hash |
| Workflow after native cancellation | incomplete; invocation timeout | incomplete; invocation timeout |
| Trace after fresh-process reopen | partial, evidence_complete false | partial, evidence_complete false |
| Original run/trace/invocation/native identity | retained | retained |
| Start / cancel routes | 1 / 1 | 1 / 1 |
| Native private raw event count | 45 | 108 |
| Exact container cleanup / server stop | verified / verified | verified / verified |
| Conservative shared turn count | 11/12 | 12/12 |

The during-effect SHA-256 is
`769de7aa90420fc20b613b9dba39e234821b286f19d63b9298583750d6359335`,
the bytes `FIRST` followed by a newline. The timeout receipt precedes its effect
receipt, followed by the exact cancel and confirmed native-terminal receipt.
No workflow timeout, crash, or prior effect is overwritten by native cancellation.
The [before](evidence/before.json) and [during](evidence/during.json) machine records
contain the full durable receipt projection, selected native boundary events and
private raw-file hashes. Neither case redispatched or resumed the graph.

Deterministic verification includes ten native reconciliation controls, four
HTTP join tests and two probe-cleanup fault injections. The pre-run full suite
passed 294 tests, six skipped. After moving the unchanged probe-only test out of
the wheel suite, the final `d43e5cad51dd2e187810821d6e9f66ffea9f4508` product suite
passed 292 tests, six skipped; the two relocated fault-injection tests passed
separately. Python 3.10/3.13 installed-wheel CI passed on both push and PR runs.
The test-placement CI failure is recovered, not a native cancellation failure.
A local full-suite run also encountered WinError 10053 in an existing loopback
HTTP test. Its focused four-test rerun and the full 292-test rerun passed without
source changes. The intermittent connection abort's cause is not established.

Claude approved implementation at `b2e98a0` and the B1 pre-run amendment at
`bec25c0` in the same session `5442f699-0e3b-4468-9bd7-0452357b66c4`.
Post-run evidence review and final-head CI are merge gates, not implied by the
probe summaries. No issue state or specification maturity was changed.

This satisfies the bounded #66 real-runner before/during-effect verification
alongside the older synthetic timeout evidence. It does not establish an
automatically deployed Langflow 408 ingress, arbitrary effect completeness,
semantic graph success, graph attestation, production authentication or #93's
outage and real push-credential revocation. Q11 and #22/#93 remain broader open
gates; absent file/effect evidence is unknown, and cancellation cannot undo FIRST.

Before publication, the changed spec files and prepared PR bodies were scanned
against the current private Codex access/refresh-token values and both runner
API tokens in memory. No exact credential match was found in 13 inspected files;
no secret value or raw login was printed or committed. This bounded scan does not
prove that every possible transformed secret representation is absent. The login
remains mounted in the native container under the existing sandbox deny, not a
newly verified production credential boundary.
