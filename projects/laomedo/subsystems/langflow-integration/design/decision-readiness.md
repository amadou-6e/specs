---
title: Langflow integration decision readiness
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration decision readiness

This is a triage for [specs issue #174](https://github.com/amadou-6e/specs/issues/174), not an accepted runtime contract. The first slice is a direct-prompt or selected-issue, one-agent Langflow workflow with a fresh session and isolated checkout. The third-party Langflow runtime owns graph sequencing; Laomedo's Langflow-integration subsystem owns its durable run record, identity and restart sweep. Trace and result references belong to their respective subsystems. A death of the fate-shared Langflow/Laomedo backend **ends** the run as `crashed`. The UI closing is not a backend crash. There is no graph reattachment, mid-graph resume or idempotent redispatch after backend death. A new, linked run is a separate action and may repeat external effects.

This page owns readiness of the Langflow adapter, not GitHub event receipt, provider execution, approval policy, artifact storage or trace projection. The [interface map](../../README.md#interface-map) identifies those peers. The first slice does not promise timers/events, multi-stage file transfer, local mounts, cross-stage session reuse, selective reruns or automatic mid-turn agent-container recovery. The merged [decision record D17](../../../decisions/0002-subsystem-handoffs.md#execution-recovery-and-inspection) and [agent-execution IF-06](../../agent-execution/contract/interfaces.md#if-06--report-invocation-outcome) now explicitly defer that recovery pending a real mid-turn restart experiment. The [agent-execution readiness PR #182](https://github.com/amadou-6e/specs/pull/182) remains a peer proposal, not runtime evidence.

## Evidence, boundary and notation

The pinned `docs/167` source below is the historical research snapshot. The
merged decision record and current interface sketches take precedence where
that snapshot differs; neither supplies runtime evidence for Langflow crash,
Stop, branch-failure, loop or snapshot behavior.

The inspected baseline is `docs/167` at [`3974d9aa1f380c72105e7f205f16e3eeae2c8d80`](https://github.com/amadou-6e/specs/commit/3974d9aa1f380c72105e7f205f16e3eeae2c8d80), inspected 2026-10-02: this subsystem's [interfaces](../contract/interfaces.md), [design](README.md) and [validation](../validation.md); [shared records](../../../architecture/shared-contracts.md), [handoff graph](../../../architecture/subsystem-handoffs.md), [decision record](../../../architecture/subsystem-decision-record.md), and [user journey](../../../architecture/user-traversal.md); and the linked IF-01/02/05/06/07/09/13 owners in the [interface map](../../README.md#interface-map). The [local Langflow/Codex pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md) is bounded evidence for a saved one-node flow, runner identity and restart of the **host runner**, not for Langflow backend death, multi-stage failure/Stop semantics, or the proposed full interfaces. Its implementation was Laomedo `5e14c7a`, Langflow `1.12.3` with image digest `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`, and Codex CLI `0.159.2`; the model cap was exhausted at 4/4. No model or runtime experiment was executed for this triage.

The review comments on [#166](https://github.com/amadou-6e/specs/pull/166), [#168](https://github.com/amadou-6e/specs/pull/168) and [#172](https://github.com/amadou-6e/specs/pull/172) were treated as hypotheses to classify, not accepted Langflow behavior. Vendor source, API documentation and implementation code were **not inspected** in this pass. That is not evidence of absence. Sibling readiness PRs and later user clarifications are provisional, not merged coverage. In particular, the reviewer proposal to reattach a crashed graph conflicts with the user's subsequent terminal-crash choice; the orphan and duplicate-effect concerns survive that correction.

`A` = ready to specify from a confirmed choice or necessary boundary invariant; `B` = product choice needed; `R` = research/owner handoff; `E` = bounded experiment needed; `D` = defer beyond the first slice. Evidence tags: `[C]` confirmed user choice, `[O]` bounded observation, `[I]` inference, `[U]` unverified. A row has exactly one class. A class is readiness, not proof of implementation. No `[U]` or contested capability is promoted to an accepted guarantee. Every B remains open pending a user decision.

## Question ledger

| ID | Atomic question / exchange | Class, evidence | Dependency and next action | First slice? |
| --- | --- | --- | --- | --- |
| Q01 | What happens to the graph run when the fate-shared Langflow/Laomedo backend dies? | A [C] | Specify terminal `crashed`; no graph reattachment or same-run resume. Align IF-07, IF-09 and result status with [run traces](../../run-traces/contract/interfaces.md) and [results](../../results-artifacts/contract/interfaces.md). | Yes |
| Q02 | What minimum launch record must exist before agent dispatch? | A [I] | Persist run ID, resolved configuration/hash, trigger, start and graph revision; failed persistence blocks dispatch. Exact transaction with Q03 is an implementation design. | Yes |
| Q03 | How is a run found and marked after backend restart? | A [I] | On restart, sweep previously nonterminal runs to `crashed`, suppress further dispatch and request [agent execution](../../agent-execution/contract/interfaces.md) orphan cleanup. Q05 tests the topology; orphan-control effectiveness is not established here. | Yes |
| Q04 | Is Stop a separate durable state or a compact terminal reason? | B [I] | Choose B04 before specifying Stop/dispatch ordering and IF-09 projection; E04 tests the race. | No |
| Q05 | Does closing the UI differ operationally from killing the backend? | E [U] | E01 distinguishes UI reconnect from fate-shared backend termination and possible surviving agent containers. | Yes |
| Q06 | Must every launch carry IF-01 issue context? | A [C] | No. Direct prompt may bypass IF-01; selected issue uses [issue integration](../../issue-integration/contract/interfaces.md). Timer/PR/Actions contexts remain deferred to Q25. | Yes |
| Q07 | Who owns timer/GitHub-event receipt, deduplication and loop guards while UI is closed? | B [I] | Choose B07 with issue integration and deployment owner; do not infer a scheduler from Langflow graph execution. Out of the first slice. | No |
| Q08 | Can a runnable graph revision and component-code identity be frozen? | R [U] | R01 inspect pinned Langflow source/docs for export/snapshot and component resolution; E02 then tests actual mutation behavior. | Yes |
| Q09 | Is there a stable agent-node API for binding per-stage input and selectors? | R [U] | R02 inspect pinned component/runtime APIs; no commitment to parse an internal flow JSON shape. | Yes |
| Q10 | Does mutation of a saved flow after launch leave the active run unchanged? | E [U] | E02; required by D09 but not proved by the one-node pilot. | Yes |
| Q11 | What does a timeout or UI Stop do to an active agent call? | E [O] pinned synthetic [EXP-10](../../../experiments/long-call-timeout/iterations/2026-10-05/results.md) and [EXP-89](https://github.com/amadou-6e/laomedo/blob/35801d0bd30df4d69ed38916c1e61903a8cdf620/experiments/exp89/RESULTS.md); [U] real-agent effect/trace | Outer-client and v2 server timeouts left late synthetic effects. EXP-89's visible Playground Stop did not cancel the bound synthetic runner on the tested `start` path; its blocking `fresh` case is inconclusive. Specify and test an explicit Stop-to-runner path, post-timeout IF-06/07 evidence, real-agent cancellation and crash cleanup before first-slice acceptance. | Yes |
| Q12 | Can Stop prevent a waiting stage from dispatching after Stop was accepted? | E [U] | E04; test concurrent Stop and scheduler release. Q04 defines desired state semantics first. | No |
| Q13 | Does an independent branch continue when another agent node raises? | E [U] | E05; current pilot node raises on error but has no independent branch. Until proven, do not promise D15 behavior. | No |
| Q14 | Are conditional loops, invocation limits and rerun handoffs supported for the target graphs? | D [U] | After first slice, research component/graph constraints then design a bounded experiment; do not infer this from one-node execution. | No |
| Q15 | How are non-agent Langflow components governed if the editor exposes all of them? | B [I] | Choose B15 before treating arbitrary components as safely executable. A selected editor component is not automatically covered by agent-container approvals or telemetry. | No |
| Q16 | Which lifecycle hooks and stable source IDs can produce IF-07 events? | R [U] | R03 inspect pinned Langflow APIs and callback ordering; Q17 chooses the ingest semantics. | Yes |
| Q17 | What deduplicates a replayed IF-07 event after reconnect or restart? | B [I] | [Run traces #179](https://github.com/amadou-6e/specs/issues/179) owns the dedup policy; this adapter must supply producer-stable keys if required. Receipt sequence and optional source ID alone cannot deduplicate. | Yes |
| Q18 | What does IF-09 send to results when a run starts or crashes? | A [I] | Emit frozen launch context before dispatch and terminal `crashed`/incomplete evidence on restart; do not reconstruct the exact selection from tool events. Align downstream result enum with [results](../../results-artifacts/contract/interfaces.md). | Yes |
| Q19 | Can IF-13 reuse a native session after its old stage container is gone? | D [U] | Existing-session follow-up is outside first slice; later check workspace/session binding with agent execution. Fresh linked runs remain distinct. | No |
| Q20 | Does a user-requested linked relaunch reuse old frozen selectors or resolve `latest` anew? | B [I] | Choose B20; never silently pretend it is same-run recovery. Show possible repeated GitHub writes and model spend. | Yes |
| Q21 | Who enforces aggregate run-level time/spend limits across invocations? | B [I] | Choose B21; [agent execution](../../agent-execution/contract/interfaces.md) owns invocation limits, not automatically an aggregate graph budget. | No |
| Q22 | Which stage owns the target PR if a future graph has several agent stages? | B [I] | Choose B22 before multi-stage PR behavior; an agent-created PR ref in IF-10 is observation, not coordination. | No |
| Q23 | How are user files and prior-stage artifacts handed to separate stage containers? | D [U] | Defer multi-stage transport and durable byte owner; coordinate Langflow, [results](../../results-artifacts/contract/interfaces.md) and [execution](../../agent-execution/contract/interfaces.md). | No |
| Q24 | Are local mounts, cross-stage sessions and selective stage reruns in the first slice? | D [C] | No. They need separate binding/collision checks and verified Langflow support; first slice uses one isolated checkout and a fresh session. | No |
| Q25 | Are timer/GitHub-event triggers included in the first slice? | D [C] | No. Later resolve Q07 plus [issue integration](../../issue-integration/contract/interfaces.md) event context, duplicate suppression and CI feedback loops. | No |
| Q26 | Are unattended approval waits covered by Langflow sequencing? | D [I] | Approval ownership, expiry and grant transport are cross-cutting and deferred here; agent execution/chat owners must specify them. Do not mistake a blocking node for approval policy. | No |
| Q27 | Is automatic same-invocation agent-container recovery part of the first slice? | D [C] | No. Merged D17/IF-06 now agree: await the real-agent restart experiment; do not call backend-crash relaunch recovery. | No |
| Q28 | Which identities distinguish a run, graph revision, configured stage and loop invocation? | A [I] | Keep all four distinct across IF-05/06/07/09; one agent node can have multiple invocations without reusing an invocation ID. | Yes |
| Q29 | Are resolved configuration and graph refs durably recorded before dispatch, including across a kill at the persistence boundary? | E [U] | E06 adopts the unresolved handoff from [prompt-library #177](https://github.com/amadou-6e/specs/issues/177); Q02 is the rule, E06 tests its realization. | Yes |

## Open product choices

These are options for review, not selected defaults. The failure/cost column names the tradeoff each choice would impose; no option may be treated as implementation authorization merely because it appears first.

| Choice | Options and consequence | Failure mode / cost |
| --- | --- | --- |
| B04 Stop state | Explicit durable `stopping` phase, or a compact active/terminal state plus stop reason. | Explicit phase clarifies dispatch fencing but adds transitions and persistence; compact state is smaller but may conceal a Stop/dispatch race. E04 must test the chosen model. |
| B07 trigger owner | A dedicated trigger service; Langflow integration; or issue integration. | Dedicated owner cleanly handles timer/event loops but adds a boundary. Langflow ownership centralizes launch but couples scheduler lifetime to graph runtime. Issue integration knows GitHub context but is an awkward timer owner. All require dedup/loop guard and unattended operation. |
| B15 component access | Managed component allowlist; expose all with clearly marked unmanaged components; or implement full sandbox/approval/trace coverage for every component. | Allowlist constrains the promised editor and needs curation. Unmanaged exposure preserves flexibility but risks untraced/unapproved external calls. Full coverage is broad implementation and verification work. |
| B17 IF-07 delivery | Use the canonical [#179 T07/T10 options](https://github.com/amadou-6e/specs/issues/179); Langflow integration supplies or explicitly lacks the lifecycle source key required by that choice. | R03 must establish whether a stable key can be produced. Until #179 chooses a policy, transitions and counts cannot be claimed unique. This is a dependency, not a second policy vote. |
| B20 relaunch selection | Reuse prior frozen refs; resolve current `latest`; or require an explicit user choice. | Reuse best preserves comparison but may depend on unavailable old revisions. Re-resolve may silently alter behavior; explicit choice adds UX friction. All are **new** runs and may repeat external effects. |
| B21 run budget | Langflow aggregate run budget; invocation-only enforcement by agent execution; or a separate quota service. | Langflow aggregate fits sequencing but requires reliable accounting before dispatch. Invocation-only can overspend across loops/branches. Separate quota improves shared policy but adds durable coordination. |
| B22 target PR | Declared delivery-stage target; permit multiple PRs with explicit mapping; or let first created PR become target. | Delivery stage is deterministic but restricts graph design. Multiple PRs require review/summary UX. First-created depends on scheduling and can race, so should not be assumed. |

## Research handoffs

| ID | Source plan and required output | Boundary |
| --- | --- | --- |
| R01 (Q08) | Inspect official source/docs at pinned Langflow version, its flow serialization/export API, and installed component loading. Record whether graph data **and component implementation identity** can be snapshotted; distinguish documented API from internal JSON. | Research only; do not edit the runtime contract until the mechanism is verified. |
| R02 (Q09) | Inspect the same pinned version's component/input APIs and a minimal saved agent-node flow. Record stable selector, input and file binding path, or mark unsupported. | Do not infer from UI labels or one pilot's static component fields. |
| R03 (Q16) | Inspect runtime lifecycle/callback source/docs and emitted event IDs/order on start, completion, error and Stop. Record producer identity availability for Q17. | Read source before E testing; no vendor behavior was established in this triage. |

## Bounded, no-model experiments to design and run later

Each proposal uses a synthetic deterministic node, not an LLM turn. Pin Langflow `1.12.3` and image digest `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` for comparison with the pilot, plus the exact local adapter/fixture commit, Docker Desktop/Windows versions, storage path, graph export/hash, request payload and clock. If the current runtime differs, record a second revision rather than silently transferring the result. Preserve raw API status, event IDs/times, graph snapshots and container/process state in a sanitized evidence manifest; never commit credentials. These rows are prospective protocols; the bounded E03 result is linked below and does not prove its missing integration checks.

| ID | Hypothesis and falsifier | Procedure, observable outcome and approximate cost |
| --- | --- | --- |
| E01 (Q05) UI close vs backend kill | H: UI close leaves run active and reconnectable; killing fate-shared backend ends it and a restart sweep marks `crashed`. Falsified by UI-close termination, hidden continuation after backend death, or no terminal record. | Start long synthetic node, close browser only and reconnect; then repeat with backend hard kill and restart. Record run/stage/container states and whether independent container/GitHub effects survive. Two local synthetic runs, minutes, zero model turns. |
| E02 (Q10) flow freeze | H: an in-flight run uses the launch-time graph/component revisions even if the saved flow is edited. Falsified if a later stage sees the edit or no exact snapshot can be recovered. | Export/hash graph and component identities; hold a synthetic stage, edit graph, release, compare observed execution and frozen record. Requires R01 and a disposable flow; two synthetic variants, minutes, zero model turns. |
| E03 (Q11) long-call timeout | H: timeout yields a visible terminal invocation and does not imply the external action was stopped unless cancellation is observed. Falsified by silent hang, success after terminal timeout without effect accounting, or wrongly complete trace. | Invoke deterministic blocking local endpoint beyond each configured client/build/server timeout; inspect Langflow error/return, downstream process and IF-06/07 timestamps. Duration must exceed the actual configured limit and may be hours; zero model turns. |

| E04 (Q12) Stop race | H: once Stop is accepted, no waiting stage dispatches. Falsified by any post-acceptance invocation start. | First test a one-node invocation paused immediately before dispatch, then a barrier-controlled predecessor and waiting successor; issue Stop at each release boundary and inspect monotonic event times and downstream call counter. Requires B04. Several short local schedules, zero model turns; exact repeat count recorded before execution. |
| E05 (Q13) independent failure | H: a raised agent-node error blocks descendants but permits an independent branch unless end-on-error is selected. Falsified by unrelated branch suppression or unintended descendant execution. | Deterministic diamond graph with one raising branch and one delayed independent branch; compare default and end-on-error modes, event and result states. Two synthetic runs, minutes, zero model turns. |
| E06 (Q29) resolved refs before dispatch | H: resolved refs, graph identity and launch context are durably recoverable before the first agent invocation. Falsified by a dispatched invocation without that record after restart. | With a synthetic no-model node, hard-kill before the record write, between write and durable acknowledgment, and after acknowledgment but before dispatch. Compare the persisted record with the invocation counter after restart. Pin filesystem and flush behavior. Several short local runs, zero model turns. |

E03's bounded runtime portion was executed as
[EXP-10](../../../experiments/long-call-timeout/iterations/2026-10-05/results.md)
at Laomedo `dee05c2`, with amended direct-capture replication at `1fc002a`.
The pinned synthetic probe showed late effects after
outer-client and v2 server timeouts; the component's 2-second HTTP timeout
produced an uncertainty-aware 500 only after the 5-second endpoint effect.
The post-408 job status was subsequently inspected in
[EXP-65](../../../experiments/post-timeout-job-status/iterations/2026-10-05/results.md):
four read-only polls returned terminal `JOB_FAILED`, including one before the
late external effect. That status is not proof of cancellation or effect
reconciliation. IF-06/07 partial trace and real-agent cancellation were not
captured, so Q11 remains a first-slice integration gate rather than a
completed safety claim.

## Crash accounting and ownership proposal

The five questions must have explicit answers in the future contract; this is a proposed minimum accounting rule, not evidence that the current Langflow adapter implements it.

1. **Before dispatch:** persist run ID, graph revision, resolved configuration hash/refs, trigger, start, and stage reservation. If persistence fails, do not dispatch. Laomedo's Langflow integration owns this record; the Langflow runtime still sequences the graph. This is not a second workflow scheduler.
2. **After restart:** mark prior nonterminal runs `crashed`, fence new dispatch for them, retain partial IF-07/08/09 evidence, and ask agent execution to reap orphan containers. A restart sweep alone may not bound a live orphan while the backend is down; the [provisional #175 readiness draft](https://github.com/amadou-6e/specs/blob/5dc5c1e/projects/laomedo/subsystems/agent-execution/design/decision-readiness.md) leaves supervisor/lease ownership and its test open.
3. **Surviving effects:** separately running containers, GitHub pushes/PRs and provider spend might continue after backend death. Their exact survival is unverified; record known effects, unknown effects, and evidence gaps without labeling a partial run clean or rolled back.
4. **Relaunch warning:** a user-requested follow-up gets new run and invocation IDs; warn that it can duplicate writes and spend. Resolve B20 before selecting old frozen revisions versus `latest`. Prompt-only “inspect first” does not make external writes idempotent.
5. **Detection owner:** Langflow integration detects its own incomplete run records on startup and emits the terminal context. Agent execution owns container cleanup effectiveness; results owns presentation; run traces owns evidence projection. A separate watchdog/lease may be required to bound orphans during an outage, but this page does not select one.

The proposal rejects a second Laomedo workflow scheduler as a way to “recover” graphs, because the user selected Langflow for graph sequencing and backend death as terminal. Laomedo's Langflow integration still owns the durable run record and restart marking. It also rejects equating UI reconnect with backend restart, and rejects receipt sequence as an IF-07 deduplication key. This does not reject a trigger service for future timers/events (B07), an orphan supervisor, or a user-requested new linked run.

## Review findings routed to owners

| Finding | Disposition |
| --- | --- |
| #172 backend reattachment / durable-run concern | Reattachment rejected by later user choice (Q01), but prior-run accounting and orphan/duplicate-effect concerns stay (Q02-05, Q20). |
| #172 trigger owner, loop guard and feedback loop | B07/Q25; issue integration owns GitHub context, not necessarily the scheduler. |
| #172 independent branches, Stop race and version freeze | E05, E04, R01/E02 respectively. Do not claim pilot coverage. |
| #172 ungoverned components, PR owner and run budget | B15, B22 and B21. |
| #172 multi-stage files, sessions, local mounts, approvals, failure report | Q23, Q19/Q24, Q26 and peer [results/issue](../../results-artifacts/contract/interfaces.md#if-12--reviewed-failure-to-issue-proposal) ownership. |
| #168 IF-01 required issue and missing trigger context | Q06 direct prompt bypass; future events Q07/Q25 and [issue integration](../../issue-integration/contract/interfaces.md#if-01--issue-context-for-run-setup). |
| #168 IF-07/08 deduplication | Q17 and run-traces ownership; IF-08 belongs to [agent execution](../../agent-execution/contract/interfaces.md#if-08--emit-agent-telemetry). |
| #168 user files and retry contradiction | Multi-stage files Q23 and [IF-05](../../agent-execution/contract/interfaces.md#if-05--invoke-a-configured-agent-stage); same-invocation D17 is deferred Q27. |

No future B choice, untested vendor capability or broader experimental result is implied by this draft. The first-slice column makes the boundary explicit. The one-node path needs Q08/R01→Q10/E02 for freeze, Q09/R02 for the agent-node binding, Q11/E03 for long synchronous calls, Q05/E01 for D16 UI closure, Q16/R03 and #179's Q17 policy for trace lifecycle, Q29/E06 for durable pre-dispatch refs, and #175's orphan-control choice for Q03. Q20/B20 is additionally needed when linked relaunch is included. Q04 Stop, Q15 arbitrary editor components, Q21 aggregate multi-invocation budget and Q22 multi-stage PR ownership are **not** first-slice gates. The selected one-invocation limit remains necessary, but an aggregate graph budget adds no separate first-slice control.
