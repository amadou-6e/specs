---
title: Langflow integration decision readiness
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration decision readiness

This is a **triage**, not an accepted runtime contract. Source baseline:
[`docs/167` at `3974d9aa`](https://github.com/amadou-6e/specs/tree/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo), including the [interface map](../../README.md), [handoff edges](../../../architecture/subsystem-handoffs.md), [D01–D25](../../../architecture/subsystem-decision-record.md), and [shared records](../../../architecture/shared-contracts.md). The later [#172 decision record at `4946315`](https://github.com/amadou-6e/specs/blob/49463154045c8e3b2fa7eefc991519bbe0fda150/projects/laomedo/decisions/0002-subsystem-handoffs.md) and [#166](https://github.com/amadou-6e/specs/pull/166), [#168](https://github.com/amadou-6e/specs/pull/168), and [#172](https://github.com/amadou-6e/specs/pull/172) reviews are critique, not proof of Langflow behavior. The [pilot result](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md) covers Langflow 1.12.3, Codex CLI 0.159.2 and Laomedo code `5e14c7a`; its model-turn ledger is exhausted at 4/4. Research inspected these pinned files, linked subsystem pages and runner-feasibility sources 118/120/123/124, **not** current Langflow vendor source or documentation. No new runtime test was run.

The first slice is one agent in one Langflow node, launched by direct prompt or selected issue, with isolated checkout, fresh session, frozen `latest`/pinned references, one PR, trace inspection and reviewed failure-to-issue conversion. The user decided on 2026-10-02 that a fate-shared Laomedo/Langflow backend crash ends active runs: no graph reattachment, in-flight resume or idempotent redispatch; a later relaunch is a new linked run. This choice is not yet in the pinned D01–D25 record and needs the next D-ID in a separate decision PR. **For this first slice only**, the user also deferred D17 automatic *agent-container* crash recovery: such a crash is terminal. D17 remains the later target, not an observed capability. Closing the UI is not a backend crash (D16).

Tags: **[C]** confirmed user choice (D-ID or the dated new choice), **[O]** observation in pinned pilot/review evidence, **[I]** inference, **[U]** unverified third-party capability. A row has exactly one readiness class: **A** decide now; **B** user decision; **R** source research; **E** pinned experiment; **D** safely deferred. The class is for the *question*, not an assertion that its proposed answer works. Rows with B, R or E are not silently binding contract language. Links to another subsystem identify questions for its owner, not decisions here.

## Triage

| Question / boundary | Class | Tags and evidence | Blocking dependency | Next action |
| --- | --- | --- | --- | --- |
| Q01 Distinguish run, flow revision, stage, invocation and native session identities (H4–H7; IF-05/06/07) | A | [C] D02–D03, D18 and the first-slice definition; [I] interface map | None for one node | Keep separate opaque identities in the launch and invocation records. |
| Q02 Run states `pending`, `running`, `completed`, `failed`, `interrupted`, `crashed`; terminal states are the last four | A | [C] fate-shared choice and first-slice D17 deferral; [I] state projection | Stop-specific `stopping` excluded | Langflow integration writes `pending` on accepted launch, `running` after dispatch acknowledgement, `completed`/`failed` from one-node outcome, `interrupted` from confirmed interruption, and `crashed` only in startup sweep. Do not claim Langflow has these native states. |
| Q03 Is `stopping` a distinct state, and what blocks dispatch during Stop? (#172 H-9) | B | [C] contested D15; [I] race | User stop policy | Choose in B03 before freezing the Stop contract. |
| Q04 Persist run ID, trigger, exact resolved configuration ref/hash, graph revision and start time **before** H4 dispatch; emit launch IF-09 | A | [C] D09, D24; [I] IF-09 | Persistent store implementation is separate | Specify write-before-dispatch invariant; failed persistence means no dispatch. |
| Q05 On backend restart, find formerly nonterminal runs, mark `crashed`, emit terminal IF-09, never resume their graph | A | [C] 2026-10-02 fate-shared choice; [I] restart projection | No third-party recovery assumed | Define one-way startup reconciliation; preserve partial evidence. |
| Q06 Who tells agent execution to terminate/check orphan containers after backend crash? | B | [I] H5/H6 ownership split; #172 H-1/H-12 | Agent execution owns containers | Select B04; no process cleanup guarantee before the handoff exists. |
| Q07 Relaunch creates new run linked to crashed run, with warning that GitHub effects may already exist | A | [C] fate-shared choice; [I] #172 H-1 | PR lookup belongs agent execution | Record `prior_run_id` and side-effect warning; never label relaunch idempotent. |
| Q08 Relaunch uses old frozen refs or re-resolves `latest` | B | [C] D09; [I] reproducibility/freshness trade-off | Product choice | Select B05; do not silently reuse or refresh. |
| Q09 Does the embedded UI run separately enough that closing it leaves backend alive? | R | [C] D16; [U] topology | Vendor/code evidence | Investigate R01; separate UI close from process crash. |
| Q10 Does UI close/reconnect preserve one progressing run and inspection identity? | E | [C] D16; [U] runtime behavior | Q09 | Run E01 after topology is known. |
| Q11 Direct prompt must not fabricate an IF-01 issue; selected issue consumes IF-01 (H1/H2; #168 B1) | A | [C] first-slice direct-prompt and selected-issue choices, confirmed 2026-10-02; [I] current IF-01 requires issue | Issue integration must correct its own schema | Send issue-integration owner the optional/no-issue trigger requirement; keep direct input in launch context. |
| Q12 Who owns future timer/GitHub event scheduling, duplicate suppression, loop guard and missed-fire policy? (D07/D08; #172 H-2) | B | [C] contested D07/D08; [I] event loop risk | Outside first slice | Resolve B01 before enabling triggers; fate sharing means timers cannot fire while backend is down. |
| Q13 Resolve each prompt/skill `latest` or pin to an exact immutable ref at launch (IF-02; D09) | A | [C] D09; [I] IF-02 | Source revisions must exist | Freeze the selected refs/hash; missing revision prevents dispatch. |
| Q14 Can Langflow execute a frozen flow snapshot, including custom component code identity? (#172 H-10) | R | [C] D09; [U] Langflow API | Vendor source/docs | Investigate R02 before promising snapshot semantics. |
| Q15 Does an edited flow/component leave an already-launched run at the original bytes? | E | [C] D09; [U] runtime behavior | Q14 | Run E02; fail closed if immutable execution cannot be established. |
| Q16 Can agent-node prompt/skill selectors be extracted through a stable public interface, not internal JSON? | R | [I] configuration design; [U] API | Vendor source/docs | Investigate R03. |
| Q17 Does the pilot's synchronous IF-05/06 HTTP call tolerate multi-hour invocations and bound failure? | E | [O] pinned pilot has blocking node; [U] long duration | Langflow 1.12.3 behavior | Run E03 with synthetic HTTP; no model turns. |
| Q18 Does Langflow cancellation stop in-flight calls and prevent a ready stage dispatch after Stop? | E | [C] D15; [U] cancellation; [O] pilot tested runner cancel only | Q03 stop policy | Run E04; pilot HTTP 500 is not Langflow Stop proof. |
| Q19 Does a raised node let independent branches continue? (#172 H-8) | E | [C] contested D15; [O] pilot node raises; [U] branch behavior | Outside one-node slice | Run E05 before accepting branch independence. |
| Q20 Is there a supported bounded conditional-loop API? | R | [C] D01/D15; [U] Langflow API | Outside one-node slice | Investigate R04. |
| Q21 Does the pinned runtime enforce the configured loop bound under failures? | E | [U] runtime behavior | Q20 | Run E06 after R04. |
| Q22 Should node errors be raised or represented as data for downstream branches? | B | [I] policy/graph semantics | Outside first slice; Q19 | Choose B06 after E05. |
| Q23 Expose all Langflow components or allowlist/mark unmanaged external-call components? (#172 H-11) | B | [C] contested D01; [I] approval/trace bypass risk | Outside one-node slice | Choose B07 before unrestricted editor release. |
| Q24 Does Langflow expose native lifecycle hooks for IF-07? | R | [U] capability | Vendor docs/source | Investigate R05. |
| Q25 What IF-07 source identity/deduplication guarantee is promised? (#168 B2) | B | [I] optional native IDs cannot guarantee dedup | Q24 | Choose B08; receipt sequence alone is not a stable source ID. |
| Q26 Emit IF-09 at launch and terminal, including `crashed` on restart | A | [C] fate-shared choice; [I] current payload omits `crashed` | Results must support terminal value | Propose additive `crashed` status and missing/partial evidence semantics; current contract remains flagged below. |
| Q27 Existing/new-session IF-13 follow-up and selective rerun | D | [C] D19/D23; [U] selective rerun | Not needed for first run | Revisit when follow-up slice starts; agent execution owns session binding (#172 H-7). |
| Q28 Who materializes user/upstream files across separate stage containers? (#168 M1; #172 H-6) | B | [C] D04/D12; [I] missing owner | Multi-stage only | Choose B09 with agent execution/results; IF-05 needs a manifest there. |
| Q29 Who enforces a run-wide budget across invocations? (#172 H-16) | B | [I] per-invocation cap is insufficient | First-slice aggregate policy not settled | Choose B02; agent execution still owns per-invocation limit enforcement. |
| Q30 Who reserves the one target PR when several stages can publish? (#172 H-13; D10/D23) | B | [C] contested D10/D23; [I] parallel-write race | Multi-stage only | Choose B10; first slice has one PR-writing stage. |
| Q31 Agent-container crash recovery D17 in this first slice | D | [C] explicit 2026-10-02 deferral; [O] pilot did not test mid-turn crash | First slice treats agent-container crash as terminal `failed`, not backend `crashed` | Revisit with bounded duplicate-effect experiment before implementing D17. |
| Q32 Does a fate-shared backend kill/restart leave a correctly marked run and no new dispatch? | E | [C] crash rule; [U] actual process behavior | Q04/Q05 implementation | Run E07; orphan detection belongs Q06. |

Counts: **A 8 / B 10 / R 5 / E 7 / D 2 = 32**. These counts describe triage rows, not accepted features or passing tests.

## User decisions required (class B)

Each proposal is **ownership pending**, not a contract. The first-slice blockers are B02 (budget policy if a run-wide cap is required) and B03 (only if Stop is included); the remaining B choices either govern post-crash relaunch or later multi-stage/event scope. D17 is separately deferred by the user.

| ID / question | Option | Consequence | Failure prevented or caused | Cost |
| --- | --- | --- | --- | --- |
| B01 Trigger/scheduler owner | Langflow integration owns trigger registry, duplicate keys and loop guard | One owner sees launch identity and config | Can suppress duplicate event launches; expands this subsystem beyond launch | Persistent scheduler/event ingress |
| B01 | Issue integration owns GitHub hooks; Langflow integration owns timer | Provider-specific ingress | Splits loop guard and missed-fire accounting | Cross-owner coordination |
| B01 | New trigger subsystem | Independent scheduling | Clear clock/event boundary, but extra interface and deployment | New subsystem/API |
| B01 missed-fire policy | Skip timer slots missed while the fate-shared backend was down | No surprise catch-up workload | A scheduled task may never run | Simple slot accounting and visible missed status |
| B01 | Launch one bounded catch-up run on restart | Recovers some missed work | Can produce stale or duplicate effects unless dedup and loop guards work | Persistent slot history and concurrency controls |
| B02 Run-wide budget owner | Langflow integration reserves aggregate run budget; agent execution enforces each invocation | Budget spans stages and loops | Prevents unbounded workflow spend; requires atomic accounting | Shared ledger/API |
| B02 | Agent execution owns aggregate budget | One enforcement service | Can enforce before model turns; needs graph/run-wide policy input | Broader agent-execution state |
| B03 Stop state/barrier | Persist `stopping` before Langflow cancellation and reject later IF-05 dispatch | Explicit race barrier | Prevents post-Stop launches; requires all launch paths to check it | State transition plus dispatch guard |
| B03 | No separate state; best-effort cancel only | Simpler | A waiting stage may dispatch after Stop | Lower implementation cost, higher surprise |
| B04 Orphan cleanup owner | Langflow integration sends restart sweep notices; agent execution reaps its containers | Separates run status from process ownership | Detects orphan agents after fate-shared crash | Durable orphan inventory and handoff |
| B04 | Agent execution independently sweeps containers against run status | No explicit notice | Avoids missed notification; may race status update | Cross-store reconciliation |
| B05 Crashed-run relaunch revision | Reuse prior exact frozen refs | Reproducible rerun | Avoids silent drift; may miss desired fixes | Old artifacts retained |
| B05 | Re-resolve `latest` under a new run | Fresh versions | Picks up fixes; can obscure comparison with crashed run | New explicit resolution/provenance |
| B06 Error representation | Raise failure into Langflow | Uses native error path if available | May abort independent branches | Native semantics test needed |
| B06 | Return structured error-as-data | Graph may branch explicitly | Keeps graph live but can mask a true failure if unchecked | Conditional plumbing/validation |
| B07 Component exposure | Expose all components with unmanaged-external-call warning | Honors D01 surface intent | Some calls may evade Laomedo approval/trace | Audit and warning UI |
| B07 | Allowlist managed components until adapter exists | Stronger boundary | Blocks some Langflow functionality, contrary to literal D01 | Registry and review process |
| B08 IF-07 dedup | Require stable producer event ID for exactly-once projection | Replay can be deduplicated | Blocks sources lacking IDs | Adapter-generated durable IDs |
| B08 | At-least-once events; explicitly no cross-restart dedup guarantee | Accepts more sources | Duplicates possible after reconnect/replay | Consumer tolerance and clear labeling |
| B09 Inter-stage file owner | Agent execution materializes a versioned input manifest from user/upstream refs | Receiver owns bytes offered to agent | Avoids missing files; may duplicate artifact access policy | Manifest and mounts |
| B09 | Results/artifacts stages files, agent execution only mounts | Central artifact custody | Clean location owner; risks premature result coupling | Staging API and lifetime rules |
| B10 Target PR owner | Langflow integration reserves one `target_pr` slot at run launch; agent execution performs write | Run-level intent is visible | Prevents parallel stages creating competing PRs | Reservation/compare-and-set |
| B10 | Agent execution arbitrates writes; results records winner | Central GitHub writer | Can block duplicate PRs but decides workflow policy indirectly | Write arbiter and contention handling |

## Research questions (class R)

No current vendor source was inspected; these are reproducible research assignments, not claims that APIs exist. For each, inspect Langflow **1.12.3** official docs and pinned source first, record exact file/line or documentation revision and access date, and report direct evidence, contradictions and upgrade limits. Do not infer support from a registered component name.

Research boundary: Langflow runtime/editor APIs and component loading for the
local 1.12.3 deployment; exclude unrelated hosted variants unless source shows
they share the same path. Search official documentation, tagged source, relevant
tests and release notes; record the query/path selection, inspected portion,
source owner/version/access date and likely selection bias. For each answer,
return an atomic finding with direct evidence, counterevidence, applicability,
confidence and **directly verified / externally reported / inferred /
unverified** classification. Distinguish *not found* from *not inspected* and
*not supported*. Report any actual commands/tests separately from source
reading; do not use a search result or issue comment as proof of runtime
behavior. If documentation and code conflict, record both and leave the
behavior for a pinned experiment.

| ID | Question and search boundary | Required handoff |
| --- | --- | --- |
| R01 | What process serves the embedded editor, run API and backend; does closing only the browser window affect the backend? Inspect deployment/embedding docs and UI/server process startup at pinned version. | Topology diagram with source locations; distinguish browser close from server restart; mark uninspected deployment variants. |
| R02 | Is a flow executable from immutable snapshot/copy rather than mutable saved ID, and where are custom-component code bytes/version captured? Inspect run endpoint and component loader source. | API fields, execution lookup path, hash coverage and negative evidence; feed E02. |
| R03 | Is there a stable public way to enumerate agent-node selectors (prompt, skill, model/effort) for launch resolution? Inspect component schema and public flow API. | Field mapping and version sensitivity; internal JSON-only route is a limitation. |
| R04 | What conditional/loop constructs and limit fields exist in Langflow 1.12.3? Inspect source/docs, not screenshots alone. | Exact API/graph semantics and unresolved runtime behavior for E06. |
| R05 | Which lifecycle hooks/events expose run, stage and invocation identity and stable source event ID? Inspect event API, callbacks and streaming source. | Hook/ID inventory with absence versus not-found distinguished; if no suitable hook exists, describe what agent-execution records could derive and which non-agent transitions would remain unobserved. Feed B08 and E08 without choosing the source. |

## Pending experiments (class E)

**None executed.** Pin Langflow `1.12.3` image digest `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`, the local Docker/Desktop environment, and a synthetic local HTTP component; no agent/model invocation. Model-turn estimate for every experiment: **zero**. Time estimates are operator wall-clock, not measured runtime. Any real agent turns require a new explicit budget because the pilot ledger is 4/4.

The triage has seven E-class questions. E08 is contingent on the R-class hook
inventory Q24 and B-class event guarantee Q25; E09 is contingent on the B-class
file owner Q28. They are listed as later test designs, **not** additional
E-class triage questions or first-slice readiness gates.

| ID / unblocks | Hypothesis; falsifier | Minimal synthetic procedure | Meaning of outcomes; estimated cost |
| --- | --- | --- | --- |
| E01 / D16, Q10 | UI close does not end backend run; falsified by termination or duplicate run | Start delayed synthetic node; close only browser UI; reopen and inspect same run ID | Pass permits reconnect contract; fail reopens process-topology design. ~15 min, zero turns. |
| E02 / D09, Q15 | Launched run uses frozen flow/component A after edit to B; falsified by B output/hash | Snapshot/copy A, launch delayed node, edit saved flow and component to B, inspect executed bytes and result | Pass supports freeze implementation; fail requires immutable copy mechanism or no launch. ~20 min, zero turns. |
| E03 / IF-05/06, Q17 | Synchronous bridge survives configured long delay or fails bounded with correlated outcome; falsified by silent timeout/lost identity | Synthetic HTTP endpoint delays across configured request/build timeouts; record response and trace | Pass bounds one-node call; fail requires asynchronous adapter/timeout policy. ~time limit plus 15 min, zero turns. |
| E04 / D15, Q18 | Stop prevents new dispatch and ends active call; falsified by post-Stop dispatch or live untracked worker | Synthetic active node plus ready downstream node; invoke Stop near transition; inspect launch log/processes | Pass informs B03; fail requires stronger barrier. ~20 min, zero turns. |
| E05 / D15, Q19 | One raising branch leaves independent branch running; falsified by its abortion | Two independent synthetic branches; one raises; inspect the other's output | Pass permits conditional branch policy; fail reopens D15 or requires error-as-data. ~15 min, zero turns. |
| E06 / D15, Q21 | Conditional loop stops at configured limit even with error path; falsified by extra invocation | Build bounded synthetic loop after R04; count invocations and terminal state | Pass supports limited loops; fail forbids loop launch. ~20 min, zero turns. |
| E07 / fate-shared crash, Q32 | Persisted run becomes `crashed` on restart with no redispatch; falsified by stale `running`, duplicate dispatch or surviving orphan | Start delayed synthetic run, kill fate-shared backend, restart, sweep, inspect run and container registry | Pass validates implemented sweep only; fail blocks crash contract. ~20 min, zero turns. |
| E08 / IF-07, Q24–Q25 | Lifecycle adapter emits correlatable transitions and stable IDs if promised; falsified by missing/duplicate transition or missing ID | After R05, run synthetic one-node flow; compare native hook, adapter event and trace projection | Pass supports chosen B08 guarantee; fail narrows IF-07. ~15 min, zero turns. |
| E09 / D04, Q28 | A file ref survives mixed-component handoff; falsified by inaccessible or changed bytes | After file owner chosen, pass hashed tiny fixture through non-agent and agent-shaped synthetic components | Pass supports later multi-stage scope; fail revisits materialization boundary. ~20 min, zero turns. |

## Crash behaviour: five answers

1. **Persist before dispatch:** Q04's run ID, trigger/input ref, exact resolved config ref/hash, flow revision and start time, plus a write acknowledgement. IF-09 launch context is the proposed handoff to results. If that write fails, no H4 dispatch. This is an [I] design consequence of the confirmed fate-shared rule, not pilot evidence.
2. **Restart:** Q05's sweep marks all formerly nonterminal runs `crashed`, emits terminal IF-09, retains partial IF-07/08 and IF-10/11 evidence, and never resumes the graph. A first-slice agent-container crash *while the backend remains alive* instead produces IF-06 failure and one-node run `failed`; it is not `crashed`. Container cleanup is B04 with agent execution; `stopping` is B03. No claim that a dead process itself can write the terminal state.
3. **Orphans:** Docker agent containers or subprocesses may outlive the fate-shared backend and may still write to GitHub; fate sharing alone does not prove process-tree termination. The agent-execution owner must supply an orphan inventory/reap path. Until B04 and E07 pass, external writes remain uncertain.
4. **Relaunch:** new linked run; it may duplicate an already-created PR or other external effect. Q07 requires a prominent prior-effects warning and current-GitHub check; B05 chooses revision semantics. Prompting an agent to look first is not an idempotence guarantee.
5. **Detection:** no live crash handler is assumed. A subsequent backend startup detects prior nonterminal records and marks `crashed`; if it never restarts, status remains last persisted and must be displayed as stale/unknown rather than falsely complete. E07 validates only an implemented sweep, not the design by itself.

## Review coverage and cross-owner handoffs

| Finding/interface | Disposition here |
| --- | --- |
| IF-01 / #168 B1 | Q11: direct launch has no issue; issue-integration schema correction is outside this folder. |
| IF-02 | Q13, Q14–Q16: library refs frozen; flow snapshot and selector access unverified. |
| IF-05/06 / #168 M1/M2 | Q01, Q17, Q28, Q31: agent execution owns user-file manifest, retry/session identity and container failure. D17 deferred only for first slice. |
| IF-07 / #168 B2 | Q24–Q25: native hook research and dedup policy; optional IDs do not prove replay dedup. |
| IF-09 | Q04–Q05, Q26: launch/terminal context and proposed `crashed` value. |
| IF-13 | Q27: follow-up/existing session and selective rerun deferred; not a first-run launch dependency. |
| #172 H-1 | Problem retained (Q06–Q08, Q32), proposed durable reattachment ledger rejected by fate-shared choice. |
| #172 H-2/H-3/H-4/H-5 | Scheduler B01; approval broker, local mounts and cross-stage sessions belong agent execution and are outside first slice. |
| #172 H-6/H-7/H-8/H-9 | File owner B09; existing-session follow-up Q27; branches/loops Q19–Q22; Stop Q03/Q18. |
| #172 H-10/H-11/H-12/H-13 | Flow freeze Q14–Q16; all-components B07; recovery Q31 deferred but external duplicate risk Q07; PR owner B10. |
| #172 H-14/H-15/H-16 | Active GitHub review-context fetch belongs results/issue integration; failure-report producer belongs results; budget B02. |
| #166 graph review | H1/H3/H4–H7/H16 are covered by rows above; its review is a hypothesis, not implementation evidence. |

The [agent-execution owner](../../agent-execution/contract/interfaces.md) must settle D17's later recovery, workspace/session conflicts, external access approval, IF-05 user-file manifest, orphan reaping and PR write semantics. [Results](../../results-artifacts/contract/interfaces.md) owns partial/failure report assembly and active PR review-context presentation; [issue integration](../../issue-integration/contract/interfaces.md) owns no-issue trigger shape and reviewed issue publication; [run traces](../../run-traces/contract/interfaces.md) owns IF-07 event storage/projection. These are proposed handoffs, not unilateral edits to those contracts.
