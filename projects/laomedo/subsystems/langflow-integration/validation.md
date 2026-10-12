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

## Frozen-bundle verifier recovery, 2026-10-12

AMENDMENT-06's branch prerequisite worked and its real imported graph reached
the host through the mailbox, freezing one bundle. The composition incorrectly
expected `advertised_commit` in the freezer receipt. The field is derived by
the validated private bundle reader, not supplied by that receipt. Verification
never started; the helper stopped with `stage_pending_no_retry`, and the graph
routed the invalid final submission to rejection. No provider write occurred.
Ledger 6/10, grants revoked and cleanup verified. See the
[machine observation](https://github.com/amadou-6e/laomedo/blob/e1eaaa4272bb22e3b95da771a815166c09befedc/experiments/exp139/AMEND06-OBSERVATION.json)
and [result](https://github.com/amadou-6e/laomedo/blob/e1eaaa4272bb22e3b95da771a815166c09befedc/experiments/exp139/AMEND06-RESULTS.md).
Executed source and manifest remain the AMENDMENT-06 pins in the next section.

[AMENDMENT-07](https://github.com/amadou-6e/laomedo/blob/e1eaaa4272bb22e3b95da771a815166c09befedc/experiments/exp139/AMENDMENT-07.md)
corrects both verification dispatch and downstream artifact resolution to use
the existing checksum-validated private reader. It does not execute host Git
against agent-owned configuration. The regression feeds a real freeze receipt
and captured bundle into the composition boundary and refuses tampering before
the verifier is called. The
[Docker control](https://github.com/amadou-6e/laomedo/blob/e1eaaa4272bb22e3b95da771a815166c09befedc/experiments/exp139/VERIFY-CONTROL.json)
verifies a copy of the actual retained capture under a synthetic active binding,
with limits and cleanup passing, zero model turns, no login and no provider
writes. This is integration evidence, not live publication acceptance.

Candidate source `e1eaaa4272bb22e3b95da771a815166c09befedc`, manifest
`3a0675e1c84886fa7906ed39115f099f51bafdc8f274f38f937408556ac63dc0`.
Eight consumed requests and six used turns are retained. Permission, credential
custody, relay and write budgets remain unchanged. Exact-source review, checks
and explicit recovery activation approval precede the fresh success request.
Published-byte readback remains unverified.

## File-relay live result and task correction, 2026-10-12

The owner approved AMENDMENT-05 after Claude review and passing final CI.
Its fresh imported graph used one real Codex turn, bringing the ledger to
5/10. It retained exact report bytes and closed twelve native items, but the
agent reported task failure. The contract accepted that form and routed to
failure. No provider push or draft-PR attempt occurred; the run grant was
revoked and container cleanup verified. Both campaign host trees were stopped.

See the [machine-written observation](https://github.com/amadou-6e/laomedo/blob/190de01a6e2157ca521ba91a1aaea2b72fe2e742/experiments/exp139/AMEND05-OBSERVATION.json)
and [result](https://github.com/amadou-6e/laomedo/blob/190de01a6e2157ca521ba91a1aaea2b72fe2e742/experiments/exp139/AMEND05-RESULTS.md).
Executed source was `6f6a5c7e7936adfe8534e62cbd6dcdd5a9747e29`, manifest
`b58a3017664577c3b4177cb055e11d64d0d60c274cf4ffd34b1541425a9a327a`.
The preserved checkout had detached HEAD and no configured local run branch.
The helper refused before writing a journal or sending a mailbox request.
The [network-none dummy control](https://github.com/amadou-6e/laomedo/blob/190de01a6e2157ca521ba91a1aaea2b72fe2e742/experiments/exp139/BRANCH-CONTROL.json)
reproduces that failure and succeeds after explicit branch creation. This is
not a live provider success claim.

The owner approved task-only
[AMENDMENT-06](https://github.com/amadou-6e/laomedo/blob/190de01a6e2157ca521ba91a1aaea2b72fe2e742/experiments/exp139/AMENDMENT-06.md):
require creation of the named run branch before committing and use a fresh
request/grant identity. Seven consumed requests and five used turns remain
retained. Permissions, relay, credential custody, scope and the unused
one-push/one-draft-PR budgets do not change. Source and input manifest is
`6e7b5b4bbdc8debd2375685cd66a15f43db5fd5315d95a1d1e548a6961cc560c`.
Claude approved the candidate; passing host tests and final CI remain activation
gates. Live publication and published-byte readback are still unverified.

## Prospective file-relay recovery, 2026-10-11

The owner increased EXP-139's cap to ten total submitted turns, retaining four
used turns. No additional live turn has been submitted. The original one-push
and one-draft-PR attempt budgets are retained. The previous negative findings
below remain historical evidence; the real draft-PR path is still unverified.

[AMENDMENT-05](https://github.com/amadou-6e/laomedo/blob/6f6a5c7e7936adfe8534e62cbd6dcdd5a9747e29/experiments/exp139/AMENDMENT-05.md)
proposes invocation-only helper discovery and a file-mailbox relay to the fixed
host mediator. Commands retain network-off and the exact auth-file denial.
The relay holds only the existing run capability, never the GitHub credential,
and uses the existing host scope, artifact, expiry and write-budget checks.
This is a local experiment transport proposal, not production isolation.

The [machine-written dummy controls](https://github.com/amadou-6e/laomedo/blob/6f6a5c7e7936adfe8534e62cbd6dcdd5a9747e29/experiments/exp139/MAILBOX-CONTROL.json)
use a network-none container, dummy capability and loopback fake mediator.
Login-shell helper discovery and a sandboxed commit/bundle/native push through
the real helper pass against the fake mediator; direct TCP and dummy
auth-file reads are denied; symlinks, FIFOs and directory replacement are refused.
The exact bootstrap also passes with a stub app-server. These controls establish
neither the actual Windows-host route nor real GitHub publication.
The invocation uses opt-in regular-file child stdio to avoid the reproduced
nested Node pipe denial; other runner invocations keep their existing default.
The relay is outside the command sandbox under the controller UID; process
attachment has not been tested. This residual must be explicit in local
configuration approval; direct auth-file denial does not prove that isolation.
Fifteen focused controls and 646 host tests with eleven skips pass. These checks
use zero model turns and zero provider writes.

Source and candidate input pins are frozen at `6f6a5c7e7936adfe8534e62cbd6dcdd5a9747e29`,
manifest `b58a3017664577c3b4177cb055e11d64d0d60c274cf4ffd34b1541425a9a327a`.
The [startup draft](https://github.com/amadou-6e/laomedo/blob/6f6a5c7e7936adfe8534e62cbd6dcdd5a9747e29/experiments/exp139/STARTUP-DRAFT-05.md)
still requires exact-source review, final-head CI and explicit configuration
approval before activation. The cap increase does not itself approve startup.
All consumed requests, private traces and failed attempts must remain retained.

## Imported live recovery, 2026-10-11

The owner-approved AMENDMENT-03/04 recovery used the three remaining real Codex
turns through imported Langflow graphs. **#139 remains incomplete:** the live
draft-PR success path is blocked. See the machine-written
[recovery observation](https://github.com/amadou-6e/laomedo/blob/9d3a297c26f560b344e8affaf5a9bf25e0b77e5b/experiments/exp139/RECOVERY-OBSERVATION.json),
[results](https://github.com/amadou-6e/laomedo/blob/9d3a297c26f560b344e8affaf5a9bf25e0b77e5b/experiments/exp139/RECOVERY-RESULTS.md)
and [credential-free helper controls](https://github.com/amadou-6e/laomedo/blob/9d3a297c26f560b344e8affaf5a9bf25e0b77e5b/experiments/exp139/HELPER-CONTROL.json).
Executed source is `fc44d7edfb77519b4f4c0d8ef589606d424a232f`, manifest SHA-256
`3554dad38921b21a1c695faa80897baf200adcf5bf4790e959f8cd2813a068d0`.
The later evidence-writing source is distinct. The original checkpoint below
and its negative observation remain historical evidence, not reset results.

| Observable gate | Actual recovery result | Limit |
| --- | --- | --- |
| Git metadata and native setup | Exact full inline permission table starts; dummy-auth control denies auth reads and permits Git metadata writes | Preserves original rules plus only owner-approved `.git` write; not an audit of every real login access route |
| Agent precheck correction | Fresh success task rejects missing report, accepts correction within the same request, then accepts its honest final failure form | Three precheck calls, one model turn; no continuation retry |
| Intended success task | Exact report, 13 closed native items and verified cleanup; Git push exits 128 because `remote-laomedo` is not discovered | Contract accepts failure form and routes to failure; no provider write or draft PR |
| Deliberate agent failure | One real turn, four closed items, ordinary non-mediated supervisor, accepted failure form | Failure route, no GitHub grant or publication |
| Downstream pin rejection | One real turn, four closed items; agent-side precheck accepts original requirements but downstream contract rejects its changed pin | Rejection route, no GitHub grant or publication |
| Budgets and cleanup | Ledger 4/4; zero push/PR provider attempts, all issued GitHub grants revoked; both owned process trees stopped and port 8779 released | Private workspaces, raw traces, consumed identities and histories retained; no extra turn authorized |

A no-turn setup refusal between the original and final activation is preserved
as run `7391913c-318f-4317-8c68-fda10b84769d`: the nested CLI override did not
form a valid profile. Owner and Claude approved the later inline-table correction
before its activation. All three previously consumed digests and the durable
write budget were retained. The report is fixed-scope evidence, not arbitrary
implementation of the source issue.

The live run establishes missing-helper discovery, without an exported live-shell
identity. Login-shell PATH loss is a reproduced mechanism and likely cause.
Credential-free controls reproduce helper discovery in a plain shell and its
loss in a login shell; an explicit Git exec path finds a dummy helper. That is
not a deployed fix or successful mediated push. The temporary host 404 fixture
is reachable outside the sandbox, while the selected network-off sandbox's
`host.docker.internal` request returns `EAI_AGAIN`. This establishes a DNS/hostname
barrier on that route, not denial of every numeric-address route. The live push
stopped at helper discovery before reaching that barrier. Both problems remain
owned by [#139](https://github.com/amadou-6e/laomedo/issues/139); a reviewed
discovery/reachability fix, required configuration approval and a new numeric
model cap must precede another success campaign.

Before final activation, 643 host tests with 11 skips, 12 focused controls and
all three actual frozen-request digest checks passed. Executed-head CI passed
after one rerun of the existing Git maintenance-lock race; the initial failures
are retained. Thirteen focused controls now include a private-content export
regression. An in-memory scan of proposed EXP-139 source/evidence and every
campaign report found no current known selected GitHub, runner or Codex token
values. No credential values or credential hashes were exported. Historical
rotated values and private raw transcripts were not scanned; there is no
published PR to scan. GitHub credentials stayed host-side; accepted local Codex
login custody remains the container profile and sandbox auth denial. No hosted,
multi-user or private-client subscription-eligibility claim is made.

## Imported live workgraph checkpoint, 2026-10-11

[Laomedo #139](https://github.com/amadou-6e/laomedo/issues/139) remains incomplete.
The owner approved the exact bounded deployment, four submitted turns and at
most one push plus one draft PR in the disposable repository. Claude approved
the source before activation. The campaign used pinned Langflow 1.12.3 and
Codex 0.159.2, the existing subscription profile and unchanged permissions.
See the [machine observation](https://github.com/amadou-6e/laomedo/blob/eb42a46d6ccda002d49b18722f008517857d693f/experiments/exp139/OBSERVATION.json)
and [result](https://github.com/amadou-6e/laomedo/blob/eb42a46d6ccda002d49b18722f008517857d693f/experiments/exp139/RESULTS.md).

| Observable gate | Actual result | Limit |
| --- | --- | --- |
| Frozen issue, skill and requirements enter imported graph | Actual three request digests matched host bindings; real issue/task multiline escapes required a prospective base64 transport correction | Credential-free transport check; encoding is not encryption |
| Agent precheck and retained execution evidence | One live turn, two bound precheck calls (reject then accept), nine closed native items, exact report bytes and verified snapshot/controller/container cleanup | Evidence closure does not establish task success |
| Failure behavior and conditional route | Git config/index-lock writes were denied; agent honestly returned failure; contract accepted the failure form and graph selected failure | Success publication did not run |
| No-grant deliberate failure case | Mediated supervisor refused before a turn with `mediated_lease_request_invalid`; runner reports `lease_service_unavailable`, graph selects rejection | Intended real-agent failure case remains unexecuted |
| Publication budget and cleanup | Ledger 1/4; zero push/PR attempts; first run grant revoked; both new process trees stopped and port released | Refused launch lease cleanup was unverified, although runner cleanup is recorded verified; retain that distinction |

The preceding host head passed 638 tests with 11 skips. The transport correction
passed three pinned imported-graph tests with multiline/non-ASCII round-trip and
four negative outcome variants. Seven host binding/budget controls passed.
The actual source checkout was checked clean at its baseline before activation.
The exact report digest matched; no commit, push or draft PR was created.

Recovery is a proposal, not an applied configuration: explicit Git-metadata
write permission and an ordinary non-mediated supervisor for no-GitHub-grant
cases. A credential-free sandbox control reproduced the original denial and
showed the exact proposed Git rule permits config/index-lock writes while still
denying a dummy auth-file canary. No production isolation or authorization claim
is made. Live success publication and downstream pin rejection remain unverified;
the original negative outcomes and ledger must be preserved. Raw traces stay
private. The GitHub credential remained host-side; the accepted local Codex
profile still relies on the sandbox auth-file denial. The historical preparation
record below predates this live campaign and does not describe current usage.
The proposed evidence/report scan found no known selected GitHub, runner or
current stored Codex credential values; historical rotated values and private
raw traces were not covered. Claude approved this negative evidence checkpoint,
not live completion. Before any recovery activation it requires a host-side
Git-config execution audit and hostile-config control, host-only supervisor
selection, and preserved consumed identities. The observed rejection-before-
recovery routing priority also remains a #139 design gap.

## Native execution closure preparation, 2026-10-11

[Specs #348](https://github.com/amadou-6e/specs/issues/348) and
[Laomedo #139](https://github.com/amadou-6e/laomedo/issues/139) add host-side
native trace closure to the trusted publication path. Nine credential-free
controls cover exact terminals, open command/noncommand tools, malformed or
truncated raw data, wrong thread/answer, duplicate or late identities, reader,
snapshot and cleanup uncertainty, old resume bytes and a persisted runner record.
The runner test substitutes the native transport and independent lease/cleanup;
it does not establish live native schema compatibility or Docker removal.
The full development suite passed 630 tests with 11 skips at implementation
[`95cc09c`](https://github.com/amadou-6e/laomedo/commit/95cc09cf2a92ba9604bce8b4a2b2168369d01627).
Claude's independent review required refusing resumed cumulative publication
without a durable per-attempt closure history. The focused fix at
[`b4630df`](https://github.com/amadou-6e/laomedo/commit/b4630df26b89f64df711a0a3ee8c2eaf83c1ca39)
passes ten focused controls, including the actual start/resume route, and Claude's
focused recheck approved it. Both Python 3.10/3.13 installed-wheel CI jobs pass.
A local 631-test rerun encountered a Windows connection reset in the publication
HTTP test; the unchanged 23-test publication suite passed when rerun. The earlier
CI maintenance-lock race was absent on the reviewed final head. Neither recovered
test failure is counted as live acceptance. The prospective protocol was frozen at
[`9fd1a69`](https://github.com/amadou-6e/laomedo/commit/9fd1a69).

No model turn, real credential, live GitHub request or running configuration
change was used for this preparation. The prospective EXP-139 protocol is
committed before any live call, with authorization and manifest gates. The
owner subsequently approved four submitted turns and one draft PR in the
named disposable repository using the existing host-side credential reference;
none has been consumed. Deployed wiring, protocol/source review and explicit
configuration approval precede the live run. Earlier negative findings remain
historical and are not relabelled by these fixture controls.

## Trusted publication handoff checkpoint, 2026-10-10

[Laomedo #138](https://github.com/amadou-6e/laomedo/issues/138) implements the
[trusted handoff design](design/trusted-publication-handoff.md) as opt-in host
composition. At [3742913](https://github.com/amadou-6e/laomedo/commit/3742913),
609 host tests pass with 11 skips under cached pinned project dependencies,
and five publisher-node tests pass inside pinned Langflow/LFX 1.12.3 with
network disabled and source mounted read-only. The final guard amendment at
[840dfac](https://github.com/amadou-6e/laomedo/commit/840dfac) passes 39 focused
handoff/lease tests; the node source is unchanged. The initial raw Python run
lacked PyJWT and could not load the full suite; `uv` with the project's pinned
dependencies resolved that environment failure.

The tests establish draft-only fake-provider publication after host contract
acceptance; exact readback; refusal of task failure, contract rejection,
interruption, unknown completeness and requirements mismatch; old agent-bearer
denial during validation; unconfirmed/foreign artifact refusal; no automatic
resend; durable intent before dispatch; bounded renewals; cancellation and
expiry races; provider-connection removal; explicit startup recovery; and
authenticated empty-body host API admission. The lease-service test uses a
real service object with synthetic heartbeat loss and a fake Docker cleanup:
it revokes the same handoff grant before cleanup while another run remains
usable. It is not a whole-process-tree kill or real GitHub revocation probe.

On 2026-10-11, independent Claude review approved implementation `840dfac`
and the design, subject to updating this record. Its two nonblocking publication
findings were fixed together at [75db8fe](https://github.com/amadou-6e/laomedo/commit/75db8fe):
mediation exceptions consult the durable effect state before distinguishing
failed from unknown, and early/concurrent publish requests cannot end the lease
or interrupt the first provider call. All 41 focused handoff/lease tests pass,
including four journal-state controls and concurrent authenticated HTTP POSTs.
Claude approved that incremental logic diff, conditional on the full suite and
final-head CI. The full host suite at `75db8fe` subsequently passed 613 tests
with 11 skips and exit zero. It did not independently run tests; the initial review read code
and specs, and the incremental review read the changed logic and regression tests.
The earlier quota-only request produced no verdict and was explicitly resolved
before these reviews in the same bound session.

No configuration, real credential, model turn or GitHub acceptance write was
used. This checkpoint is credential-free host composition, not live #139
acceptance. The real runner's unknown completeness, native provider
acceptance, host deployment wiring and #139 cap/scoped identity
remain required before live publication.
The bounded #100/#104 gates are now recorded as completed; #100's live-provider
evidence is merged through [specs #344](https://github.com/amadou-6e/specs/pull/344).

## Imported skill-agent-contract demonstration, 2026-10-10

The credential-free [Laomedo #137 implementation](https://github.com/amadou-6e/laomedo/pull/142) composes the production Skill Reference, Codex Agent and Output Contract nodes with fixture issue ingestion and explicit conditional routes. It deserializes the committed export with pinned `Graph.from_payload(...).arun()`, not a manually reproduced router. This is Graph-engine import/execution, not a live REST/UI server-import claim.

The final [protocol amendment](https://github.com/amadou-6e/laomedo/commit/33ffa62) froze handwritten expectations before source/export [c594e47b8dff75707ac845d2e28e6851465dd114](https://github.com/amadou-6e/laomedo/commit/c594e47b8dff75707ac845d2e28e6851465dd114), then [machine-written evidence](https://github.com/amadou-6e/laomedo/blob/084e934/examples/langflow-workgraph-demo/evidence.json) recorded all six cases. The coordinator independently verified ten artifact hashes against those committed bytes and the evidence SHA-256 `c9abe4976e661ca4e3c20df051433f66d84a0db3768e305ea011f98d08ad2056`. Earlier captures remain in Git history, not silently relabelled.

| Fixture | Observed contract / destination | Publication |
| --- | --- | --- |
| Valid success | Accepted / success | Explicitly simulated |
| Valid task failure | Accepted / failure | None |
| Invalid form | Rejected / rejection | None |
| Same-request scripted precheck correction | Accepted / success | Explicitly simulated |
| Exhausted scripted continuation | Rejected / rejection | None |
| Valid form on interrupted executor | Accepted / recovery, apparent task success clamped to unknown | None |

At [084e934](https://github.com/amadou-6e/laomedo/commit/084e934), 57 combined pinned Langflow tests pass: 41 Codex, 6 Output Contract and 10 demo tests. Controls show changed downstream requirements reject and false evidence routes recovery. Router logic also sends any non-true completeness value to recovery, but an unknown-value fixture was not run. Every case has one fake-runner HTTP dispatch and retained run/invocation/trace metadata. The image is Langflow/LFX 1.12.3, `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`.

Correction counts are labelled `scripted_continuations`; they do not prove native turn scheduling or enforce a model ledger. Real precheck verdicts use the shared evaluator; synthetic native transport/ledger checks belong to the [agent-execution validation](../agent-execution/validation.md#output-contract-and-routable-codex-outcomes-2026-10-10). Issue ingestion uses an injected fixture transport and never reads ambient host `gh` credentials. No real account, model turn, physical interruption-preservation proof or GitHub write is supplied by this fixture.

Live [#139](https://github.com/amadou-6e/laomedo/issues/139) remains blocked by unreported real-run evidence completeness, native provider acceptance, [#138](https://github.com/amadou-6e/laomedo/issues/138) trusted publication handoff, the remaining [#100](https://github.com/amadou-6e/laomedo/issues/100) gate, and #139's separate model-turn cap and disposable identity. [#104](https://github.com/amadou-6e/laomedo/issues/104) has recorded bounded acceptance; that result does not lift the other live gates. The fixture does not lift those gates or activate a live flow.



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
