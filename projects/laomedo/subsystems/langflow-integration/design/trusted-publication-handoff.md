---
title: Trusted output-validation publication handoff
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Trusted output-validation publication handoff

Engineering mechanism for [decision 0007](../../../decisions/0007-trusted-output-publication-handoff.md), tracked by [Laomedo #138](https://github.com/amadou-6e/laomedo/issues/138) and [specs #345](https://github.com/amadou-6e/specs/issues/345). This is host-side opt-in composition, not an activated deployment or live-publication pass.

## Ownership and admission

The trusted host constructs `PublicationController` with its mediator store, a finite positive lifetime, a private artifact resolver, a description builder, an injected provider transport and a provider readback. There is no default lifetime and no ambient GitHub login fallback. The host must explicitly run the startup recovery sweep after the old controller is known dead; it revokes unfinished handoffs and never replays a publication.

Before agent dispatch, the controller registers the existing supervised grant and freezes the Output Contract reference, wall-clock deadline and monotonic deadline in `publication_handoffs`. An opt-in GitHub-scoped launch without a valid Output Contract refuses dispatch. Renewal clamps to those deadlines. Neither agent completion nor graph waiting resets them. The independent lease service continues supervising the same lease; there is no separate publisher grant, grant resurrection or extra sign-in. This remains run scoping, not authorization against another process with the same user's host access.

After verified executor removal, the controller freezes the host-observed answer and resolves the existing private `VerifiedStage`. The artifact's run, repository and branch must match the existing grant, its bundle bytes must match their digest, and its exact stage digest must have a confirmed push receipt under that grant. The controller fixes PR head/base, title/body, a stable handoff marker, `draft: true` and an effect identity. A graph never selects a host path, repository, branch, grant, deadline or publication payload.

The transition to `validation_pending` serializes with mediator intent reservations. All operations through the old agent bearer, including bundle capture/status, are refused after this transition. Any unresolved effect intent makes the handoff `unknown` and revokes it; waiting for a possibly in-flight agent write is not evidence of safe completion.

## Graph and publisher boundary

The Draft PR Publisher node follows the accepted-success route. It sends only an empty POST body to the authenticated local runner's `/v1/runs/{run_id}/publish`. Its convenience checks reject contract rejection, reported failure, interrupted execution and incomplete/unknown evidence before dispatch. These checks are not authority: the host reevaluates the dispatch-pinned contract against its frozen envelope. A forged graph verdict cannot replace that data.

Only contract acceptance with explicit task success, completed executor status and independently established `evidence_complete: true` admits `publication_pending`. The proposed host native-trace closure below can establish evidence availability, not truthful task success. An already-pushed, verified artifact is required; this publisher does not push an agent checkout or create a new bundle.

### Native execution evidence closure

For a supervised Codex invocation, the host records the raw-stream byte offset and existing turn-history length before dispatch. After closing both native trace readers and independently verifying exact executor removal, it checks only that invocation's retained JSONL suffix and submitted turn identities. Every selected native turn must have exactly one completed terminal event bound to the same thread; item identities must be unambiguous and every observed started item must complete. Command completion uses the existing explicit terminal-status/integer-exit rules. Duplicate identities, missing bindings, late items, malformed/truncated/unreadable traces, unfinished tools or unknown cleanup cannot close evidence.

The final retained agent message must equal the host's recorded answer. A ready working-file snapshot and verified controller/executor cleanup are required. The check is bounded to 64 MiB per invocation; a larger trace stays unknown rather than being truncated into a pass. Resuming clears the prior completeness flag and cannot use previous turns or prior raw bytes as proof of the new invocation. Public closure diagnostics contain only schema version, reason and counts, without trace content or credential hashes.

A successful fresh-invocation check sets `evidence_complete: true` and `completion_basis: native_trace_closure`; all missing/ambiguous cases stay unknown. Resumed invocations remain unknown and cannot admit trusted publication: their cumulative workspace may include writes from earlier attempts without closed evidence. Supporting that publication requires a durable closure history for every contributing attempt, outside this preparation's scope. This means the observed native execution evidence was retained and closed, not that the task was accomplished, the model's claims were truthful or a remote effect succeeded. Native provider compatibility, imported graph-to-publisher wiring and live publication still require #139 acceptance. Unsupplied or unsupported transport reader state cannot claim completeness.

The publisher uses the existing mediation journal: the fixed effect identity is persisted as unknown before provider dispatch. A complete rejection is failed; a lost response, inconclusive readback or process loss stays unknown and never causes an automatic resend. Successful readback must identify the exact draft PR number, repository, head branch and commit, base, title, body and marker. Completion is publication acceptance at that scope, not proof that the code is correct.

A local mediation exception is classified from the durable effect row, not its exception type: no intent or a recorded complete rejection may be failed; an unknown intent or confirmed write followed by an error remains unknown. Early or concurrent duplicate publish requests observe the current phase without ending the agent lease or interrupting the first publication. The controller admits only one publication call per run at a time.

## Termination and recovery

Completion, contract rejection, failure, uncertainty, cancellation and expiry revoke the same grant and finish its lease. Cancellation or expiry racing a remote write cannot undo that effect: preserve its journal receipt and never relabel the cancelled/expired handoff as successful. The publisher node also treats a lost HTTP response as unknown, does not follow redirects and exposes only sanitized phase and publication state.

The controller keeps the lease heartbeat through validation. Runner/controller death stops that heartbeat; the existing independent service revokes before exact owned-container cleanup. Its startup sweep and hard grant TTL retain the 60-second orphan bound. No new service configuration is activated by this design. Host shutdown/startup composition must explicitly cancel/recover controller-owned handoffs.

## Verification boundary

Credential-free checks must cover accepted draft publication and exact readback, non-success refusal, forged graph operations, foreign or unconfirmed artifacts, changed requirements, in-flight effects, deadline-preserving renewal, clock rollback, cancellation/expiry during publication, no resend after uncertainty, explicit startup recovery and lease loss while another run remains usable. Pinned Langflow checks cover the real custom node against a fake local response, without a live provider.

The bounded [#100](https://github.com/amadou-6e/laomedo/issues/100) and [#104](https://github.com/amadou-6e/laomedo/issues/104) prerequisite acceptance is recorded; #100's live-provider result is in [specs #344](https://github.com/amadou-6e/specs/pull/344). Live publication still requires [#139](https://github.com/amadou-6e/laomedo/issues/139)'s separate model-turn cap and scoped identity. Native precheck acceptance, independently verified real-run completeness and a deployed graph-to-publisher demonstration are not established by fake transports.

## Integrated contract-route compatibility

The integrated Output Contract's Success port connects directly to the Draft
PR Publisher's existing validation input with its `{route, validation}` envelope.
The publisher unwraps only `route: success` with an object validation. Any
other route or malformed wrapper refuses without a publication HTTP request;
it must not fall back to raw-validation handling. Raw legacy validation remains
compatible and uses the same accepted/success/completed/complete-evidence checks.
Current graphs need no Accepted Validation adapter; historical embedded exports
and their adapter stay intact. Publisher access, expiry, frozen-run
validation and effect reconciliation remain host-owned and unchanged. No
failure/rejection/recovery branch may invoke publication. Combining visible
nodes does not create an authorization boundary within custom Langflow code.


## Fresh interactive demo configuration (2026-10-12)

The owner authorized a new campaign with four submitted Codex turns, counting
attempts that time out, and one push plus one draft PR in the existing disposable
repository `ga84jog/laomedo-exp104-disposable-20261007`. This is separate from the
completed EXP139 ledger (8/10); its grants, consumed write budget and evidence
remain unchanged. This authorization does not cover another repository or an
unlimited service.

The simplified imported graph uses the selected frozen issue and pinned Skill,
Codex Agent, integrated Output Contract and direct Draft PR Publisher. The host
binds the exact request before dispatch and limits the report to one file on the
fresh `langflow-demo-20261012-c` branch. The finite handoff remains 600 seconds;
agent commands keep network-off and authentication-file denial. A durable
one-attempt write budget includes unknown provider outcomes. Repeated graph
clicks cannot renew a consumed task or grant.

The runner and independent services use fresh private state outside Git and
existing provider login custody. Langflow receives only the runner API token as
a read-only mount; the GitHub credential stays in the host connection and does
not enter graph data. The prepared configuration must have an exact reviewed
source and frozen input manifest before activation. Readiness checks are
credential-free or no-model authenticated checks, not live execution evidence.
The user starts the graph through Run component on Draft PR Publisher, which
builds its upstream dependencies. A green component still means returned Data,
not proof of semantic success or publication.

### Interactive recovery within the same campaign

A completed pre-dispatch task-binding refusal exposes the fixed public code
`experiment_request_binding_denied`, without inventing a run or exposing raw
server text. Other complete client refusals expose `runner_dispatch_refused`;
server or transport uncertainty remains unknown. Neither automatically resends.

The first interactive turn produced a report with one extra final newline. Its
exact-byte policy check correctly refused publication, but the helper treated
that completed rejection as pending and the agent ended while its push command
was outstanding. No provider write was attempted. A completed stage-policy
rejection now stops the helper promptly with a sanitized refusal; missing or
ambiguous verification remains unknown.

The recovery archives the old frozen inputs and activation, preserves the same
1/4 turn ledger and durable unused one-push/one-draft-PR budget, and prepares a
new exact task and invocation identity. The task decodes the approved report
from base64, verifies its SHA-256 before committing, and waits for command
completion without repeating an uncertain push. It does not weaken report
validation, renew the failed grant, alter permissions or reset any budget. The
new source and input manifest require independent review before activation.
