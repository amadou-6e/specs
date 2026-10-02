---
title: Skill registry decision readiness
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill registry decision readiness

This is triage for [issue #178](https://github.com/amadou-6e/specs/issues/178), not acceptance of the target contracts. The inspected specification base is [`3974d9aa1f380c72105e7f205f16e3eeae2c8d80`](https://github.com/amadou-6e/specs/tree/3974d9aa1f380c72105e7f205f16e3eeae2c8d80), inspected 2026-10-02. Evidence is the [2026-10-01 pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md) (Laomedo `5e14c7a`, Langflow `1.12.3`, Codex CLI `0.159.2`) and the [runner feasibility sources](../../../research/runner-feasibility/sources/README.md). The pilot spent its full **4/4 model-turn cap**. It observed one whole skill, no dependency-bearing selection or promoted draft. No current vendor documentation, live Laomedo implementation, private raw traces, or actual registry-crash test was inspected for this triage. Existing target text and review comments are not runtime evidence.

The first slice is one agent in a one-node Langflow workflow, a direct prompt or selected issue, an isolated checkout and fresh session, launch-frozen latest/pinned selectors, one PR, trace inspection, and a reviewed failure issue. A fate-shared Langflow/Laomedo backend crash ends the run as `crashed`; a later launch is a **new linked run**, not graph recovery. UI closure is different. The merged [decision record D17](../../../decisions/0002-subsystem-handoffs.md#execution-recovery-and-inspection) now explicitly defers agent-*container* recovery from the first slice pending a real mid-turn restart experiment.

Tags: **[C]** confirmed decision (with D-ID), **[O]** bounded observation, **[I]** inference or controllable design, **[U]** unverified third-party behavior. A question has exactly one class: **A** decide now, **B** user decision, **R** source research, **E** pinned experiment, or **D** safely defer. The next action is a proposal, not a claim that it ran.

## Triage

| Question | Class | Tags | Blocking dependency | Next action |
| --- | --- | --- | --- | --- |
| A2. IF-04 effective-workspace hash ordering | A | [O] pilot; [I] contract rule | B7 determines the location and therefore the effective-workspace **hash definition** | Ordering alone is draftable now: compute after complete hash-validated materialization and before agent dispatch. Define whether mounted external skill bytes or their immutable ref enter the effective hash only after B7; keep source/post-run hashes distinct. |
| A3. IF-04 direction and fail-before-dispatch code categories | A | [I] from [interface map](../../README.md) and [IF-04 schema](../../agent-execution/contract/schemas/if-04-skill-materialization.md) | None; transport encoding remains open | Registry provides bytes/result; agent execution requests. Propose stable categories for unknown/invalid revision, missing dependency, hash mismatch, and unsafe path; never return an empty successful bundle. |
| A4. IF-03 `latest`/pinned lookup identity | A | [C] D09; [I] from [shared ref](../../../architecture/shared-contracts.md) | GitHub-backed identity is R1, not needed for native first slice | Resolve once at launch and return exact revision plus tree/file hashes; execution never follows a moving alias. |
| A5. IF-03 unknown/invalid revision | A | [I] [IF-03 contract](../contract/interfaces.md) | None | Return a coded error without fallback to another revision. |
| A6. Native content-addressed read integrity | A | [O] whole-bundle pilot; [I] storage rule | [#175 S13/E04](https://github.com/amadou-6e/specs/issues/175) must check Windows line-ending transformations | Verify immutable tree/file bytes against the selected reference on each lookup/materialization; reject mismatch rather than normalizing bytes silently. |
| A7. Publishing a native revision pointer | A | [I] controllable design | E2 must verify crash behavior | Write candidate bytes, verify hashes, then publish the pointer; never present a candidate as current until verification completes. This is a design rule, not an observed crash guarantee. |
| B1. Interrupted IF-04 materialization and checkout retention | B | [I]; [U] crash behavior | Agent execution's isolated-checkout sweep/retention choice (#175) | Decide between discard-on-crash and atomic temp-tree publication; then test E1. |
| B2. Stale `pending` IF-14 drafts after backend death | B | [I] from [draft lifecycle](../contract/drafts.md) | Restart-sweep owner with #174/#175 | Choose which owner marks or reconciles incomplete draft records; never imply current pilot did it. |
| B3. Prompt revision storage relative to registry | B | [I] from [library boundary](../../prompt-skill-library/contract/interfaces.md) | #177 owns prompt-library side | Choose shared store/index or separate stores; registry does not silently acquire prompt semantics. |
| B4. Canonical promotion authorization | B | [C] D06; [I] draft contract | User policy; #177 owns publication channel | Choose review gate, scoped automatic promotion, or GitHub merge as canonical. Keep immutable draft and canonical revision separate in every option. |
| B5. Agent-authored IF-14 drafts and approval | B | [C] D20/D22 contested; [I] | Shared approval policy, #177 edit entry | Decide whether draft creation, promotion, or both need an explicit user grant. No agent edit silently promotes. |
| B6. A linked relaunch after `crashed`: old ref or moved `latest` | B | [C] D09 for original launch; [I] for *new* run | #177 selector policy and #174 launch owner | Select old exact refs, new latest resolution, or explicit user choice; do not misapply “frozen including recovery” to a different run. |
| B7. IF-04 full-skill destination without polluting or blocking git | B | [O] pilot used `.agents/skills/<skill_id>`; [I] location trade-off | [#175 S08/E04](https://github.com/amadou-6e/specs/issues/175) found git-clean and read-only-file hazards | Choose ignored in-checkout path or private provider-discoverable mount; do not make the pilot path a first-slice default. |
| R1. GitHub-backed skill revision identity | R | [U] GitHub semantics | D06 and #177 backend design | Inspect primary Git/GitHub documentation and implementation: commit SHA + path versus tree/content hash, and which is the stable runtime ref. |
| R2. Pinned GitHub revision after force-push or deletion | R | [U] GitHub retention behavior | R1 | Inspect primary Git/GitHub docs, retention/garbage-collection rules, and API responses; define a cache/availability policy only after that. |
| E1. Registry materialization interrupted before IF-04 completion | E | [U] crash timing | B1; pinned fixture required | Run a no-model process-kill fixture during file/rename phases and test no partial tree reaches dispatch. |
| E2. Native revision write interrupted before pointer publication | E | [U] filesystem crash timing | A7; pinned fixture required | Run a no-model process-kill fixture around byte write, flush, hash/index publication and restart; readers should see old or complete new revision only. |
| D1. General dependency closure | D | [I] first-slice scope; [O] pilot lacks dependencies | First slice must reject dependency-bearing skills | Revisit when the first real selected skill declares dependencies; no A item assumes closure is already implemented. |
| D2. Isolated rule/example item IDs and subsets | D | [O] [#119](../../../research/runner-feasibility/sources/119.md) examined item identity; [I] slice | First slice offers whole bundles only | Revisit for item selection or few-shot UI; do not describe whole-skill pilot as subset proof. |

Counts: **A 6 / B 7 / R 2 / E 2 / D 2**. IF-03 is A4–A6 and R1–R2; IF-04 is A2–A3, B1/B7, E1, and D1–D2; IF-14 is B2/B4/B5 and E2. IF-14 draft provenance itself remains required by the [draft contract](../contract/drafts.md): base, policy, actor/edit-run and candidate identity must not be lost. No row converts an existing proposal into a validated implementation.

## User decisions

These options require user selection; none is silently adopted. Where a peer owns the resulting contract, this registry page will link that decision.

| Item | Option | Consequence and failure prevented/caused | Cost |
| --- | --- | --- | --- |
| B1 | Discard the isolated checkout on backend crash | A half-written IF-04 tree cannot be relaunched from that checkout; cleanup must be reliably owned by agent execution. | Low registry complexity; retained forensic workspace unavailable. |
| B1 | Temp directory, validate, then publish/rename | Retained checkout cannot expose a partial skill under the canonical path; cross-platform rename/crash behavior still needs E1. | More disk and filesystem protocol complexity. |
| B2 | Registry startup reconciles pending drafts | Registry can mark orphan drafts failed/ineligible from its own journal; avoids eternal pending records. | Requires durable operation markers and restart scan. |
| B2 | Agent execution emits a terminal edit outcome | Uses execution ownership; a fate-shared backend death may prevent this event and leave stale pending drafts. | Less registry logic but needs a restart fallback. |
| B2 | Leave pending, mark ineligible on read | Avoids a sweep but users can see indefinite pending state; must distinguish ineligible from a live edit. | Cheapest write path, weaker inspection clarity. |
| B3 | Use the canonical [#177 B06 prompt-store options](https://github.com/amadou-6e/specs/issues/177); registry supplies skill bytes/index only until that choice is made | Shared machinery may reduce duplication but can contaminate skill-only validation; separate storage retains clear authority at higher operations cost. | No independent registry vote; schema migration follows #177. |
| B4 | Human review before every canonical promotion | Stops unreviewed draft from becoming active; adds queue/latency. | Reviewer time. |
| B4 | Scoped auto-promotion under explicit grant | Faster iteration; a mistaken policy or check can publish bad content. | Grant/audit controls and rollback design. |
| B4 | GitHub merge defines canonical revision | Leverages PR review; native backend needs reconciliation and offline handling. | GitHub dependency and sync logic. |
| B5 | Allow agent draft creation, always gate promotion | Preserves useful agent edits while keeping active skill safe; unchecked drafts may accumulate. | Draft quota/cleanup and review queue. |
| B5 | Gate draft creation and promotion | Limits storage and untrusted edits; interrupts unattended curation. | Approval latency. |
| B5 | Grant-scoped direct canonical edit | Fastest, but risks bypassing the draft/promotion boundary unless rewritten as two explicit operations. | Highest policy and audit burden. |
| B6 | Use the canonical [#174 B20 relaunch-selector options](https://github.com/amadou-6e/specs/issues/174); registry resolves the exact ref requested | Prior bytes improve reproducibility but may be obsolete; moved `latest` changes inputs; explicit choice adds interaction cost. | No independent registry vote; every new run records the chosen exact bytes. |
| B7 | Ignored path inside the checkout, with protected/verified skill bytes | Native discovery may work, but read-only files can block git cleanup and ignored files still need safe removal. | Git-safety tests and mount/write isolation. |
| B7 | Private provider-discoverable mount outside the checkout | Avoids accidental `git add -A` and git-clean conflicts, but provider discovery and path binding must be verified. | Per-provider adapter and mount setup. |

Priority for the first slice: **B7** (materialization location) and **B1** (checkout cleanup/retention), then **B6** only if linked relaunch is exposed. B7 is the registry-side requirement; #175 S08 owns stage git cleanliness and provider discovery testing. The canonical prompt-storage choice B3 belongs to [#177](https://github.com/amadou-6e/specs/issues/177); the canonical linked-relaunch selector B6 belongs to [#174](https://github.com/amadou-6e/specs/issues/174). These rows record dependencies, not independent votes. B2 matters if IF-14 drafts run in the slice. B4–B5 concern later curation/promotion unless a first-slice selected skill must be edited or published.

## Research handoffs

Neither result is assumed from an uninspected upstream source.

- **R1 — GitHub identity.** Search primary Git object model and GitHub repository/API documentation at the revision or access date used by the follow-up researcher. Inspect how a path at a commit is addressed, what a tree hash protects, and whether one reference alone preserves all dependency bytes. Record docs/source location, version/date, applicability to private/public repos, counterevidence, and a candidate IF-03 ref shape. A web search result is not evidence until its underlying source is inspected.
- **R2 — rewritten-history availability.** Inspect primary Git/GitHub docs for force-pushed commit reachability, API fetch after branch deletion, garbage collection and retention caveats. Distinguish “not guaranteed retrievable” from a measured time-to-loss. Return a reproducible source ledger and options for local content-addressed cache, publish-time copy, or fail-visible lookup. Do not infer immutable availability merely from a SHA.

## Experiment sketches

Both are proposed, not executed. Each uses a synthetic whole-skill fixture and **zero model turns**; the pilot's 4/4 allowance cannot be reused.

| Experiment | Hypothesis / falsifier | Pins and minimal procedure | Outcome for contract; estimated cost |
| --- | --- | --- | --- |
| E1 — interrupted IF-04, unblocks B1 | No half-written canonical skill tree is ever offered to dispatch. Falsified by a partial tree under the selected path or an agent invocation using it. | Pin Laomedo fixture commit, OS/filesystem, Python/runtime, one content-addressed skill hash, and chosen B1 algorithm. Inject process kill after each file write and just before/after rename; restart, inspect checkout and IF-04 outcome; repeat at least once per cut point. No Langflow or model call required. | If discard works, contract may rely on owner-confirmed sweep; if temp publication works, specify atomic materialization for the tested FS; otherwise revise. Approx. 10–30 minutes **after fixture exists**, fixture authoring extra. |
| E2 — interrupted native registry write, tests A7 | Readers see old published revision or complete hash-valid new revision, never a torn new pointer. Falsified by a visible pointer whose bytes fail verification or lost old revision. | Pin registry fixture commit, OS/filesystem, durability settings, candidate bytes/hash and index implementation. Inject process kill during byte write, flush/fsync, hash verification and pointer publication; restart and query both pinned and latest. No agent/model call. | Passing bounded tests support the chosen write protocol on that FS, not all crash modes. Failure requires revised publication/durability rule before claiming safety. Approx. 10–30 minutes **after fixture exists**, fixture authoring extra. |

## Crash behaviour

1. **Persisted before return.** A successful IF-03/IF-04 return must identify exact revision, tree/file hashes and provenance; an IF-14 receipt must identify its base, edit policy, actor/edit run and draft state. The first-slice run record must retain the selected refs before dispatch ([D09 and shared records](../../../architecture/shared-contracts.md)). This is a target invariant; the pilot did not test backend-death durability.
2. **Restart handling.** Fate-shared backend death makes Langflow/Laomedo mark active runs `crashed`. Registry startup must not publish incomplete bytes; whether it reconciles pending IF-14 drafts is **B2**. Agent execution owns checkout/container cleanup (**B1**), not the skill registry. No graph reattach or same-run redispatch is specified.
3. **Orphans.** A native write may be interrupted; E2 covers the index/byte boundary. An agent edit container could outlive the backend unless #175 enforces cleanup. GitHub publication may continue or finish externally and belongs to #177's policy; registry must not infer publication solely from a local proposal.
4. **Relaunch duplicates.** A linked new run may materialize the same exact bytes again, which is harmless if hashes verify. Following moved `latest` may produce different bytes: **B6**, not automatic crash recovery. A repeated IF-14 draft needs a new draft/edit-run identity and must not silently promote twice.
5. **Detection.** The registry need not detect the moment of backend death. On restart it can detect incomplete local operations from durable records and reject/clean them; B2 chooses draft reconciliation. Run terminalization belongs to the Langflow/Laomedo launch boundary, not this registry.

## Review findings and ownership

The #168 minor IF-04 direction finding is now addressed in the merged [agent-execution interface](../../agent-execution/contract/interfaces.md#if-04--obtain-exact-skill-bytes): execution requests and registry provides bytes. A3 still calls for error-category verification. #168 B1/B2/M1/M2 concern launch trigger, event deduplication, file inputs and retry identity; none is a registry guarantee. #172 H-1's reattachment remedy is superseded by the fate-shared crash decision, but its orphan/duplicate risk remains in B1/B2/B6 and the crash answers. #172 H-10 concerns launch caller, H-12 external PR delivery: peers own them. The inspected #166 review supplied no registry-specific blocker. Reviews are hypotheses, not accepted contracts.

The merged decision record already covers fate-shared crash and D17 deferral; no new D-ID is needed for that correction. Before implementation, resolve B7 and B1 and run the bounded materialization/crash tests. Do not infer acceptance of any unmerged sibling readiness PR.
