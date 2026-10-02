---
title: Run-trace decision readiness
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Run-trace decision readiness

This is triage for [specs #179](https://github.com/amadou-6e/specs/issues/179), not acceptance of the [run-trace contract](../contract/README.md) or proof of crash durability. It covers IF-07, IF-08 and IF-11, and H7/H8/H10. Historical research base: [`3974d9aa1f380c72105e7f205f16e3eeae2c8d80`](https://github.com/amadou-6e/specs/tree/3974d9aa1f380c72105e7f205f16e3eeae2c8d80), inspected 2026-10-02. Evidence inspected: [2026-10-01 pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md) (Laomedo `5e14c7a`, Langflow `1.12.3`, Codex CLI `0.159.2`) and [#123 trace research](../../../research/runner-feasibility/sources/123.md) (synthetic projector at Laomedo `2230f22`). The pilot retained **39 events after explicit cancellation**, not backend death. #123 tested duplicate/conflicting IDs, result-before-call and unknown-versus-zero on synthetic envelopes, not provider replay. No current vendor source, private raw trace, hard-crash test or new runtime test was inspected. The pilot spent its **4/4 model-turn cap**. Neighboring #174 and #175 readiness ledgers are still draft proposals.

The first slice is one agent in one Langflow node, launched by direct prompt or selected issue, in an isolated checkout with fresh session, launch-frozen versions, one PR, trace inspection and a reviewed failure issue. Fate-shared Laomedo/Langflow backend death is terminal `crashed`; relaunch is a new linked run, not graph reattachment. UI closure is different. The merged [decision record](../../../decisions/0002-subsystem-handoffs.md) now explicitly defers D17 agent-container recovery from the first slice. This ledger still requires crash-durability and event-identity experiments before implementation claims.

Classes: **A** controllable first-slice rule, **B** user choice, **R** primary-source research, **E** pinned experiment, **D** safely deferred. `[C]` confirmed user choice, `[O]` bounded observation, `[I]` inference/design proposal, `[U]` unverified third-party behavior. Tags are not implementation maturity. Each question has exactly one class; no A item rests on `[U]` or a contested D-ID.

## Triage

| Question | Class | Tags | Blocking dependency | Next action |
| --- | --- | --- | --- | --- |
| T01. Flush-on-receipt, batch, or journal for raw events? | B | [I] durability/throughput trade-off; [O] cancellation only | E01 for measured loss window | Choose acknowledgment and durability policy. |
| T02. What prefix survives an actual backend kill? | E | [U] failure timing | T01 protocol | Run E01 at write/flush/ack cut points. |
| T03. Who is the authoritative raw writer/store? | B | [I] [H8](../../../architecture/subsystem-handoffs.md); [O] pilot runner stores events | #175 orphan/reaper owner | Choose run-traces ingest or agent-execution external file, not two canonical writers. |
| T04. Is an orphan tail frozen/quarantined or visibly growing? | B | [I] inspectability versus retention | T03, #175, E03 | Choose labeling/fencing; neither is complete. |
| T05. How are non-terminal streams labeled on restart? | A | [C] fate-shared crash rule; [I] [IF-11](../contract/interfaces.md) gap | Durable run/trace index | Mark `partial`, reason `crashed`; propose an IF-11 reason field. |
| T06. Does relaunch merge old/new events? | A | [C] new linked run | None | Allocate a distinct run/trace ID and prior-run link; never merge histories. |
| T07. How does IF-08 dedup without native IDs? | B | [O] [IF-08 schema](../../agent-execution/contract/schemas/if-08-agent-event.md) IDs optional; [I] #123 synthetic limit | #175 produces source keys or declares absence; E02 | Run traces owns the dedup/uncertainty policy; choose producer-stable key or at-least-once uncertainty here. |
| T08. Is receipt sequence a dedup key? | A | [O] IF-08 assigns it on ingest; [I] identity rule | None | No; it orders accepted receipts, not source events. |
| T09. What Langflow lifecycle hooks/source IDs support IF-07? | R | [U] Langflow API | #174 lifecycle owner | Inspect pinned source/docs; if absent, consider invocation-record-derived lifecycle. |
| T10. How are IF-07 observations deduplicated? | B | [O] [IF-07 sketch](../../langflow-integration/contract/interfaces.md) source ID optional; [I] | T09 and #174 lifecycle-key producer; E02 | Choose adapter-stable transition key or preserve duplicate uncertainty here; #174 B17 consumes this policy. |
| T11. Does D17 retry reuse run identity? | D | [O] [shared contract](../../../architecture/shared-contracts.md) new run; [C] contested D17 | D17 deferred, #175 identity work | Revisit before agent-container recovery; relaunch is already a new run. |
| T12. What can a one-node trace show directly? | A | [O] pilot native/run refs; [I] first-slice scope | IF-08 data availability | Keep raw one-invocation receipts and native thread/session ID if supplied; missing stays unknown. |
| T13. May projection invent a result/parent edge? | A | [O] #123 synthetic projector; [I] evidence rule | None | No; retain observed/declared/inferred provenance. |
| T14. Does a final message mean complete trace? | A | [O] [IF-11](../contract/interfaces.md); [I] | None | No; completeness is independent of task outcome. |
| T15. Is unknown usage/cost zero? | A | [O] pilot inner usage unknown; #123 outer zero | None | No; preserve unknown, omitted, unsupported and measured zero. |
| T16. Is D18 multi-invocation layout ready? | D | [C] waterfall is candidate only; [I] slice | View-owned Draw.io | Revisit at multi-stage UI workshop. |
| T17. What raw content is retained, redacted and readable? | B | [I] sensitive-content/access trade-off; [O] private raw pilot traces | Product security policy | Choose retention and access before broad export promise. |
| T18. How are loops/cross-stage sessions aggregated? | D | [C] D13/D18 target; [I] outside slice | Multi-stage design | Revisit when multi-stage selected; preserve invocation identities now. |
| T19. Can IF-11 link a failed run? | A | [O] [results IF-11 consumer](../../results-artifacts/contract/interfaces.md); [I] independent states | Reserved trace identity | Return honest refs/completeness independently of success. |
| T20. Can an external writer leave an orphan tail? | E | [U] process lifetime | T03/T04 and #175 reaper | Run E03 synthetic hard kill and tail inspection. |
| T21. What if run/trace ID cannot be durably reserved? | A | [C] direct user clarification, 2026-10-02; [I] invariant | Run-index reservation | **Refuse dispatch** with visible error; no in-memory fallback. |
| T22. Is Codex/Claude projection parity ready? | D | [O] #123 lacks Claude trace | Claude sample/budget | Revisit for second provider; do not infer parity. |

Counts: **A 9 / B 6 / R 1 / E 2 / D 4** (22). There are three experiment sketches because E02 tests the B-class deduplication choices; only T02 and T20 are E-class questions. IF-07: T09–T10; IF-08: T07–T08, T12–T13; IF-11: T05, T14–T15, T19. D18: T16. T21 is a direct user clarification after the research handoff, not an implemented feature.

## User decisions

These are alternatives, not selected contract behavior. T01, T03, T04 and T07 are first-slice blockers; T10 blocks IF-07 if emitted rather than derived. T17 blocks a broad raw-content access promise. Costs are relative, not measured.

| Item | Option | Consequence / failure prevented or caused | Cost |
| --- | --- | --- | --- |
| T01 | Flush each receipt before acknowledgement | Bounds acknowledged loss under tested storage contract; may throttle ingest. | High per-event IO/latency. |
| T01 | Bounded batch flush | Higher throughput; acknowledged tail may vanish unless ack waits for commit. | Scheduler and explicit loss-window accounting. |
| T01 | Append journal then project asynchronously | Durable capture separated from read projection. | Journal recovery and extra storage. |
| T03 | Run traces ingests and owns canonical raw store | One sequence/retention owner; producer can lose unhanded events. | Ingest API and backpressure. |
| T03 | Agent execution owns one durable external raw file | May retain more events during backend loss, but orphan writer can append. | File fencing, reconciliation, access control. |
| T04 | Freeze confirmed prefix; quarantine later tail | Stable `crashed` trace and separable orphan evidence. | Fence/quarantine mechanism and UI. |
| T04 | Show visibly growing partial/orphan tail | Retains observation, but terminal trace changes over time. | Versioned status/read snapshots. |
| T07 | Require producer-stable key | Can dedup redelivery; keyless provider needs durable adapter key or fails. | Producer journal and key contract. |
| T07 | Accept at-least-once receipts with uncertainty | Keyless provider works, but action counts may include repeats. | Projection and review ambiguity. |
| T10 | Require adapter-stable transition key | Deterministic IF-07 dedup even without native ID. | Adapter state and hook research. |
| T10 | Keep all lifecycle receipts with uncertainty | Avoids false collapse, but duplicate transitions may inflate activity. | Richer read model. |
| T17 | Short guarded raw retention/redacted export | Less exposure, but later reprojection may be impossible. | Expiry/redaction/audit controls. |
| T17 | Longer encrypted owner-only retention | Better forensics with more sensitive-data exposure. | Key management/storage/deletion work. |

Proposed T03 boundary, pending user choice: run traces is the authoritative raw store and receipt-identity owner; agent execution is a producer that may spool until acknowledged handoff. Reject dual canonical logs. The alternative is one agent-execution-owned external file with run traces indexing it; that can preserve a tail but requires stronger fencing. Neither was hard-crash tested. [#175](https://github.com/amadou-6e/specs/issues/175) Q28 now records the producer-side raw-writer dependency and owns orphan cleanup. This page owns the T07/T10 dedup policy; #175 and #174 own key production, not parallel policy votes.

## Research handoff

**T09 — Langflow lifecycle evidence.** Inspect Langflow `1.12.3` primary source/docs for graph/run/node callbacks, timing, source IDs, replay semantics, and terminal failure after node exception. Record commit/package version, access date, exact files/API signatures, counterexamples and applicability to Laomedo's node. Compare the [pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md), which observed an outer trace but not a proven IF-07 feed. Return an adapter-stable key candidate or explicit absence; if no hook exists, coordinate with #174 on deriving stage lifecycle from IF-05/IF-06 records. A search result or review is not primary evidence.

## Experiment sketches

**Not executed.** All use synthetic fixtures, zero model turns, a pinned Laomedo adapter/fixture commit, OS/Docker, filesystem and fsync settings, and the exact selected protocol. Include Langflow `1.12.3` image digest `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` when it participates. The pilot's 4/4 model turns cannot be reused. Estimates below exclude fixture construction.

| Experiment / unblocks | Hypothesis / falsifier | Minimal pinned procedure | Outcome / estimated cost |
| --- | --- | --- | --- |
| E01 — T02/T01 durability | Acknowledged receipts survive hard backend death to chosen boundary; falsified by an acknowledged missing event presented as complete or unreported gap. | Hard-kill before append, after write/before flush, and after ack; restart and compare producer ledger, raw prefix, receipt sequence and IF-11. Repeat each cut point. | Specify measured prefix/loss only for pinned FS/protocol or revise T01. ~10–30 min execution plus fixture. |
| E02 — T07/T10 dedup | Chosen key/uncertainty rule creates no fabricated confirmed unique action; falsified by duplicate action represented as distinct confirmed or conflicting payload collapsed. | Replay keyed, keyless, reordered and conflicting-ID IF-07/IF-08 fixtures through pinned ingest/projector; compare raw receipts and projections. Include call ID reused by start/completion. | Require producer key or explicit at-least-once uncertainty; #123 synthetic tests do not prove provider replay. ~10–20 min plus fixture. |
| E03 — T20/T03/T04 orphan tail | Chosen policy detects post-crash writes and keeps them separate from confirmed prefix; falsified by unmarked growing `crashed` trace or lost tail claimed complete. | Run synthetic external writer, hard-kill backend while appending; inspect before restart and after #175 reaper sweep. No model/GitHub. | Specify fence/quarantine or versioned partial tail; coordinate #175 E01. ~10–30 min plus fixture/reaper. |

## Crash behaviour

1. **Persist first.** Reserve durable run/trace IDs, frozen refs and invocation identity before dispatch (T21). T01 must define whether event acknowledgement means durable raw storage. IF-11 exposes last confirmed sequence and completeness; the pilot does not prove a hard-crash prefix.
2. **Restart.** Mark unfinished streams `partial` with reason `crashed` (T05); retain confirmed prefix. T04 determines treatment of later orphan tail, and #175 owns stopping/cleaning orphan containers. No graph reattach or same-run redispatch.
3. **Orphans.** An external writer or container may continue after backend death (T20, untested); its tail is not automatically pre-crash confirmed evidence. A trace cannot prove a GitHub PR write finished; agent execution owns that external effect.
4. **Relaunch.** New linked run and trace IDs (T06), no merge. Similar provider events or repeated external actions remain separate; deferred D17 intra-invocation retry is a different question (T11).
5. **Detection.** Run traces need not sense the kill live. On restart it learns `crashed` from the run-state owner and identifies unfinished local streams. T09 determines whether IF-07 can supply lifecycle events. UI closure is not a crash.

## Review and boundary coverage

| Finding / boundary | Disposition |
| --- | --- |
| [#168 review](https://github.com/amadou-6e/specs/pull/168) B2 / IF-08 | T07–T08/E02 accept the finding: optional source IDs plus receipt sequence do not guarantee dedup. The merged [IF-08 text](../contract/interfaces.md) now states that uncertainty; the policy choice and replay test remain open. |
| #168 M2 | T11 separates old shared-contract retry/new-run wording from deferred D17 same-invocation recovery. #168 B1 trigger shape and M1 input files belong to issue integration/agent execution, not traces. |
| [#172 review](https://github.com/amadou-6e/specs/pull/172) H-1 | Reject proposed graph reattach/run-ledger remedy under later fate-shared decision; retain orphan/duplicate problem in T03–T04/T20. |
| #172 H-15/H-16 | Results owns failure-report assembly; traces owns IF-11 completeness and honest usage/cost (T14–T15/T19). |
| [#166 review](https://github.com/amadou-6e/specs/pull/166) | Trace/crash concerns are hypotheses, not an accepted guarantee. |
| IF-07 / H7 | Langflow integration produces lifecycle; T09 research and T10 policy open. #174 B17 is provisional. |
| IF-08 / H8 | Agent execution produces native events/IDs; traces owns receipts/projection. #175 orphan cleanup is provisional. |
| IF-11 / H10 | Traces supplies independent trace link/completeness; results assembles missing inputs. |

Cross-owner decisions: T03/T04 with agent execution writer/reaper, T09/T10 with Langflow adapter, T07 with event producer key. Before implementation, record the fate-shared crash rule and the user's T21 refuse-dispatch choice as new D-IDs in one central decision-record PR, and reconcile the older D17 wording; this subsystem PR does not edit peer decisions or contracts.
