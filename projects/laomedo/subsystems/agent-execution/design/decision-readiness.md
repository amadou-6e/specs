---
title: Agent execution decision readiness
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution decision readiness

This is a triage of decisions, research and experiments needed before implementing
the agent-execution boundary, **not** an accepted permission policy or a claim that
the pilot satisfies it. It covers the provider adapters, stage container, checkout,
session, preflight and IF-04/05/06/08/10 exchanges. The Langflow runtime owns
graph sequencing; Laomedo's Langflow integration owns its durable run record.
A crash of the fate-shared Langflow/Laomedo backend ends that run.
The backend must still account for any independently surviving, writable container.

## Evidence and notation

The research baseline was specs `docs/167` at
[`3974d9a`](https://github.com/amadou-6e/specs/commit/3974d9aa1f380c72105e7f205f16e3eeae2c8d80),
inspected 2026-10-02: [interfaces](../contract/interfaces.md),
[isolation](../contract/isolation.md), [Codex](../contract/codex.md),
[Claude](../contract/claude.md), [exchange sketches](../contract/schemas/README.md),
and the [2026-10-01 pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md).
The later decision clarification is now part of the merged
[decision record](../../../decisions/0002-subsystem-handoffs.md). Current
[IF-05/06/08/10 sketches](../contract/schemas/README.md) also incorporate
several #168 review fixes. The older baseline remains evidence of what this
triage inspected, not a competing current contract. Rows below that say
"specify" a shape already present in the sketches mean **verify and refine**
it; they do not reopen the settled first-slice rule or claim runtime proof.
The [#175 issue](https://github.com/amadou-6e/specs/issues/175) and its
[writable-checkout](https://github.com/amadou-6e/specs/issues/175#issuecomment-5950569517),
[network/Actions](https://github.com/amadou-6e/specs/issues/175#issuecomment-5950620596),
and [setup-preflight](https://github.com/amadou-6e/specs/issues/175#issuecomment-5950727562)
clarifications were accessed by the coordinating agent on 2026-10-02. Direct
user clarification defers the reduced-Docker-protection policy until an
experiment and automatic mid-turn container recovery from the first slice.
The latter is now recorded as [D17](../../../decisions/0002-subsystem-handoffs.md#execution-recovery-and-inspection).

`A` = ready to specify from a confirmed choice; `B` = product choice still
needed; `R` = research/owner handoff; `E` = bounded experiment needed;
`D` = defer outside the first slice. Evidence tags are `[C]` confirmed user
choice, `[O]` observed in a bounded pilot, `[I]` inference, `[U]` unverified.
A row has **one** triage class; dependencies and a later decision are named
without pretending the experiment has settled them. `[C]` is not proof that a
provider or Docker can implement the choice. No `[U]` or contested claim is
treated as accepted behavior.

## Question ledger

| ID | Question / exchange | Class, evidence | Dependency and next action |
| --- | --- | --- | --- |
| Q01 | Who stops an orphan with a writable checkout and push credential when the fate-shared backend dies? | A [C] | User selected an independent stage lease supervisor plus backend startup sweep, with a 60-second bound. [EXP-07](../../../experiments/orphan-lease/iterations/2026-10-02/results.md) tested the synthetic mechanism; real push credential integration remains unverified. |
| Q02 | Does the chosen orphan mechanism actually stop the container and revoke access within its bound? | E [O] | EXP-07 passed for a disposable HTTP grant and synthetic worker. Recheck the effective boundary for the production stage and credential path before live writable dispatch. |
| Q03 | Is the request/invocation identity committed before agent dispatch? | A [C] | The merged decision record requires durable identity and refusal if it cannot be established; verify the [IF-05 reservation](../contract/schemas/if-05-stage-invocation.md) experimentally. This does not imply run recovery. |
| Q04 | Which native ID and event prefixes survive kills at each persistence boundary? | E [U] | E02; do not claim mid-turn recovery from the restart-only pilot. |
| Q05 | How long is a writable checkout retained after a terminal run? | B [I] | Product tradeoff inferred from writable checkout and container cleanup; decide retention vs verified snapshot/deletion with [results ownership](../../results-artifacts/contract/interfaces.md). |
| Q06 | Can another stage's native session be reused safely? | D [C] | D13 target; omit cross-stage reuse from first slice until binding and profile isolation are proved. |
| Q07 | Are GitHub writes mediated and journaled, or can the agent use raw `gh`/git? | B [I] | Decide effect identity/PR ownership before claiming deduplicated create/update after uncertainty. |
| Q08 | Can a crashed provider container resume the *same in-progress turn*? | D [U] | D17 remains a later target. First slice reports `failed` and partial evidence; later E08 needs a fresh model budget. |
| Q09 | Does a retry get a new run or invocation identity? | D [I] | Reconcile older Codex retry wording with same-invocation D17 before implementing later recovery; first slice has no automatic mid-turn retry. |
| Q10 | Where do multiple user-added files travel in IF-05? | A [I] | The merged [IF-05 sketch](../contract/schemas/if-05-stage-invocation.md) now has `user_file_refs` separate from `input_ref` and upstream refs. Verify resolution and hash failure before dispatch; exact ordering remains open. |
| Q11 | Who enforces per-invocation timeout? | A [I] | Proposed ownership: agent execution enforces and reports its limit; numeric default is S02, and Langflow owns run-level sequencing. |
| Q12 | Does IF-06 `partial` mean a terminal outcome or only evidence completeness? | A [I] | Define one terminal status plus separate output/trace completeness; distinguish `interrupted` from partial output. |
| Q13 | What stable source identity can agent execution supply for IF-08 replay? | B [U] | [Run traces #179](https://github.com/amadou-6e/specs/issues/179) owns the dedup policy; this producer chooses a stable key capability or explicitly reports absence, then E03. Receipt sequence alone is insufficient. |
| Q14 | What if the provider supplies no native event ID? | A [I] | Preserve source identity as absent/unknown, not fabricated; R01 checks provider APIs. |
| Q15 | How does an IF-10 partial manifest get superseded by a later one? | A [I] | The merged [IF-10 sketch](../contract/schemas/if-10-output-manifest.md) has identity, revision and supersedes fields. Verify producer persistence and consumer replacement with [results](../../results-artifacts/contract/interfaces.md). |
| Q16 | Which side-effect identity fields accompany a PR create/update? | B [U] | Resolve with Q07 and results owner; `target_pr` alone is not a write journal. |
| Q17 | Is the first-slice stage checkout writable? | A [C] | Yes: isolated checkout, commit/push/PR path. Protect skill tree, runner store and host paths separately; old read-only text is superseded for this mode. |
| Q18 | Are protected roots, symlinks and shared-home mounts actually contained when stage writes are allowed? | E [U] | E05 before accepting the Docker boundary. A Docker grant alone is not proof. |
| Q19 | Can parallel stages write the same local mount? | D [C] | Local mounts are outside first slice; later decide exclusion/locking and collision semantics. |
| Q20 | Can two stages share a native session or external home? | D [C] | D12/D13 target, not first-slice support; later validate ownership and secrets. |
| Q21 | How does a follow-up run resume after its old container is deleted and PR branch moves? | D [U] | Existing-session follow-up needs snapshot/branch compatibility; first slice uses a fresh session. |
| Q22 | Who brokers approvals used by both run agents and the chat assistant? | B [I] | Choose shared broker vs execution-local adapter and link chat owner; do not infer from a prompt. |
| Q24 | Who stores bytes passed between separate stage containers? | D [I] | Propose results/artifacts owns durable bytes and execution materializes checked refs; confirm with Langflow/results owners before multi-stage files. |
| Q25 | Who performs orphan reaping: stage supervisor or backend restart sweep? | A [C] | User selected independent supervisor for outage-time revoke/stop and backend startup sweep for persisted state reconciliation. EXP-07 observed both in a synthetic harness. |
| Q26 | Which direction is IF-04? | A [I] | Execution requests exact bytes; registry responds. This is a reading of the draft interface, not a runtime observation; keep provider/consumer labels consistent across map and schema. |
| Q27 | Does the per-run/stage network toggle cover required model/GitHub lanes or only extra egress, and is its default on or off? | B [U] | The existence of the toggle and Actions read are confirmed in #175; scope/default are not. Choose both before dispatch and test effective lanes in a separately designed network check. |
| Q28 | Does execution spool IF-08 until acknowledged ingest, or own a single external raw file? | B [I] | [Run traces #179](https://github.com/amadou-6e/specs/issues/179) T03 owns the canonical-writer decision; this producer must implement its side and never create a second canonical log. |
| S01 | What sensible nonzero default turn cap replaces pilot 4/4 exhaustion? | B [O] | Choose after budget/user-experience review; preflight flags a cap that blocks the intended task. |
| S02 | What invocation timeout default permits long coding/CI work? | B [I] | Product tradeoff inferred from long coding/CI work; choose with resource budget, approval wait and CI-wait rules. The 600-second figure is a shared-contract example, not an observed pilot limit. |
| S03 | What Codex/Claude sandbox and approval prompts are nested inside the container? | R [U] | R01 verify pinned provider modes and request path; E05 tests effective restrictions. |
| S04 | May execution continue when a requested Docker restriction is unavailable? | E [U] | **Policy deferred by direct user clarification on 2026-10-02, after [#175's earlier setup proposal](https://github.com/amadou-6e/specs/issues/175#issuecomment-5950727562).** Agent execution owns E05 design before first-slice preflight; no calendar deadline was selected. Until then, unsupported protection blocks dispatch rather than silently reducing it. |
| S05 | Are home, temporary and cache locations writable without exposing personal profiles? | A [C] | Provide private writable paths, preflight path/capability; E05 verifies actual mounts. |
| S06 | Can bundled skill scripts run in the writable stage? | A [C] | Allow subject to explicit grant and bounded paths unless user disables; test execution and provenance, not arbitrary host writes. |
| S07 | Are git identity, push auth, signing and hooks usable inside the container? | R [U] | R02 inspect selected host/repo configuration; preflight each requested operation, never copy personal credentials implicitly. |
| S08 | Where must materialized skill files live to be discoverable without polluting git? | B [U] | Choose after R01 provider discovery and E04 git/hash check. |
| S09 | How are tests requiring secrets handled? | B [U] | Choose explicit per-run injection/denial; never silently inherit host secrets. |
| S10 | How are Docker-dependent tests run in the stage? | B [U] | Choose sidecar/socket/unsupported after threat review; no implicit host Docker socket. |
| S11 | Which toolchains, dependencies and GPU are preinstalled or requested? | B [U] | Choose image/capability model; preflight declares missing requirements rather than inventing availability. |
| S12 | Can waiting for GitHub Actions complete without exhausting turns or time? | E [U] | E07 synthetic polling; separate later completion/resume policy if invocation ends. Actions *read* is first-slice input; dispatch/re-run is excluded. |
| S13 | Do Windows CRLF changes preserve source/effective/post-run hash meaning? | E [U] | E04 with pinned checkout and bytes; do not equate textual equality with byte identity. |
| S14 | When is workflow-file push permission available? | B [U] | Decide explicit opt-in vs unsupported; R03 verifies GitHub token scope and error classification. |
| S15 | What if approval escalation gets no answer? | A [C] | Finite TTL, denial/failure and trace; no indefinite unattended block. Numeric TTL remains open. |
| S16 | How is uncommitted work preserved when the cap/timeout stops the agent? | B [U] | Choose snapshot/branch retention and visibility; do not label unsaved work published. |

For every setup item, preflight must expose the effective choice rather than
silently supplying an assumed default. This is the proposed **default / override /
observable check** inventory; “unset” is not a product default.

| Item | Default and override status | Observable preflight check |
| --- | --- | --- |
| S01 turn cap | No numeric default selected; explicit user cap may override the eventual default. | Show requested/effective cap, reject zero or invalid cap, warn when a known task cannot fit it. |
| S02 timeout | No numeric default selected; user timeout may override within an eventual hard ceiling. | Show effective deadline and whether expected approval/CI waits could exhaust it. |
| S03 nested prompts | No provider-mode default established; user grant cannot bypass unsupported provider protection. | Report provider/version, requested/effective sandbox and approval mode or unknown. |
| S04 Docker reduction | **Decision and experiment design deferred**; no warn-and-proceed override exists yet. | Report exact unsupported protection as `block` until an explicit reviewed policy says otherwise. |
| S05 writable home/temp/cache | Private writable paths are required; path override only inside approved isolated roots. | Probe write, ownership and mount resolution without reading personal profile data. |
| S06 skill scripts | Enabled only within the explicit grant unless user disables; no host-path override. | Report script executable, grant and designated scratch write path. |
| S07 git identity/push/signing/hooks | No ambient host credential default; user-selected credential/config source needs R02. | Dry-check identity, branch permission and configured signing/hooks without publishing. |
| S08 skill location | No default selected; path override must remain provider-discoverable and protected. | Report materialized exact revision/path/hash and git cleanliness. |
| S09 test secrets | No injection default selected; require explicit scoped grant if supported. | Report secret requirement as known/unknown and whether a scoped secret is available, never its value. |
| S10 Docker tests | No socket/sidecar default selected; per-run request cannot silently mount host socket. | Detect requested Docker capability and effective safe service or unsupported result. |
| S11 toolchains/GPU | No image/hardware default selected; user may request supported image/resources. | Report requested/effective versions, binaries and device access. |
| S12 CI wait | Actions read is in scope; no wait duration or polling default selected. | Show Actions access, polling/wall-time allowance and turn use; avoid hidden long waits. |
| S13 CRLF/hash | Byte hashing remains required; no text-normalizing override established. | Compare source/effective/post bytes and disclose line-ending transformation. |
| S14 workflow push | No permission default selected; explicit opt-in is a B option, not assumed. | Report token permission for workflow-file edit without exposing token. |
| S15 unattended approval | Finite expiry and deny/fail are required; numeric TTL/override not selected. | Show policy, expiry and terminal result of unanswered request. |
| S16 work at cap | No retention default selected; user choice depends on Q05. | Inventory uncommitted diff/snapshot and distinguish local/saved/published states. |

Each first-slice preflight check reports `ok | warn | block` with check ID,
requested/effective setting, reason, user remedy and evidence ref. Run it before
dispatch and retain the result. `block` means the requested operation cannot
proceed under the chosen grant or verified protection; a warning is **not**
permission to weaken an isolation boundary. Detection may itself be unknown;
preflight cannot promise to infer every repository secret, toolchain or CI need.
This shape follows the [#175 setup clarification](https://github.com/amadou-6e/specs/issues/175#issuecomment-5950727562);
its actual checks require R/E evidence.

## Choices to take to the user, in dependency order

| B | Options and trade-off | Prerequisite |
| --- | --- | --- |
| Q01 | **Selected:** independent lease supervisor plus startup sweep, with a 60-second maximum exposure window. Integrate the mechanism with real stage grants before live writable dispatch. | EXP-07 synthetic result and Q25. |
| Q25 | **Selected:** independent supervisor revokes/stops during outage; backend restart sweep reconciles durable state. | Q01 and EXP-07 synthetic result. |
| Q07 | Mediate and journal GitHub writes (audit/deduplication, more integration) or allow raw agent `git`/`gh` (flexible, effect identity uncertain). | First-slice PR safety, Q16. |
| Q16 | Require a stable idempotency/effect key at a mediated write boundary or record only observed PR ref under raw CLI mode; the latter cannot promise exactly-once creation. | Q07 and results owner. |
| Q13 | Producer supplies a durable source key if supported, or exposes key absence; [run traces #179](https://github.com/amadou-6e/specs/issues/179) chooses at-least-once/dedup projection. This is not a second trace-policy decision. | R01 and E03. |
| Q28 | If traces owns canonical ingest, execution spools until acknowledged handoff; if execution owns the one external raw file, traces indexes it. | #179 T03 chooses the owner; this is a producer-side dependency, not a second vote on policy. |
| Q05 | Retain checkout until review (easy continuation, longer credential/file exposure) or snapshot and delete (lower exposure, restore complexity). | Results/artifacts owner, S16. |
| S16 | Retain dirty checkout, snapshot uncommitted files, or let them be lost with explicit warning; choose before claiming preservation at cap. | Q05 and results/artifacts owner. |
| Q22 | Shared approval broker for chat and run agents, or execution-local broker plus compatible chat adapter. | S15 and user interaction owner. |
| S01 | Choose a nonzero capped default with user override (predictable cost, may cut work) or no default cap within a hard run budget (longer unattended work). No number is inferred from the four-turn pilot. | Run-level budget owner. |
| S02 | Choose finite default timeout with explicit longer override (bounded resources, may interrupt CI waits) or stage-class-specific defaults (more configuration). | Q11 and E07. |
| S08 | Provider-discoverable ignored path in checkout vs private mounted path outside repo; compare native discovery, hashes and git cleanliness. | R01 and E04. |
| S09 | No secret-dependent tests (safe but lower coverage) or explicit scoped injection (better coverage, credential handling cost). | R02 and grant review. |
| S10 | Unsupported Docker tests, isolated sidecar (more setup) or host socket (high host-control exposure; not implicit). | Docker threat review. |
| S11 | Prebuilt image/toolchains (repeatable, image maintenance) or per-run requested build/resources (flexible, slower and less reproducible). | Image/resource owner. |
| S14 | Workflow-file push unsupported (least privilege) or separate explicit opt-in (more capability and token risk). | R03. |
| Q27 | Cover only extra egress while model/approved GitHub lanes remain, or all egress (off makes required operations impossible); choose default on/off separately. | [#175 network clarification](https://github.com/amadou-6e/specs/issues/175#issuecomment-5950620596); network test design still open. |
| Docker degradation after S04 | After E05, decide fail-closed or a narrowly defined user override with exact exposed paths/credentials. **No choice is made here.** | E05 and explicit security review; first-slice gate. |

## Research handoffs

| ID | Owner / bounded question | Required return, not assumed finding |
| --- | --- | --- |
| R01 | Codex/Claude adapter maintainers | At pinned CLI/SDK versions, native skill search, sandbox/approval prompts, event IDs, session binding and no-ID behavior; cite APIs and tested traces. Claude's earlier `CLINotFoundError` preceded a model call. |
| R02 | Execution/credential owner with [#129](https://github.com/amadou-6e/specs/issues/129) | Required git identity, signing/hooks and push credential placement for isolated checkout; identify any personal path exposure. |
| R03 | GitHub integration/credential owner with #129 | Minimal Actions/checks/job-log read, content/PR write and workflow-file permission; separate workflow dispatch/re-run, which is not first slice. |
| R04 (Q24, deferred) | Langflow/results owners | For later multi-stage files, identify byte-storage owner and checked-ref materialization; this does not make Q24 first-slice work. |

Each handoff should return inspected source/version, tested command or API,
negative result, and exact first-slice effect. “Not inspected” is not “absent.”

## Experiments

The EXP-07 synthetic orphan/lease experiment was executed with zero model turns;
the other experiments below remain proposals. Use synthetic local tasks with
**zero model turns** where possible; the 2026-10-01 pilot spent its recorded
4/4 turns. Pin specs and
implementation SHA, Langflow 1.12.3, Codex CLI 0.159.2 where used, Docker
Desktop/Windows build and permission grant before execution. Record exact
commands, timestamps, mounts and cleanup. No raw credential or transcript goes
into this repo.

| ID | Hypothesis and falsifier | Minimal procedure / observable outcome | Cost |
| --- | --- | --- | --- |
| E01 | Chosen lease/reaper bounds orphan lifetime; falsified if container retains push-capable access beyond bound. | [EXP-07 synthetic result](../../../experiments/orphan-lease/iterations/2026-10-02/results.md) passed its 60-second bound for a disposable HTTP grant and worker. Real push-capable access and production launch integration remain untested. | Local Docker, no model. |
| E02 | Pre-dispatch identity and native ID/event flush survive each crash phase; falsified by missing/duplicated identities or falsely complete trace. | Inject kills before reserve, after reserve, after native-ID receipt and after event flush; restart, inspect persisted state without resuming the terminal run. | Local harness, no model for synthetic provider; real provider later. |
| E03 | IF-08 chosen key handles delivery replay; falsified by an unmarked duplicate or silently lost event. | Replay/reorder same synthetic event with and without source ID through trace ingest; compare raw record, projection and completeness. | Local harness, no model. |
| E04 | Selected skill path stays discoverable, ignored and hash-stable; falsified by missing native discovery, dirty git tree or unexpected byte change. | [EXP-08 revised synthetic result](../../../experiments/pinned-skill-materialization/iterations/2026-10-03/results.md) confirms exact bytes and demonstrates that an unprotected actual Git clone becomes dirty/stageable/cleanable. A local exclude rule protects ordinary Git operations in a second clone, but production installation, force-clean safety and native Codex discovery remain unverified. | Disposable Git clones; zero model turns so far. |
| E05 (design deferred) | Can reduced Docker protection coexist with a writable, push-capable stage without exposing protected host/runner/skill paths or credentials? An unauthorized access would falsify that possibility. | **Agent execution owns the next protocol draft before first-slice preflight; no calendar date was authorized.** First decide which Docker protection failure, protected assets, disposable canaries, test credential and safe-stop rule to use; only then specify procedure and outcome threshold. Do not use real personal credentials or dispatch a degraded stage meanwhile. | Local Docker may suffice without model calls; exact cost awaits protocol design and safety review. |
| E06 | Approval expiry and Stop cannot cause an unapproved resumed invocation; falsified by side effect after denial/expiry/terminal state. | Synthetic paused tool request; expire/deny while UI closed, race Stop with response, inspect state and effects. | Local harness, no model. |
| E07 | Actions polling can be bounded without spending agent turns or silently exceeding timeout; falsified by hanging invocation or unseen CI failure. | Stub Actions status/log API and delayed completion, compare wall time, turn counter, timeout and trace. | Stub network, no model. |
| E08 (later) | A real provider can safely resume after an interrupted mid-turn container crash. | Only after D17 is reopened: bounded Codex/Claude run, kill mid-turn, compare native session and side-effect identities. Do not infer from clean restart. | New model budget and provider access required. |

## Review finding coverage

This maps findings from [PR #168](https://github.com/amadou-6e/specs/pull/168)
at `3974d9a` and [PR #172](https://github.com/amadou-6e/specs/pull/172)
at `25aca35` to this triage or their other canonical owner. A row assigned
elsewhere is **not** silently fixed by this document. Earlier
[PR #166](https://github.com/amadou-6e/specs/pull/166) review scenarios are
retained as hypotheses, not accepted observed failures. Its disapproving verdict
was **not** retracted; an earlier review on #168 was the one retracted.

| Finding | Coverage or owner, with reason |
| --- | --- |
| #168 B2, IF-08 replay/deduplication | Q13/Q14/Q28, E03. Optional native keys plus receipt sequence cannot guarantee deduplication; canonical policy belongs to #179. |
| #168 M1, IF-05 user files | Q10. Explicit `user_file_refs` are now in the merged sketch; pre-dispatch byte/hash behavior remains untested. |
| #168 M2, retry identities versus D17 | Q08/Q09 and E08 later. No first-slice automatic mid-turn retry. |
| #168 minor IF-04 direction | Q26, with [skill registry](../../skill-registry/contract/interfaces.md) as byte provider. |
| #168 minor IF-06 `interrupted`/`partial` | Q12; terminal state and evidence completeness are different concerns. |
| #168 minor IF-10 supersession | Q15; the merged schema records revisions, while results/artifacts still owns interpretation and tests. |
| #168 B1, IF-01 trigger context | [Issue integration](../../issue-integration/contract/interfaces.md), not an agent-execution input shape until Langflow supplies a frozen invocation. |
| #172 H1, durable reattach claim | Fate-shared crash decision supersedes reattach; residual orphan safety is Q01/Q25/E01 and pre-dispatch evidence Q03/E02. |
| #172 H3, approval requests/expiry | Q22, S15 and E06. Shared broker owner remains B. |
| #172 H4, parallel local mounts | Q19 deferred; first slice uses isolated checkout, so locking local mounts is not specified here. |
| #172 H5, cross-stage session reuse | Q06/Q20 deferred; private binding must be proved before support. |
| #172 H6, inter-stage files | Q24/R04 deferred; durable byte owner is cross-subsystem, execution only materializes checked refs. |
| #172 H7, follow-up after container/branch move | Q21 deferred; [Langflow follow-up](../../langflow-integration/contract/interfaces.md) chooses new/existing session, but compatibility is not proved. |
| #172 H9, Stop/dispatch race | E06 tests local rejection of late approval/effects; [Langflow integration](../../langflow-integration/contract/interfaces.md) owns graph dispatch after Stop. |
| #172 H11, all components bypass approvals/trace | [Langflow component boundary](../../langflow-integration/contract/interfaces.md) owns non-agent nodes. This agent-execution triage applies only when a stage reaches IF-05. |
| #172 H12, duplicate PR creation | Q07/Q16; agent prompt to inspect existing PR is insufficient idempotency. |
| #172 H13, multiple stages claiming PR | [Langflow integration](../../langflow-integration/contract/interfaces.md) must choose graph-level PR owner; Q07/Q16 covers only this execution boundary's side effects. |
| #172 H14, review-comment context | [Issue integration](../../issue-integration/contract/interfaces.md) and [results/follow-up](../../results-artifacts/contract/interfaces.md) own context; execution consumes the frozen IF-05 input. |
| #172 H15, failure report without agent | [Results and artifacts](../../results-artifacts/contract/interfaces.md) owns assembly from terminal run/trace refs; not a provider final message requirement. |
| #172 H16, no run-level budget | [Langflow integration](../../langflow-integration/contract/interfaces.md) owns run-level budget; Q11/S01/S02 cover only invocation limits and defaults. |
| #172 H2/H8/H10, timer/event, branch/loop, flow snapshot | Langflow/issue integration, not agent execution; this page neither validates their behaviour nor relaxes their gates. |

## Crash-behavior answers for the first slice

1. **What is persisted before dispatch?** The target is run/stage/invocation
   identity, frozen config and grant, resolved workspace/skill refs, and a
   dispatch reservation before starting a container or provider turn (Q03).
   Native session ID and events must be flushed when received, not invented
   later. The actual atomic boundary is unverified (E02); after a crash,
   absence of an ID means *unknown*, not “no agent ran.”
2. **What does restart do: stop, clean up, and mark?** Langflow and Laomedo
   are fate-shared. Restart does not reattach or continue the crashed run.
   It must identify incomplete invocations and mark them `crashed` (or
   `interrupted` with reason `backend_crash`) with partial/unknown evidence,
   consistent with the run's `crashed` state. That vocabulary requires a
   coordinated IF-06 change; it is not an agent failure. Arrange orphan cleanup through the selected
   Q01/Q25 owner. Automatic same-turn D17 recovery is deferred. Synthetic
   EXP-07 observed supervisor cleanup and restart sweep within the selected
   bound; production integration and E02 completeness remain unverified.
3. **Can orphaned containers still write externally?** Yes. EXP-07 observed
   three synthetic writes after backend kill was requested and before the
   independent supervisor revoked the grant. The 60-second synthetic bound
   passed, but a real push-capable credential and production stage may have
   different access paths. Do not call the first slice safe until those paths
   are governed by the selected mechanism and checked by E05.
4. **Can relaunch duplicate side effects, and is that acceptable?** A user
   launch is a *new run*, not recovery. It may duplicate a PR or push if the
   previous agent acted before the crash but its ref was not persisted.
   Exactly-once is **not** accepted or proved by asking the agent to inspect
   GitHub. Q07/Q16 must choose mediation/effect identity or explicitly accept
   uncertainty and disclose it before relaunch.
5. **Is crash detection necessary?** Yes, to mark the fate-shared run terminal,
   prevent new dispatch into a stopped run, revoke/stop a surviving stage, and
   distinguish incomplete evidence from no work. Whether that is a durable
   lease, supervisor heartbeat or restart reconciliation is Q01/Q25 and E01;
   E02/E03 check state/event boundaries. No provider mid-turn recovery is
   promised by this detection.

The first slice cannot be declared decision-ready while the chosen Q01/Q25 mechanism is not integrated with the real writable-stage grant, or while Q07/Q16,
Q13, the network-toggle boundary and the post-E05 Docker policy are unresolved.
Other B items may be scoped out only by explicit first-slice exclusions and
matching preflight behavior; no experimental outcome is asserted here.
