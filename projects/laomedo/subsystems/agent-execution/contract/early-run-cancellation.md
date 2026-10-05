---
title: Early runner identity and cancellation handoff
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Early runner identity and cancellation handoff

This is the proposed additive boundary for [Laomedo #22](https://github.com/amadou-6e/laomedo/issues/22).
The existing synchronous `POST /v1/runs` and resume path remain supported;
they do not acquire early identity retroactively. The first slice covers a
fresh Codex run on the authenticated, single-user local runner. It does not
redesign Docker permissions, model login, hosted tenancy or Langflow's graph
scheduler. The prospective [zero-model protocol](https://github.com/amadou-6e/laomedo/blob/7975ffaa1555d7baf39880a578128724e5a08f50/experiments/exp22/PROTOCOL.md)
is not execution evidence.

## Start and identity

`POST /v1/runs/async` accepts the same fresh-run body as the synchronous
endpoint plus a caller-generated canonical UUID `request_id`. The ID binds
the **complete canonical request** for this local runner, not one HTTP POST
attempt. Validate the request and skill references before dispatch. Persist a
new `run_id`, request ID/hash, status `prepared`, raw-event location and the
frozen input/skill snapshot before acknowledging. The authenticated response
is HTTP 202 with that queryable run ID and no claim that a model turn started
or finished. The worker may start only after the response is sent or its
transport attempt has conclusively ended. The same ID and identical body
returns the same run record without a second worker or model turn, even if
the first response was lost or the run became terminal; the same ID with a
different body returns HTTP 409. A different request ID is a new run, not a
safe retry of an uncertain one.

`GET /v1/runs/{run_id}` reports the saved state (`prepared`, `running`, or
terminal `completed|cancelled|failed|timeout|interrupted`) and known native
IDs/partial raw-event reference. Polling is read-only and does not dispatch.
A runner restart marks saved nonterminal runs `interrupted` (or explicitly
unknown if their fate cannot be resolved), preserves their IDs/events and
never automatically resumes or replays them. An acknowledgment timeout must
be resolved with the **same** `request_id`, not an uncorrelated new POST.

## Cancellation and evidence

`POST /v1/runs/{run_id}/cancel` for `prepared` may atomically prevent worker
creation/turn dispatch and report `cancelled` with positive local evidence.
For `running`, HTTP 202 means only `cancel_requested`; the runner must attempt
its supported native interrupt and container teardown. The consumer polls the
run record and reports remote cancellation only after the runner confirms
`cancelled` and retains the native/teardown evidence. A timeout, disconnected
client, Langflow `JOB_FAILED`, accepted cancel request, or missing run ID is
not confirmation. A terminal completed/failed/timeout record is not rewritten
to cancelled by a late request. Raw events committed before stop remain
queryable. A cancel/turn-start race must end in an explicit recorded outcome;
it cannot silently dispatch another turn.

The Langflow Codex node may expose an additive nonblocking start operation
that returns the early run reference, followed by its existing status/cancel
operations. A graph that waits for completion must retain that ID while
polling and must not treat cancellation of its own HTTP wait as remote stop.
Whether Langflow UI Stop reliably invokes node cleanup is a **separate
unverified capability**; do not promise automatic Stop propagation before a
bounded installed-runtime test demonstrates it.

## Acceptance boundary

Credential-free fake-transport and authenticated local-HTTP tests must cover
early acknowledgment, duplicate/lost-response identity, conflicting payload,
cancel before worker and during a blocked tool call, timeout/cancel races,
restart fencing, preserved partial events and turn-ledger counts. An explicit
negative control must fail if a second turn starts. These checks establish
the local mechanism only. Real-agent acceptance additionally requires a
separately frozen cap and positive native cancellation/container evidence for
both pre-thread and active-tool points, linked to IF-06/07 partial trace.
[Q11](../../langflow-integration/design/decision-readiness.md) remains open
until those observations exist.
