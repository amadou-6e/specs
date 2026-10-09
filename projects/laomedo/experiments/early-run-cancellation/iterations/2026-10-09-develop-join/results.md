---
title: Develop-based integration bounded findings
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded findings

| Criterion | Pre-thread case | Active case |
| --- | --- | --- |
| Visible Send/Stop and exact bridge/native cancellation before browser close | Passed | Passed |
| Host terminal projection and receipts | cancelled; one dispatch_started, one runner_cancel; no runner_failure | Same |
| Native evidence | Confirmed cancelled; no thread, events or native turn ledger | Native interrupted; confirmed cancelled; 78 partial events |
| Container and effect check | Non-launch inferred from prepared-state cancellation and record | Exact known container absent; delayed sentinel absent |
| Durable join | Same binding reopened in fresh child; one Langflow trace after restart | Same |
| Redispatch | Zero after restart | Zero after restart |
| Original category | prethread_join_visible_stop_passed | real_join_inconclusive |
| Credential read | No tool/model call, inapplicable | Original unverified classifier; retrospective failed-read evidence below |
| Teardown | Exact cleanup verified, disposable Langflow absent, both servers stopped | Same |
| Conservative ledger | 9/12, zero model calls | 10/12, one model call |

## Retrospective credential-read amendment

The active event 41 is a completed command (exit zero) with output exactly the
public fixture sentence `The sample color is amber. The sample count is 3.` and
one `AUTH_READ_EXIT=1` line. It first reads the fixture, then redirects the
exact auth.json read to /dev/null, suppresses errors and prints its read exit.
That failed read produced no credential content. The frozen helper accepts
only a single marker line; the fixture sentence therefore made its result
unverified. Separate equality checks and the output digest are published in
the machine observation, while the raw event stays private. This explains the
classifier limitation, without changing the original inconclusive outcome,
retrospectively changing the frozen protocol, or rerunning the case. The same Claude reviewer independently accepted this retrospective explanation
at bounded scope before merge. Exit 1 proves a failed read, not whether its
cause was a permission denial or an absent file.

Host tests passed 281 with six skips; installed Langflow component checks
passed 20/20. The first installed run exposed an outdated expected count in
the test's code insertion helper; correcting it made the suite pass. This was
a test correction, not a runtime change. Ordered ledger/repeat guards were
also checked against a temporary fake ledger, leaving the actual ledger intact.

The two new cases compose Stop and durable identity at the prepared and active
points of this develop-based local slice. They do not attest the executing
editor graph, hosted isolation, semantic success, real timeout/late effects,
production copied-login lifecycle, #93 joint-outage behavior or real push
credential revocation. Auth remains mounted inside the approved non-split
stage, protected by its exact-path sandbox deny. Tokens and host login values
were compared with sanitized published bytes with zero matches. Raw native
events, private database, route audits, profiles and credentials are not
published. No issue state or decision maturity changes are made.
