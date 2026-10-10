---
title: Local runner API boundary
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Local runner API boundary

This page owns the tested single-user local HTTP control plane used by the
[Codex pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md).
It is narrower than production authentication, which remains with
[specs #129](https://github.com/amadou-6e/specs/issues/129). The runner binds
only to host loopback. Docker Desktop can still route a bridged container to
that listener through `host.docker.internal`, so loopback binding alone is not
an access boundary.

On startup, the runner creates or reuses a random 64-hex API capability at
`<private-runner-state>/api-token`. Every `GET` and `POST` under `/v1/runs`
requires `Authorization: Bearer <api-token>`. Missing or incorrect capability
returns HTTP 401 before reading a run or reserving a turn. This covers fresh
start, status, resume, cancel, and artifact selection where supported. The
capability is separate from the model login, never belongs in flow JSON or
agent command containers, and may be mounted read-only into a trusted
Langflow server. Every custom component and other code running in that server
can then read it. On Windows, the private state directory ACL provides the
file boundary; Unix `0o600` does not establish a Windows ACL.

Fresh `POST /v1/runs` accepts task, model, effort, and exact pinned skill
reference. `GET /v1/runs/{run_id}` returns a persisted run record.
`POST /v1/runs/{run_id}/resume` requires task, model, effort, native thread ID,
and post-run snapshot hash. `POST /v1/runs/{run_id}/cancel` requests stop and
returns HTTP 202 when accepted. Invalid inputs fail before model dispatch where
possible. A failed or timed-out accepted run retains its run ID, category, and
partial events; client timeout is not evidence that remote work stopped.

The proposed [early-run and cancellation handoff](early-run-cancellation.md)
adds `POST /v1/runs/async` with a caller-supplied request identity and early
queryable run ID; it leaves this synchronous API intact. Its pre-dispatch
cancel, idempotency, restart and positive-confirmation rules are target
behavior, not yet product-validated. An accepted cancel request alone is not
remote cancellation.

The single-user Codex runner may expose a `native_error_summary` for the
current native turn. Its categories are exact values from the pinned CLI
app-server `codexErrorInfo` schema, with unknown variants mapped to `unknown`.
It may count error and retry events and retain integer HTTP status codes from
the four schema variants that carry them. The summary and public
`error_category` must never copy free-text messages, URLs, additional details,
account identifiers, request headers, or arbitrary provider fields. If a
failed native turn has no separate runner error, `error_category` may use the
last allowlisted category prefixed by `codex_`. Raw events remain in private
run evidence; this projection does not prove the cause of an authorization or
connection failure by itself.

For active Codex turns, the runner addresses a uniquely named container,
sends native `turn/interrupt`, force-removes the owned container, and verifies
removal on cancel or timeout. If removal cannot be verified, it records
`container_termination_unverified` instead of reporting a clean stop. A no-model
Docker canary established this teardown path after the 2026-10-01 pilot; that
pilot itself observed cancellation status and 39 retained events but did not
verify immediate container termination. A cancel before `turn/start` can still
reserve a turn before interruption. No atomic cancel/dispatch guarantee is
claimed. The permission file content did not change; the runner accepts only
its reviewed CRLF and LF byte hashes for Windows and Linux checkouts.

Acceptance for this local boundary requires an unauthenticated bridged worker
request to return 401, an authorized request to succeed, a private token file
absent from the agent mounts, and a no-model cancel/timeout probe to observe
owned-container removal. These checks do not establish hosted or multi-user
tenancy, complete network isolation, or production credential lifecycle.

## Native turn and outstanding commands (#24)

Codex `turn/completed` ends the observed native turn, not necessarily its shell
commands. Project each observed command identity separately: completion observed,
allowlisted terminal status, integer exit code, and raw event/output-event indices.
Output bytes remain in private raw evidence rather than being copied into the
command summary. Ignore events explicitly belonging to another turn. An absent
completion, unidentified command, or unrecognized status stays unknown. Do not
infer command cancellation, denial or success from controller/container teardown.
A completion item missing status establishes terminality only if it reports an
integer exit code; boolean values are not exit codes. Events without a turn ID
are conservatively attributed to the current observed turn.

When the native turn completes with an outstanding command, record the native
status as `native_turn_status: completed`, keep `native_answer` and the command
summary, but record run `status: unknown` and
`error_category: outstanding_command_completion_unknown`. Do not advertise the
answer as completed output: `answer` is null, `snapshot_ready` is false, and
`post_run_hash`/`output_ref` are null. Do not create a new post-run snapshot, permit
artifact selection, or permit resume from that incomplete attempt. On resume,
invalidate the prior artifact identity before dispatch; an older retained snapshot
must not be relabelled as this attempt's output. Persist summaries per turn and in
the run record so evidence remains queryable after runner restart.

This route exposes outstanding commands rather than adding an unbounded drain.
Existing controller shutdown and owned-container cleanup remain unchanged.
Successful cleanup establishes removal only. A cleanup failure retains the
existing unverified-termination failure, with no snapshot readiness.
The run's `controller_cleanup` is `not_started`, `pending`, `confirmed`, or
`unverified`; `confirmed` does not change an outstanding command's unknown status.
Late native notifications after the observed boundary are not awaited or claimed
reconciled.

If every observed command has an explicit terminal notification, normal snapshot
validation may proceed. Preserve failed/declined/cancelled command outcomes and
nonzero exits; terminality is not task success. A recovered command failure need
not fail the whole agent run. Neither native completion nor `snapshot_ready`
attests semantic correctness, missing/unobserved commands, detached descendants,
or a stable workspace against processes outside the owned runtime. This change
does not alter permissions, authentication, model budgets or OpenCode semantics.

Historical #24 integration limit: at that revision, Langflow component polling, durable join and
trace reconciliation do not classify `unknown` as terminal. They can continue
waiting until their deadline even after `controller_cleanup: confirmed`; they
must not claim artifact readiness or semantic success. Accurate end-of-attempt
liveness for this route is follow-up under the existing
[node lifecycle issue #20](https://github.com/amadou-6e/laomedo/issues/20).
This result is runner-level coverage, not end-to-end Langflow unknown-state
presentation. No issue text or scope was changed to claim that work implemented.

## Ended attempts with unknown outcome (#20 follow-up)

The runner persists `attempt_finished: false` when an attempt starts, and writes
`true` only in its final record after cleanup has returned or failed. Prepared
records and older records without the field are not evidence of an ended unknown
attempt. This marker describes runner attempt liveness, not command outcome,
semantic success, cancellation confirmation or verified container removal.
`controller_cleanup` separately distinguishes confirmed and unverified cleanup.

The updated component, join controller and trace bridge stop waiting for
`status: unknown` only when `attempt_finished` is exactly boolean true. Missing,
false, string and integer values do not authorize that transition. They retain
unknown outcome and false artifact readiness, rather than converting the run to
completed or cancelled. Existing terminal-status semantics are unchanged. A
fresh node surfaces the existing error category immediately and keeps its run
identity; status output retains trace references and the ended-attempt marker.
Stop sends no additional cancel to an already-ended correlated attempt.

The authenticated status adapter and join HTTP projection retain the marker.
The durable store accepts an unknown terminal receipt only with the explicit
finished marker, preserves the exact native binding, and stores unknown run and
invocation outcomes with `evidence_complete: false`. Exact receipt replay is
idempotent, conflicting terminal outcomes remain refused, and existing workflow
timeout/crash records stay preserved alongside the later native receipt. No
redispatch, new start, output attestation or retry follows from this observation.

This is a credential-free lifecycle follow-up. It does not establish a live
Codex result, a new UI Stop guarantee, lease revocation or outage recovery.
The current effect-ingestion predicate does not accept an invocation newly
projected to `unknown`; a later trusted effect for that route is refused, not
silently recorded as success. Existing timeout-preserved effect ingestion is
unchanged. Legacy records missing `snapshot_ready` are projected conservatively
as false; this does not itself invalidate a stored snapshot hash.
