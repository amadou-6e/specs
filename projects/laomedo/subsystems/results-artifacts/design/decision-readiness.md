---
title: Results and artifacts decision readiness
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results and artifacts decision readiness

This is triage for [specs issue #180](https://github.com/amadou-6e/specs/issues/180),
not acceptance or runtime evidence. The inspected base is `docs/167` at
`3974d9aa1f380c72105e7f205f16e3eeae2c8d80` (2026-10-02). The
[decision record](../../../architecture/subsystem-decision-record.md),
[handoff inventory](../../../architecture/subsystem-handoffs.md),
[shared records](../../../architecture/shared-contracts.md), this subsystem's
[interface sketch](../contract/interfaces.md), and the linked providers and
consumers are the local sources at that SHA. [#174 PR #188](https://github.com/amadou-6e/specs/pull/188),
[#175 PR #182](https://github.com/amadou-6e/specs/pull/182), and
[#179 PR #189](https://github.com/amadou-6e/specs/pull/189) are *unmerged
drafts*, not base contracts. Their proposed crash-sweep and trace decisions
inform dependencies only. The fate-shared crash constraint is the confirmed
user decision quoted in issue #180: a Laomedo/Langflow crash ends the run;
restart marks it `crashed`; relaunch creates a newly identified linked run.
Neither a crash nor a relaunch was run for this draft.

Pinned source snapshots: [decision record](https://github.com/amadou-6e/specs/blob/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo/architecture/subsystem-decision-record.md),
[handoff inventory](https://github.com/amadou-6e/specs/blob/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo/architecture/subsystem-handoffs.md),
[result interfaces](https://github.com/amadou-6e/specs/blob/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo/subsystems/results-artifacts/contract/interfaces.md),
[IF-09/13](https://github.com/amadou-6e/specs/blob/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo/subsystems/langflow-integration/contract/interfaces.md),
[IF-10](https://github.com/amadou-6e/specs/blob/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo/subsystems/agent-execution/contract/schemas/if-10-output-manifest.md),
[IF-11](https://github.com/amadou-6e/specs/blob/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo/subsystems/run-traces/contract/interfaces.md),
and [IF-12](https://github.com/amadou-6e/specs/blob/3974d9aa1f380c72105e7f205f16e3eeae2c8d80/projects/laomedo/subsystems/issue-integration/contract/interfaces.md).

Classes: **A** draftable now; **B** user choice; **R** source research;
**E** pinned experiment; **D** outside the first single-agent slice. Tags:
**[C]** confirmed decision, **[O]** observed evidence, **[I]** inference,
**[U]** unverified capability. A row tagged [I] is a proposed invariant,
not a claim of implementation. No A row relies on [U] or a contested D-ID.

## Question triage

| ID / question and coverage | Class | Tags | Blocking dependency | Next action |
| --- | --- | --- | --- | --- |
| T01 IF-09/IF-10/IF-11, H9/H10: join by exact run and invocation identity; absent input remains visibly missing | A | [C:D24] [I] | None for the invariant; persistence is E01 | Retain in contract; test E01 |
| T02 IF-09, H13: display `crashed` as distinct from failed/interrupted/incomplete | A | [C:issue #180] [I] | IF-09 producer enum lacks it; peer change pending | Propose coordinated enum extension; do not imply current producer emits it |
| T03 IF-10, H9/H12: inventory only reported artifacts and confirmed PR refs; never infer a PR from a diff, prose or absent manifest | A | [C:D24] [I] | External effect discovery is B02 | Retain provenance rule and visible unknowns |
| T04 IF-10/H9: unreachable location is `unknown` until deletion is verified; `lost` requires evidence | A | [C:D24] [I] | Checkout sweep is E03 | Keep uncertainty explicit in projection |
| T05 IF-12/H13/H14: failure proposal stays editable until explicit user review/publish; failed write does not claim publication | A | [C:D25] [I] | Exact draft retention and duplicate-write rules are peer-owned | Retain current boundary; test E04 |
| T06 IF-13/H16: new-session follow-up links prior run/PR and gets new run, invocation and trace IDs | A | [C:issue #180] [I] | Langflow creates run; no existing session in slice | Retain as first-slice request invariant |
| T07 IF-10: partial and complete manifest supersession identity/order/precedence | B | [I] | #168 review found no manifest revision or supersedes field | Choose B01 before schema revision; test E02 |
| T08 H12, #172 H-12: how results discovers external PR/branch effects after crash without IF-10 | B | [I] | Agent execution owns the effect-policy choice in [#175](https://github.com/amadou-6e/specs/issues/175) Q07/Q16 | Consume that choice for B02; do not invent effects |
| T09 H13, #172 H-15: failure-report provenance when no agent final message exists; whether a model summarizer is allowed | B | [C:D25] [I] | Trace completeness and summarizer policy | Choose B03; test E04 without model turns |
| T10 D24/H9: artifact destination, retention, unsaved output and cleanup policy | B | [C:D24] [I] | Isolated checkout lifetime and actual persisted locations | Choose B04; test E03 |
| T11 H12/H16, #172 H-14: who refreshes PR review state for follow-up display | B | [I] | Issue integration owns the choice in [#176](https://github.com/amadou-6e/specs/issues/176) B10; GitHub read authorization | Consume that choice for B05; no silent refresh claim |
| T12 H9/H10: who owns retained artifact-store policy, distinct from later transport of bytes? | B | [I] | Cross-subsystem boundary; multi-stage movement deferred | Choose B06 for retention/store ownership; #175 Q24 covers later materialization |
| T13 GitHub PR review-state read API and credential scope after an owner is selected | R | [U] | B05 must choose refresh owner and desired freshness | Inspect GitHub primary API/auth docs; no current API claim |
| T14 Crash-time IF-09/10/11 assembly and restart view with absent or out-of-order inputs | E | [C:issue #180] [U] | Durable producer handoffs and restart marking | E01 |
| T15 IF-10 partial→complete/replayed or reordered manifests: projection must not double-count | E | [I] [U] | B01 chooses identity and ordering | E02 synthetic replay fixture |
| T16 Artifact path after isolated-checkout crash/cleanup: reachable, unknown or verified lost | E | [I] [U] | B04 and #175 cleanup decision | E03 |
| T17 Failure report without final agent message and failed IF-12 publication retain reviewed draft | E | [C:D25] [U] | B03 and issue-integration retention choice | E04 |
| T18 #172 H-6: inter-stage artifact transport and lineage | D | [C:D04] | Multi-stage graphs outside first slice | Revisit with graph-file handoff experiment; execution owns materialization proposal |
| T19 #172 H-7/H16: existing-session follow-up, selective stage rerun | D | [C:D19] [I] | Single-agent new-session slice only | Revisit after Langflow/session feasibility |
| T20 #172 H-13: multiple stages/PRs and PR ownership | D | [I] | One PR per first-slice run | Revisit with multi-stage policy |
| T21 D25/H13: selected findings as durable project knowledge | D | [C:D25] | Optional after result inspection | Revisit when knowledge destination is selected |
| T22 H12: live PR review-refresh implementation | D | [I] | B05 then R01; not needed to record confirmed creation | Revisit for follow-up UI freshness |

T02 is a **proposed coordinated change**, not a rewrite of Langflow's
unmerged IF-09 contract. T04 does not promise that cleanup preserves bytes.
The first-slice result can display `unknown` for an external effect or
unreachable artifact without silently calling it absent.

## Choices requiring user decision

These are alternatives, not chosen contracts. The first four affect the
first-slice crash result most directly.

| B item | Option | Consequence, failure prevented/caused, cost |
| --- | --- | --- |
| B01 manifest supersession | Stable manifest ID plus monotonic revision and explicit `supersedes` | Deterministic replacement after replay; requires producer persistence and schema migration. |
| B01 | Append-only per-output events with idempotency keys | Avoids whole-manifest replacement; more events/indexing and harder completeness signal. |
| B02 external effects | Consume the canonical [#175 Q07/Q16 write-identity options](https://github.com/amadou-6e/specs/issues/175); results shows only confirmed effects and marks absent IF-10 evidence unknown pending that choice | A surviving journal or authorized reconciliation may reveal more, but neither justifies inventing an unconfirmed PR. This is not a second effect-policy vote. |
| B03 report provenance | Deterministic template from known IF-09/10/11 with explicit missing/unknown fields | Available without agent/model response, low cost; less narrative interpretation. |
| B03 | Optional model-authored synthesis, labeled with model/version and cited evidence refs, plus deterministic fallback | More readable but adds cost, latency and unsupported-claim risk; no model use is authorized by this triage. |
| B04 artifacts | Persist selected outputs before checkout cleanup and retain by explicit policy | Inspectable crash artifacts, storage/cleanup cost and data-scope choices. |
| B04 | Retain only references and report unresolved/lost workspace-only outputs | Lower storage cost; may make crash work impossible to inspect; never call an unverified path saved. |
| B05 PR refresh | Consume the canonical [#176 B10 owner/freshness options](https://github.com/amadou-6e/specs/issues/176); results labels the timestamp/source of the last known review state | A stale or failed read must not appear current. This is not a second PR-refresh owner vote. |
| B06 retained store policy | Results owns inventory/store retention, agent execution materializes checked bytes later, Langflow carries refs | Separates retained record from execution; requires explicit durable store and access policy. |
| B06 | Agent execution owns the durable artifact store; results links verified refs | Fewer storage boundaries but long-term retention becomes coupled to execution lifecycle; separate the later #175 Q24 inter-stage transport choice. |

Ownership proposal, pending B06: prefer results for inventory and store policy,
agent execution for byte materialization and cleanup, Langflow for handoff
references. The later inter-stage transport question is deferred to [#175](https://github.com/amadou-6e/specs/issues/175)
Q24; B06 here concerns the retained artifact store, not a second transport
decision. Reject automatic file transfer by results: IF-10 reports locations,
not a safe transport primitive. B02 and B05 record consumer needs; their
canonical policy choices belong to #175 and #176 respectively. Ownership
proposal, pending B03: prefer a
deterministic results-owned failure report as minimum; a model summarizer is
an optional, separately attributed action, not implicit agent output.

## Source research

**R01** (after B05): inspect the pinned GitHub REST/GraphQL PR endpoints,
authentication and cache/conditional-request behavior. Question: can the
selected owner refresh review/comment state with the intended credential
scope, and what does a failed/stale read mean? Record endpoint/version/access
date, required permission, response fields and rate-limit/error behavior.
Do not infer freshness from D23 or from the PR URL. GitHub is a changing
external source; it was not inspected for this draft.

## Synthetic experiments, not executed

All use no model turns; the prior [pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
used its 4/4 model-turn cap and observed 39 events after **explicit
cancellation**, not a hard crash. Pin code/fixture SHA before execution; use
Langflow 1.12.3 and Codex CLI 0.159.2 only where relevant to comparison,
and record OS, Docker and filesystem versions for E03. Time costs below are
planning estimates, not measured durations.

| Experiment | Question/decision unblocked; hypothesis and falsifier | Minimal procedure and interpretation | Cost |
| --- | --- | --- | --- |
| E01 crash assembly | Can a restart show a conservative result from persisted IF-09/10/11? Supports T14 and fate-shared crash. Hypothesis: only same-run persisted inputs appear; falsifier: invented PR/output or mixed invocation. | Synthetic one-node run; kill at before/after each input persistence; restart, mark run crashed, inspect result/missing flags. A pass supports the chosen persistence design, not automatic reattachment. | Fixture plus ~30–60 min, 0 model turns. |
| E02 manifest replay | Does chosen B01 scheme avoid duplicate/older overwrite? Falsifier: duplicated output or complete manifest replaced by stale partial. | Emit partial, complete, duplicate and reordered synthetic manifests with same run/invocation; inspect inventory after each. Pass validates only that versioned projection. | Fixture plus ~15–30 min, 0 model turns. |
| E03 isolated checkout | What survives #175 crash sweep under B04? Falsifier: UI calls a removed path retrievable or marks a reachable file lost. | Write fixture artifact, kill backend, run chosen sweep, compare path/store probes with displayed saved state; include cleanup failure. | Fixture plus ~30–60 min, 0 model turns. |
| E04 report and issue write | Can report remain evidence-bounded when agent never concludes, and can a reviewed draft survive publication failure? Falsifier: invented work/effects or lost reviewed draft. | Feed incomplete IF-09/10/11, generate deterministic report, simulate failed IF-12 write and restart; inspect provenance and draft. Model option, if selected, needs a separate explicit budget/protocol. | Fixture plus ~20–40 min, 0 model turns. |

Any real GitHub side-effect reconciliation and orphan-process behavior needs a
separate authorized, isolated test; these fixtures cannot prove it.

## Crash behaviour: five required answers

1. **Persist first.** [C:issue #180; I] Run and trace identity plus frozen
   context must be durable before dispatch; the user's #179 answer was to
   refuse dispatch otherwise (recorded in unmerged PR #189). A durable result
   shell and incremental manifest/trace refs are candidates, not proven.
2. **On restart.** [C:issue #180; I] Langflow/Laomedo marks nonterminal runs
   `crashed`; results assembles only surviving inputs and marks missing or
   partial ones. Agent execution owns container/checkout cleanup decisions;
   results does not delete bytes or claim deletion from a missing path.
3. **Orphans.** [I/U] A container or GitHub write may outlive the backend.
   Results cannot discover every effect from IF-10 or trace alone. Warn about
   unknown effects and await B02/#175; do not assert an orphan was stopped.
4. **Relaunch.** [C:issue #180; I] A new linked run and fresh session may
   repeat external work. It never merges evidence into the crashed run;
   acceptability depends on effect reconciliation, not on a prompt alone.
5. **Detection.** [C:issue #180; I] Results need not detect a process crash
   independently. It receives the restart `crashed` state via IF-09; closing
   the UI is not this event (D16). In the first slice, an agent-container
   failure while the backend lives ends the invocation and run as `failed`;
   D17's same-session recovery is deferred. A backend crash instead marks
   the run `crashed`; its invocation-level vocabulary must be aligned with
   [#175](https://github.com/amadou-6e/specs/issues/175), not inferred as an agent failure.

## Claim-to-evidence and review coverage

| Claim group | Evidence at base SHA; limitation |
| --- | --- |
| T01–T06, T14 | [Results contract](../contract/interfaces.md), [IF-09](../../langflow-integration/contract/interfaces.md), [IF-10](../../agent-execution/contract/schemas/if-10-output-manifest.md), [IF-11](../../run-traces/contract/interfaces.md), D24/D25 and issue #180. These are proposed payloads, not tested persistence. |
| T07/T15 | IF-10 has `partial`/`complete` but no revision/supersedes; #168 review flagged supersession. The invariant is draftable; protocol remains B01. |
| T08/T11/T22 | [H12](../../../architecture/subsystem-handoffs.md) shows GitHub→results, while IF-10 carries confirmed PR provenance; #172 review H-12/H-14 raised external effects and refresh. No direct GitHub lookup was proven. |
| T09/T17 | D25 and #172 review H-15 require a failure report even without agent conclusion; neither source proves a summarizer. |
| T10/T16/T18–T21 | D04/D19/D24/D25 and H6/H13/H16 identify intended scope; placement, transport and multiple-PR rules are open. |
| Review exclusions | #172 H-6→T18, H-7→T19, H-12→T08, H-13→T20, H-14→T03/T11, H-15→T09. #168 IF-10 supersession→T07/T15. Other #166/#168 findings concern peer IF-01/07/08 or nested validation; not this results boundary. |

The #172 H-12/14 concern is valid, but the H12 diagram's apparent direct
GitHub→results arrow is not proof of a usable refresh interface. The earlier
pilot and [synthetic projection issue #123](https://github.com/amadou-6e/specs/issues/123)
do not prove hard-crash durability, artifact retention or GitHub effects.
Researcher ran no runtime/vendor tests for this handoff; this writer ran only
the structural/content checks reported with the PR.
