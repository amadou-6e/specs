---
title: Timeout and late-effect reconciliation
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Timeout and late-effect reconciliation

This is the proposed first-slice Laomedo boundary for [#66](https://github.com/amadou-6e/laomedo/issues/66).
It is informed by [EXP-10](../../../experiments/long-call-timeout/README.md)
and [EXP-65](../../../experiments/post-timeout-job-status/README.md), not an
implemented or accepted behavior. Langflow still owns graph sequencing;
Laomedo owns durable identity, receipt and status projection. No component
retries a timed-out agent invocation automatically.

## Correlation and durable order

Before a native call that may dispatch an agent, durably reserve `run_id`,
`trace_id`, `stage_id` and a fresh `invocation_id` with frozen graph and
configuration refs. Record the dispatch attempt **before** sending the call;
failure to commit the reservation refuses dispatch. A later timeout, job
status observation or effect receipt must refer to these same IDs. A job ID
returned after dispatch is an additional native correlation field, not a
replacement for Laomedo IDs. Receipt order is append-only and receives a
local sequence; it is not proof of a unique external action.

The first slice may store one agent invocation, but identities must not
conflate run, stage, invocation, native job and native agent session. A
duplicate or conflicting source delivery is retained with uncertainty, not
silently merged. On backend restart, preserve committed receipts, mark any
still-dispatching run `crashed`, fence redispatch, and leave any timed-out run
and its incomplete trace inspectable. A restart does not resume Langflow.

## Outcome projection

Keep these dimensions separate:

| Observation | Workflow/invocation projection | Effect and trace projection |
| --- | --- | --- |
| Synchronous `408 EXECUTION_TIMEOUT` | Workflow `timed_out`; affected IF-06 invocation `failed` with provider timeout classification, if its identity is known | `evidence_state=unknown` or `partial`; external effect `unknown`, not `none` or `cancelled` |
| GET returns HTTP 500 and `detail.code=JOB_FAILED` | Native Langflow job `failed`; do not rewrite the earlier timeout as a successful or confirmed-cancelled invocation | Effect remains unknown until independently observed; record the native response as an IF-07 receipt |
| GET returns HTTP 500 without `JOB_FAILED`, or lookup is inaccessible | Native status `unknown` and query error | Do not infer job failure from HTTP status alone |
| Correlated runner effect arrives after timeout or terminal native job status | Keep the original terminal workflow/invocation outcome and append an effect receipt under its IDs | Effect `observed`; trace remains `partial` until its required evidence is genuinely complete; never project “failed with no effects” |
| Runner positively confirms cancellation | Cancellation may be reported only for the affected remote invocation, with its source evidence | Preserve earlier receipts and any effects; cancellation does not erase them |

For `IF-11`, expose exact delivery count and last received sequence,
`stream_state=partial|unknown`, and `action_uniqueness=uncertain` unless a
source-specific identity guarantee is verified. A later effect receipt may
change the effect projection but does not retroactively make the timed-out
Langflow graph completed. An absent effect receipt means **unknown**, not
proof of no effect. Usage/cost remains unknown unless measured.

## Required validation before acceptance

Use the pinned EXP-65-style synthetic sequence: persist identities; dispatch
once; observe `408`; observe `500 JOB_FAILED` before **and after** the delayed
runner effect; attach that effect to the same invocation; restart the Laomedo
store and inspect the durable partial trace without another dispatch. Include
controls for missing/invalid `detail.code`, omitted effect, duplicated source
delivery, crash before reservation and crash after dispatch. Test that neither
HTTP 500 nor `JOB_FAILED` yields “no effects” or confirmed cancellation.

This synthetic test is necessary but insufficient for first-slice Q11
acceptance. [#22](https://github.com/amadou-6e/laomedo/issues/22) must
provide early real-runner identity and a supported cancellation result;
separate bounded real-agent tests must show whether cancellation stops or
outlives native work, with IF-06/07 partial evidence preserved. Until those
tests exist, validation remains unaccepted.
