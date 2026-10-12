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

### Observed interactive recovery, 2026-10-12

The recovery ran through the saved Langflow flow API for graph
`68a890ed-9022-4ad1-a587-61d61124e23c`, not a direct runner-only call. The graph
retained eight nodes and ten edges. Its frozen issue, Skill, Codex Agent,
integrated Contract and direct Publisher produced a confirmed draft PR.

| Check | Observed |
| --- | --- |
| Source and merge | `4281d93`, delivered by [Laomedo PR #152](https://github.com/amadou-6e/laomedo/pull/152) (`73317b0`) |
| Frozen manifest SHA-256 | `0404c689d3355dcc61ff0cafb4b9b42b540a42f7e49a514ab7f7dab85b478941` |
| New run | `7e227205-f6d6-4cc7-87da-f95d3a78c7ff` |
| Execution evidence | `completed`, `native_trace_closure`, `evidence_complete: true`; all four shell commands completed with exit zero |
| Agent precheck | Installed, three calls; required-field rejection followed by valid submission |
| Publication | [Disposable draft PR #9](https://github.com/ga84jog/laomedo-exp104-disposable-20261007/pull/9), independently read back as draft on `langflow-demo-20261012-c` |
| Published commit | `ddaed14f8d49347455d7cce8951bb0663e319045` |
| Exact published report | 244 bytes; SHA-256 `240f33ca585cce2b89b9e77d7cc4772f65ccd4ea3031226452b9979967363934`, matching the frozen credential-free fixture |
| Cumulative campaign limits | 2/4 submitted turns, one confirmed push and one confirmed draft PR; both write allowances now consumed |
| Final authority | All campaign grants revoked, no unknown effect or remaining owned executor container |
| Regression checks | 659 host tests, 11 skips; 43 pinned Langflow component tests; final Python 3.10/3.13 CI passed |

The initial failed run and its extra-newline artifact remain preserved as unknown
with outstanding-command evidence. It is not relabeled as successful. The
recovery used the same ledger and write-budget databases, unchanged permissions,
existing login custody and 600-second handoff. Repeating this graph cannot
implicitly rearm a consumed request or replenish its publication budget.

The local viewer uses automatic login on loopback only and a persistent SQLite
volume. Langflow's API separately required a local API key; it was provisioned
automatically and retained only in ignored local state. It is not a provider
login or an additional human sign-in. No credential values or raw transcripts
appear in this record or the published report. Exact fixture equality establishes
report contents, not a general credential-exfiltration audit.

This demonstrates the bounded single-user local path for this fixed sample
report. It does not prove arbitrary issue implementation, hosted isolation,
semantic code correctness, or all failure/rejection routes in this campaign.


### Standing local development allowance, owner decision 2026-10-12

The owner selected four submitted model turns per manual Run, including
timeouts, with a fresh branch and at most one push and one draft PR per run in
`ga84jog/laomedo-exp104-disposable-20261007`. This allowance persists until
explicitly disabled. It does not reset the preceding campaign's ledger or
consumed write budgets. Unknown writes remain consumed and cannot be repeated.

The prepared configuration uses an independent local runner on port 8780,
separate private state outside Git, the existing provider login and host-only
GitHub connection, unchanged permissions and a finite 600-second handoff.
It continues to accept only the registered frozen issue, pinned skill and
contract, and publishes only the exact bounded report after accepted-success
validation. Each new request gets a host-generated branch; replaying its
request identity returns the existing run. No fresh dispatch is accepted while
a run is prepared or running. Resume is excluded on this demo route.

The issue node exposes a readable selected URL and Task form, plus advanced
structured frozen context. Base64 survives only as hidden compatibility fields.
Changing the URL does not fetch another issue; a mismatch refuses. This is not
a live GitHub issue selector or evidence of arbitrary issue implementation.

Activation requires independent review of the source and concrete policy,
clean source pinning and recorded fixture hashes. The first live Run is reserved
for the owner; automated verification must use fixtures. Disabling the policy
prevents new starts but does not cancel an active run. The existing Stop and
lease controls still govern it. The allowance is local scope control, not a
same-user Windows authorization boundary. No live standing-policy run has
been observed yet.
