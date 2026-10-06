---
title: Native runner to invocation correlation
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Native runner to invocation correlation

This is the proposed first-slice binding for [Laomedo #83](https://github.com/amadou-6e/laomedo/issues/83),
following the bounded native cancellation evidence for [#22](https://github.com/amadou-6e/laomedo/issues/22).
Langflow integration owns the durable Laomedo run and invocation record;
agent execution owns the local runner and its native events. Run traces
consumes the correlated receipts. These identities must not be conflated:

```text
RunnerBinding {
  workflow_run_id: string, trace_id: string, stage_id: string,
  invocation_id: string, runner_request_id: string,
  runner_provider: string, runner_run_id: string,
  raw_event_ref: Ref
}
```

The first slice has one fresh Codex invocation. Its `runner_request_id` is
the already reserved `invocation_id` UUID; this avoids generating an
unpersisted request identity between reservation and dispatch. Before the
runner POST, persist the Laomedo run/trace/stage/invocation identity, frozen
inputs and one dispatch attempt. Refuse dispatch if that write fails. The
runner request uses the same ID on an explicit retry of an uncertain response
and the same exact body; no timeout or restart automatically retries.

The first valid runner acknowledgement binds its provider, runner run ID and
raw-event reference to that reserved invocation in one durable transaction.
The runner response's request ID must match the reserved ID; the raw-event
reference must name that exact runner run, not an arbitrary path. Repeating
the identical binding is idempotent. A different runner run ID, provider,
request ID or raw-event reference for the same invocation is a conflict;
one runner run cannot be attached to two invocations. Acknowledgement before
the dispatch reservation or for an unknown run/invocation fails. If the
acknowledgement is lost, the reservation remains inspectable as dispatched
with an unknown runner identity until the same request is explicitly
reconciled. Neither a failed binding write nor backend restart silently
starts another agent.

Later runner status, cancellation and effect observations carry both the
Laomedo invocation identity and the bound runner identity. They append IF-07
receipts under that same `trace_id` and can be inspected after reopening the
store. An effect may arrive before or after timeout and retains its original
invocation; a status lookup error does not erase a prior observation. The
runner's local `cancel_confirmed` means its teardown boundary was verified,
not by itself that a native turn stopped. Evidence stays `partial|unknown`
until its actual completeness is established. The raw-event reference is a
pointer to private data, not a copy of raw events into a public trace.
If the runner wait deadline expires after dispatch, the workflow outcome is
`incomplete` with IF-09 terminal reason `runner_result_pending`, a timeout
error class and an append-only `runner_result_pending` receipt. The native
outcome and evidence completeness remain unknown. This does not imply native
cancellation, and a later effect can still attach to the same invocation.
Cancellation must target the bound native run, not merely a caller-supplied
execution ID.
A complete runner rejection is recorded as a failed invocation without
inventing a native run binding. A missing or uncertain response is not such a
rejection.

Synthetic acceptance must cover exact replay, conflicting and cross-invocation
bindings, malformed references, missing pre-dispatch reservation, a late
acknowledgement after timeout, cancellation and effect receipts under the
same IDs, and reopen without redispatch. This contract does not establish
Langflow UI Stop propagation, real-agent timeout effects, or runner-crash
orphan cleanup. Those remain separate first-slice gates under #22/#66 and
[Q11](../design/decision-readiness.md).

## Read-only recovery after a lost acknowledgement

For [Laomedo #87](https://github.com/amadou-6e/laomedo/issues/87), freeze a
digest of the exact runner request body alongside `runner_request_id` before
the POST (`sha256:` of canonical JSON with sorted keys and compact separators,
excluding the top-level `request_id`, matching the runner's current digest).
A fresh bridge must verify that the body it sends still has that
digest. The local runner offers authenticated `GET /v1/requests/{request_id}`:
it only reads durable runner records and returns one matching run's
`client_request_id`, `request_hash`, `run_id`, `provider`, `raw_event_ref` and
current status. It rejects malformed IDs and conflicting multiple matches;
it never starts, resumes or cancels a run. The response omits private raw
events, task text and credentials.

Recovery is an explicit operator/controller action, not an automatic retry.
After a lost acknowledgement or binding-write failure, Laomedo reads that
endpoint using the original request ID and binds only if its request digest,
provider, run ID and event reference all match the frozen invocation. A
not-found lookup, unreachable runner or ambiguous response leaves the
invocation `incomplete`; none proves the POST failed or authorizes another
POST. Exact rebinding is idempotent. After binding, cancellation can target
the recovered native run.

Every post-dispatch exception must leave a bounded, append-only IF-07/08
receipt with an error category and the original invocation ID. If the native
outcome is uncertain, IF-09 uses `incomplete` with a machine-readable reason;
the trace must not remain silently `dispatching` or claim native cancellation.
A runner `409 request_identity_conflict` is an explicit conflict receipt,
not a no-run rejection. These synthetic recovery checks do not establish
Langflow UI Stop, real-agent timeout effects or runner-crash cleanup.

The synthetic implementation on Laomedo #83 exercises a local authenticated
runner HTTP endpoint with a fake agent transport; it does not exercise a real
model, Langflow UI wiring, or agent-container teardown.
