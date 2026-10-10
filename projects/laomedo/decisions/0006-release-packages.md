---
title: Release packages and Langflow-first workflow interview
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Release packages and Langflow-first workflow interview

## Status and source

Tracking issue: [specs #336](https://github.com/amadou-6e/specs/issues/336).
Visible checkout branch: `docs/336`. This record reconstructs the owner's
answers and corrections in the current Codex conversation on 2026-10-10.
It is not a verbatim transcript or a contemporaneous record of every answer.
Exact message times are unavailable. The owner first selected planning-only,
then authorized updating the three local drafts, and finally requested full
compliance with the owner-interview skill. That last request authorizes this
recording/publication workflow, not implementation or live acceptance writes.

Exact skill read:
`C:/CodeWorkspace/theseo-anysearch/specs/shared/skills/owner-interview/SKILL.md`.
The earlier interview used the version from fetched specs `origin/main`.
Previously asked settled questions and answers left only in chat are process
failures being repaired, not claimed as retroactively compliant interviewing.

## Context, goal and inventory

Goal agreed by the owner: reviewable release scope for two packages, community
Langflow components and a single-user local Laomedo application. Deliverables:
this decision record, [release overview](../architecture/release-packages.md),
[component plan](../subsystems/langflow-integration/design/community-components.md),
[application design index](../subsystems/work-graph/design/application-experience.md)
and the linked owning contracts. Research and UI implementation are not results
of the interview.

Prefilled sources inspected before further questioning:

- Decisions [0001](0001-issue-to-agent-journey.md) and
  [0002](0002-subsystem-handoffs.md): chat assistance uses the same subsystem
  operations; explicit workflow editing, launch-frozen latest/pinned selectors,
  Langflow sequencing and partial crash evidence were already discussed.
- [0003](0003-agent-event-replay.md): raw deliveries and action uncertainty.
- [0004](0004-mediated-git-gh.md): mediated GitHub access and uncertain writes.
- [0005](0005-active-run-pr-feedback.md): PR delivery while the agent is active
  and bounded feedback; not a general automatic-merge policy.
- Contract, decision-readiness and validation owners in Langflow integration,
  agent execution, Work Graph, issue integration, prompt/skill library, skill
  registry, run traces and results/artifacts. Numeric invocation defaults remain
  unselected; HTTP waiting and the selected orphan bound are different controls.
- Open specs issues/PRs checked on 2026-10-10: no release interview owner existed.
  #336 was created for this repair. Existing experiments, reviews and merged
  code were inventoried as evidence, not substituted for product decisions.
- Laomedo `develop` inspected at
  `6882fc8ea7a90bcaf310fa6c38f8a049789797e5`: Skill/Agent and issue ingestion
  capabilities exist; no Output Contract component was present. No new run used.

## Discussion trail and dated answers

Every row below is an owner answer dated **2026-10-10**. Wording is a faithful
paraphrase unless quoted. IDs are stable question-map references, not API keys.

| ID / question | Latest owner answer | What it unblocks / owner |
| --- | --- | --- |
| P01 Who and where first? | Single-user local application | Local application scope |
| P02 Can workflows be edited? | Yes, through explicit editing, separate from execution/monitoring | Editor versus run-view distinction |
| P03 Which graph reference? | shdennlin/issue-graph as functional inspiration; GitHub Actions as visual inspiration | Reference inventory, not code adoption |
| P04 What is a category? | GitHub labels: research/implementation/fix and UI/backend/data | Assignment inputs |
| P05 Direct versus label assignment? | Direct assignment wins; selectable action-oriented workflow presets, cloning/editing and creation from scratch | Assignment resolution and authoring |
| P06 Multiple matching label defaults? | Alphabetical label priority | Deterministic workflow selection |
| P07 Workflow changes and assigned issues? | Tags like container tags: latest auto-updates; specific version remains pinned; active runs stay frozen | Selector resolution; already covered by 0002 D09 |
| P08 Chat role? | Direct agent chat helps operate Laomedo and create a graph combining existing graphs | Chat-assisted authoring scope |
| M01 Interview map? | Use the five-area map below; initially planning-only | Agreed question sequence and mutation boundary |
| A01 First complete scenario? | Issue → workflow → run → inspect → draft PR | First acceptance journey |
| A02 Distribution gate? | Release independently; pursue upstream inclusion alongside it | Packaging route; upstream acceptance not prerequisite |
| A03 Draft PR automatic or manual? | Create draft PR automatically | Success-path publication; no automatic merge selected |
| A04 Chat-created workflow handoff? | Save a draft; ask before switching screens; then open editor if agreed | Draft creation and consent-based navigation |
| A05 Provider scope? | Codex first; OpenCode follows | Both packages' initial provider matrix |
| A06 Turn/time defaults? | Question challenged; no numeric limit selected. Normal node submits one request, graph loops/continuations supply further requests | Prevents inventing 20/50-turn or 30/60-minute defaults |
| A07 Failure retry scope? | Agent output correction is separate from automatic node/infrastructure recovery | Two mechanisms; infrastructure bounds unresolved |
| A08 Agent-reported failure retry? | Corrected to output-check failure only; reported task failure goes to graph, e.g. reviewer/HITL | Distinct task versus validation outcome |
| A09 Installation? | Docker available plus Codex login; everything else automatic | Automatic runner/component setup requirement |
| A10 Output-check configuration? | User-configurable form, visible to agent for quick correction | Output requirements and feedback |
| A11 Where does Output Contract live? | Separate node for future functionality/configuration | Component boundary, distinct from Skill |
| A12 Correction sequence? | Correct in current request first; then one continuation retry, same session | Configurable default one additional continuation |
| A13 Downstream validation failure? | Agent prechecks form before handoff; downstream contract rejects; conditional routing selects next graph path | Contract → routing, not forced node exception or internal rerun |
| A14 Retain interrupted work? | Preserve changes and partial traces until explicitly deleted | Interrupted-work retention |
| A15 Supported OS first? | Windows first; macOS and Linux follow | Both packages' compatibility scope |
| R01 Next deliverable? | Running Langflow graph showing skills, agent, contract outputs, failures, routing, issue ingestion and actual draft PR creation | Integrated demonstration acceptance |
| R02 Implementation priority? | Complete only the Langflow-related Work Graph implementation first | Parks standalone board/chat UI and distribution implementation |
| R03 Build new issue ingestion? | Owner questioned whether this already exists; implementation inventory confirms existing capability. Reuse/composition is the author's resulting implementation recommendation, not a separately answered product vote | Composition work, not duplicate ingestion implementation |

Corrections preserved: the owner's initial inclusion of agent-reported failures
in retry triggers was explicitly withdrawn. Automatic infrastructure recovery
was desired, not prohibited, but its bounds and safe resume behavior were not
selected. Output Contract became a downstream node, replacing the interviewer's
earlier suggestion to put validation entirely on the agent. The repeated
latest-publication question was withdrawn; no new separate tag-confirmation
ceremony was selected. Saving a draft still does not publish it.

## Decision and scope

Use the latest answers above. Observable rules belong to the linked contracts,
not a second set of requirements in these interview notes. All owners remain
draft until reviewed. Existing isolation, grant scope, cancellation evidence,
uncertain-write fences and historical negative results are retained.

- [Application execution and demonstration](../subsystems/work-graph/contract/application-execution.md).
- [Output Contract and agent precheck](../subsystems/agent-execution/contract/output-contract.md).
- [Community distribution and automatic setup](../subsystems/langflow-integration/contract/community-distribution.md).
- Interrupted-work retention: results/artifacts and run-trace interfaces.

## Consequences and verification

Automatic setup removes manual service assembly from user acceptance. A
downstream contract lets graph routing distinguish valid task failure from
malformed output. Retain-until-deleted consumes storage; disk pressure and
deletion need visible handling. Codex/Windows first reduces the initial matrix.
No evidence in this record establishes installers, validators, graph routing,
agent precheck tools or safe infrastructure recovery as implemented.

## Open questions and agreed map

The owner selected this breadth-first map. Completed questions must not be
asked again unless new scope genuinely challenges the answer. Before each
question, read this record and its owning sources. New answers must be appended
on the issue branch immediately, then reconciled to the owning documents.

| Area | Prefilled/completed | Open work and what it unblocks |
| --- | --- | --- |
| 1. Scenario/users | [x] P01, A01, R01/R02 | [ ] Reviewed graph controls/transitions; unblocks UI implementation, not current product elicitation |
| 2. Distribution/setup | [x] A02, A09, A15, A05 | [ ] Format/service lifecycle, compatibility/license research and maintenance ownership; unblocks distributable package |
| 3. Execution/results | [x] P04-P07, A03, A07/A08, A10-A14 | [ ] Check/schema/feedback design and grant-safe PR publication after downstream validation; unblocks integrated Langflow acceptance |
| 4. Chat/authoring | [x] P02/P05/P08, A04; prior D05/D22 prefilled | [ ] Detailed action/context scope and draft storage; unblocks later chat integration |
| 5. Recovery/acceptance | [x] A06 limits distinction, A07 recovery separation, A14 retention | [ ] Infrastructure retry bounds, uncertain-effect reconciliation, deadline defaults and disk-pressure handling; unblocks safe recovery/operations |

The next product question, if this interview resumes, concerns infrastructure
recovery when an earlier external effect is uncertain. It must explain what
policy choice remains beyond existing no-blind-resend rules. Schema/transport
mechanics are engineering work and should not be sent back as owner questions.

### Parked by the implementation redirection

Standalone Laomedo issue-board/chat UI implementation; component distribution
implementation/outreach; OpenCode release acceptance; macOS/Linux support;
multi-user/hosted operation; arbitrary workflow cycles. Keep them in the release
roadmap, not in the immediate Langflow-only demonstration's acceptance gate.

### Compatibility questions, not silently superseded

- 0005 delivers while the stage is alive; the desired demo publishes after
  validation. Define a trusted active handoff or a separately scoped publisher
  capability before implementing that route. Do not extend a completed agent's
  revoked grant or change Results into a PR publisher by implication.
- D17 automatic recovery remains deferred/unverified. A07 renews the desired
  automatic infrastructure-retry direction without selecting three attempts,
  live restart semantics or a waiver of the existing crash contract.
- No external write/model-turn budget was granted by this specification repair.

The retrospective recording repair cannot undo repeated questions or recover
missing timestamps. It establishes the durable source for subsequent interview
turns. No prior decision entry is marked superseded wholesale.
