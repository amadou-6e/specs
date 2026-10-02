---
title: Prompt and skill library decision readiness
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Prompt and skill library decision readiness

This is the triage for [specs #177](https://github.com/amadou-6e/specs/issues/177), not an accepted implementation contract. The library owns user-facing prompt and skill selection, prompt revisions, native/GitHub backend choice and publication policy. The [skill registry](../../skill-registry/contract/interfaces.md) owns immutable skill bytes, revision lookup (IF-03), and draft validation/promotion (IF-14); the library **submits** IF-14 proposals and receives receipts. [Langflow integration](../../langflow-integration/contract/interfaces.md) consumes resolved IF-02 selections and owns run-state persistence and dispatch. The [handoff graph](../../../architecture/subsystem-handoffs.md#edge-inventory) calls this H3.

The candidate first slice is a one-node single-agent run from a direct prompt or selected issue, with a fresh isolated checkout, latest/pinned resolution before dispatch, one PR, trace and reviewed failure-to-issue path. A fate-shared Langflow/Laomedo backend crash ends the run as `crashed`; reopening the UI is not a backend crash. Timer/event launches, multi-stage selector discovery, local mounts, cross-stage sessions, existing-session follow-ups and selective reruns remain outside that slice. [D17](../../../architecture/subsystem-decision-record.md#execution-recovery-and-inspection) still describes three automatic **agent-container** recovery attempts, but the user's later clarification deferred that behavior from the first slice. This page does not amend the decision record or implement it.

## Evidence boundary and notation

The research pass inspected the specs source at [`3974d9aa`](https://github.com/amadou-6e/specs/tree/3974d9aa1f380c72105e7f205f16e3eeae2c8d80) on 2026-10-02: this subsystem's existing [interface](../contract/interfaces.md), [Langflow IF-02/IF-09](../../langflow-integration/contract/interfaces.md), [registry IF-03/IF-14](../../skill-registry/contract/interfaces.md), [draft](../../skill-registry/contract/drafts.md) and [revision](../../skill-registry/contract/revisions.md) rules, [agent IF-05](../../agent-execution/contract/schemas/if-05-stage-invocation.md), [shared records](../../../architecture/shared-contracts.md), [decisions](../../../architecture/subsystem-decision-record.md), [handoffs](../../../architecture/subsystem-handoffs.md), [journey](../../../architecture/user-traversal.md), and the [2026-10-01 local pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md). The pilot ran Langflow 1.12.3 and Codex CLI 0.159.2 at Laomedo `5e14c7a`, with its 4/4 model-turn cap exhausted. It proved a narrower frozen whole-skill reference and local execution path, **not** prompt revision storage, GitHub library publication, pre-dispatch durable selection persistence or process-crash behavior. Reviews on [#166](https://github.com/amadou-6e/specs/pull/166), [#168](https://github.com/amadou-6e/specs/pull/168), and [#172](https://github.com/amadou-6e/specs/pull/172) were treated as critique hypotheses, not acceptance evidence. No current vendor documentation, Laomedo PR #5 implementation/tests, private raw traces or new runtime experiment was inspected. Issue-led source selection may miss behavior outside these paths.

Each question has one class: `A` spec-verifiable first-slice behavior, `B` product choice, `R` primary-source research, `E` experiment, or `D` deferred. `[C]` records a user choice, `[O]` a directly inspected document/pilot fact, `[I]` an inference, and `[U]` unverified. These are evidence classes, not claims of implementation. In particular, a draft contract is observed text, not evidence the adapter works. No `A` rests on `[U]` or a contested user choice. The R and E work lists below are follow-ups, not checks already run.

## Question triage

| Question | Class | Basis | Dependency | Next action / owner |
| --- | --- | --- | --- | --- |
| Q01. What exactly identifies a prompt revision? | B | [O] IF-02 leaves serialization open; [I] identity affects reproducibility | B01, R01 if GitHub-backed | Choose content hash, monotonic revision plus hash, or Git SHA/path/blob rule before freezing a prompt ref; library owns prompt identity. |
| Q02. Who calls IF-02 for one node and when? | A | [C] D09; [O] IF-02 and Langflow H3 | None for target behavior; E01 for implementation | Langflow launch setup requests one stage's selection; library returns exact prompt/skill refs before dispatch. Langflow records the frozen selection. |
| Q03. How are selectors discovered across a multi-stage graph? | D | [C] first-slice one-node limit; [O] D03 and H3 | Later graph-authoring contract | Defer traversal, defaults and per-stage resolution; do not imply one-node IF-02 proves graph-wide discovery. |
| Q04. How is an inline direct prompt represented? | A | [O] IF-02 and shared `InputSnapshotRef`; [I] IF-05 mapping gap | None for target distinction | Keep inline content as an input snapshot, not an unpublished library revision; separately carry its exact `content_ref`/hash into IF-05's prompt field. The conversion/schema remains to specify and test with Langflow and agent execution. |
| Q05. What if a requested revision is missing or inaccessible? | A | [O] IF-02 failure rule; [C] D09 freeze | None | Fail visibly before dispatch; never substitute latest, an older version or empty content. This is a target rule, not proof of error handling. |
| Q06. If GitHub is unavailable at launch, may a local copy be used? | B | [O] IF-02 says unavailable fails; [I] a verified cache could change that rule | B02; R01 | Choose fail-closed or only a verified exact-byte cache; do not silently call an unverified copy the selected revision. |
| Q07. Is a GitHub-backed catalog required in the first slice? | B | [C] D06 allows native/GitHub; [O] pilot has no GitHub catalog | B03; Q01/Q06 if GitHub now | Choose native-only, both backends now, or inline-only; keep the eventual GitHub policy separate from first-slice delivery. |
| Q08. How do native/GitHub synchronization, conflicts and visibility work? | D | [O] interface explicitly leaves them open; [I] only needed when both backends participate | B03; then R02 and a product choice | Defer if first slice is native-only; if both are selected now, promote to blocking B/R work. No background sync is assumed. |
| Q09. May an agent publish a skill edit without a user review? | B | [C] D06 PR default/direct-edit opt-in and D20/D22 access intent; [O] IF-14 draft separation | B04; external approval boundary | Choose draft-only human publication, an explicitly auto-approved PR path, or explicitly enabled direct edit; an agent's ordinary run grant is not publication authority. |
| Q10. Does IF-14 submission itself publish a skill revision? | A | [O] registry IF-14 and draft rules | None | No. Library submits proposal and base; registry returns an unpromoted draft receipt. Validation, promotion and GitHub publication are separate. The issue's provider wording does not transfer registry ownership. |
| Q11. Are resolved refs durably retained before agent dispatch? | E | [O] IF-09 target only; [U] actual persistence | E01 here is adopted as E06 by [Langflow integration #174](https://github.com/amadou-6e/specs/issues/174) | Fault-inject before/after dispatch and inspect retained IF-02/IF-09 refs. This is a cross-owner dependency, not a second library experiment. |
| Q12. On a new run after backend crash, use moved `latest` or the previous frozen selection? | B | [C] backend crash ends prior run; [O] D09 covers the prior run only | [Langflow integration #174](https://github.com/amadou-6e/specs/issues/174) B20 owns the choice; B05 here records library implications | Do not label a new run recovery of the old one. |
| Q13. What if GitHub accepts a publication but the backend dies before acknowledgement? | E | [I] remote effects can outlive local acknowledgement; [U] no test | E02, only if GitHub backend selected | Fault-inject a fake publication endpoint and compare local intent, request and remote ledger; report unknown outcomes rather than infer success/failure. |
| Q14. Who owns prompt revision storage? | B | [O] library and registry explicitly leave it open | B06 | Choose shared generic store, separate prompt store, or prompt-as-registry-kind without moving skill-byte authority by implication. |
| Q15. What must be inspectable after a crashed launch? | A | [C] terminal crash rule; [O] IF-02/IF-09 intended refs | E01 tests persistence | Retain selector, resolved identity/hash, provenance, stage/run identity and launch/error state before dispatch so an operator can distinguish unresolved from frozen selection. Actual durable write behavior remains E01. |
| Q16. Can a publication request remain effective after backend death? | E | [I] external call may continue; [U] no fault test | E02 | Test send/accept/ack kill points. A terminal `crashed` run does not roll back remote GitHub effects. |
| Q17. Can relaunch duplicate selection or publication? | B | [I] new run and ambiguous external write | B05 for selection; B07 for publication; E02 | Decide whether relaunch reuses frozen refs and how an unacknowledged publication is reconciled before retry. No exactly-once claim. |
| Q18. Does the library detect a workflow crash? | A | [O] Langflow owns run lifecycle and IF-09; [C] backend-death terminal rule | None | No separate library run-crash detector. Langflow marks `crashed`; library only inspects its own incomplete publication attempts, if it owns that write. |

`A` = 6, `B` = 7, `E` = 3, `D` = 2, `R` = 0 questions (18 total). R01–R03 are bounded source checks needed by B decisions; E01 is a Langflow-owned dependency and E02 is conditional library/GitHub work. No model test is authorized by this triage.

## B choices for product owner

The alternatives are not accepted defaults. Each choice must be recorded in an owning decision/contract before implementation, with the dependency cleared.

| Choice | Alternatives and consequences | Failure mode and cost |
| --- | --- | --- |
| B01 (Q01) prompt identity | Content hash alone makes equal bytes equal but loses edit lineage; sequence plus content hash preserves history but needs atomic counter/lookup; Git commit SHA + path (and verified blob/content hash) ties GitHub history to bytes but cannot serve a native backend without a mapping. | Hash-only cannot explain source provenance; sequence races or mutable Git branch names can select wrong bytes. Storage/index and migration cost differs by backend. |
| B02 (Q06) unreachable GitHub | Fail closed makes availability dependency explicit; or permit a previously resolved, hash-verified exact-byte cache with provenance and explicit staleness semantics. | A cache without proof of exact revision silently changes a run; fail-closed can block valid work during outage. Verification/retention cost for cache. |
| B03 (Q07) first-slice backend | Native-only narrows delivery and defers D06 GitHub verification; native plus GitHub exercises publication but expands auth/sync/crash scope; inline-only avoids a catalog initially but cannot validate versioned library selection. | Calling inline-only a library launch overclaims D09; both-now increases failure modes and test cost. Native-only leaves GitHub needs to a later slice. |
| B04 (Q09) agent publication | Require human review of every draft before PR; allow a scoped auto-approval policy to open a PR while keeping merge separate; or explicitly permit direct branch edit with distinct write authority. | A generic agent grant could publish unauthorized bytes. Human review adds delay; auto-approval needs auditable policy; direct edit can bypass branch review/rollback expectations. |
| B05 (Q12/Q17) crashed-run relaunch selection | [Langflow integration #174](https://github.com/amadou-6e/specs/issues/174) B20 chooses re-resolve, prior exact refs, or explicit user selection. The library must resolve or supply exact refs accordingly. | Fresh resolution changes behavior; automatic reuse may select obsolete content; user choice adds friction. This is a dependency, not a second product vote. |
| B06 (Q14) prompt store | Shared generic revision store can reuse hashing/history but requires type and authority isolation; a separate prompt store keeps boundaries explicit but duplicates revision machinery; prompt-as-registry-kind reuses registry APIs but expands a skill-only contract and changes ownership. | Unclear authority risks mutating a frozen skill or prompt; shared/migrated schemas and separate-store upkeep have material costs. |
| B07 (Q17) ambiguous publication | Reconcile a durable local publication intent against remote GitHub evidence before retry; require user confirmation if remote outcome is uncertain; or permit an explicit duplicate-risk retry. | A blind retry may create duplicate PRs/commits; indefinite reconciliation may block progress. Remote reads, markers and support workflow cost await R03/E02. |

First-slice blockers depend on B01 and B03 if the library is used at launch. B02/B04/B07 block only the chosen GitHub-backed or agent-edit publication route, not a native selection-only slice. B05 belongs to Langflow's new-run contract; B06 is the canonical prompt-store choice here, and [skill registry #178](https://github.com/amadou-6e/specs/issues/178) links it rather than choosing again. The library cannot silently make the skill registry its store. B03 determines whether Q08 remains deferred.

## R source checks

These are **not yet performed**. Return exact owner, document/code version and access date, inspected section, applicability and contradictory evidence; a source read is not a product test.

| Check | Primary source / bounded question | Output and use |
| --- | --- | --- |
| R01 | Official GitHub API documentation for commit/tree/blob addressing, immutable content retrieval, and 404 versus authorization failures for the chosen auth route. | Decide whether B01's Git SHA+path truly resolves exact bytes and B02 can distinguish outage, denied access and missing revision. Conditional on GitHub backend. |
| R02 | Pinned Laomedo [PR #5](https://github.com/amadou-6e/laomedo/pull/5) source and tests: current draft storage, validation receipt and promotion boundary. | Before implementing IF-14, compare actual shapes with registry contract; pilot report alone is insufficient. Defer if first slice only consumes skills. |
| R03 | Official GitHub write, conditional update, branch protection and conflict semantics for the selected PR/direct-edit route. | Bound B04/B07 and publication reconciliation; do not promise idempotency or conflict prevention without evidence. Conditional on GitHub publication. |

## E experiments and crash behavior

Neither experiment has run. The pilot's 4/4 model-turn cap is exhausted; both sketches use synthetic, no-model inputs. Pin setup and logs before execution; do not fault-inject a user's live GitHub repository.

| Experiment | Hypothesis and falsifier | Pinned setup, procedure and outcome | Estimated cost / owner |
| --- | --- | --- | --- |
| E01 pre-dispatch freeze (Q11/Q15) | A selected IF-02 exact ref is durably recorded before agent dispatch; falsified if the agent can start while only a mutable selector survives, or crash leaves no inspectable frozen ref. | Use the [pilot-pinned Langflow 1.12.3 image digest](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md#frozen-runtime-and-permissions) and Laomedo `5e14c7a`; replace the model node with a fake invocation. Inject backend kills immediately before and after frozen-ref persistence and dispatch; compare request, IF-09 record, durable snapshot and terminal `crashed` state. Record the exact harness commit and all kill points. [#174 E06](https://github.com/amadou-6e/specs/pull/188) now receives and owns execution of this handoff. | ~0.5–1 engineering day, under 1 hour execution, zero model turns; **Langflow integration**, cross-owner dependency. |
| E02 interrupted GitHub publication (Q13/Q16/Q17) | A durable local intent exposes an ambiguous remote outcome without blind retry; falsified if local state says failed/succeeded without evidence or resends a write accepted by the fake endpoint. | Only if GitHub backend chosen: pin adapter and fake endpoint commits, a fixed proposed revision/branch and request ledger. Kill at before-send, after-accept and before-ack persistence; restart, inspect local intent, remote ledger, visible unknown state and reconciliation action. R03 precedes any live GitHub test; use disposable repo only with separate authorization. | ~0.5–1 engineering day plus under 1 hour execution, zero model turns/GitHub writes in fake test; **library/publication owner**. |

Five specific crash answers for the first-slice discussion:

1. **Persist before dispatch:** the selected `latest`/pin/inline origin, exact resolved prompt revision/content hash and skill snapshots, provenance, run/stage identity and IF-09 frozen configuration reference must be inspectable. E01 tests whether the proposed ordering actually holds.
2. **On restart:** Langflow/Laomedo marks the old run terminal `crashed`, not resumed. Agent execution owns its orphaned container handling. The library does not own run-state cleanup; if it started a GitHub publication, it must retain an ambiguous local attempt for reconciliation.
3. **Work that may outlive the backend:** an external GitHub write may complete despite client death; whether any agent container remains running requires agent-execution evidence and is not asserted here. A closed UI alone does not end the backend.
4. **Relaunch hazard:** a new linked run can resolve moved `latest` differently and a repeated publication can duplicate an external effect. B05 and B07 are distinct policies; neither is solved by the old run's terminal status.
5. **Detection:** Langflow detects/records run crash. The library detects only its own incomplete publication intent; remote completion requires an acknowledgement or a verified remote read, not a missing local response. E02 establishes what is actually observable.

## Ownership and review coverage

| Boundary or review concern | Disposition |
| --- | --- |
| IF-02/H3 and [#172 review](https://github.com/amadou-6e/specs/pull/172) H10 | Q02/Q03/Q11 separate one-node selection from later graph traversal and test Langflow-owned freeze persistence. The library returns refs; it does not sequence the flow. |
| IF-03/IF-14 and [#166 review](https://github.com/amadou-6e/specs/pull/166) | Q09/Q10/Q14 keep skill bytes and draft promotion with registry. Review concerns about orphaned publication are hypotheses, not proof of current library behavior. |
| GitHub publication and [#172 review](https://github.com/amadou-6e/specs/pull/172) H12 | Q13/Q16/Q17 and E02 handle remote-after-crash uncertainty for library publishing. Agent execution's **run PR** write is a different boundary; this page does not acquire it. |
| [#168 review](https://github.com/amadou-6e/specs/pull/168) M1 | Q04 shows the inline prompt snapshot-to-IF-05 mapping gap, but user-added **files** and upstream artifacts remain agent/Langflow IF-05 work. |
| [#168 review](https://github.com/amadou-6e/specs/pull/168) B1/B2/M2; remaining #172 findings | Event subjects, event dedup, invocation retry/session semantics, approval service and PR owner are outside this library. Do not silently resolve them through a library field. |

The unresolved cross-owner questions are exact IF-02-to-IF-05 prompt mapping (Langflow/agent execution), E01 and B05 (Langflow), skill revision/draft promotion and B06 if registry reuse is chosen (registry), and external grants plus B07 (approval/GitHub publication). The contract remains draft while these choices and evidence are pending.
