# Laomedo specification structure

Status: draft for [issue #153](https://github.com/amadou-6e/specs/issues/153).
This proposal applies the shared
[typed folder system](../../shared/conventions/typed_folder_system/README.md)
to Laomedo. Its category set and migration map require review before enabling
`categories` in spec.json. Existing pages keep their current authority during
that transition.

## Product definition in progress

Confirmed direction: Laomedo supports designing agent workflows, inspecting
inputs and skills for individual agents, inspecting handoffs, and editing and
rerunning steps. Work Graph adds repository work and dependencies, with agent
execution as the long-term goal. Existing component specs and feasibility reports
contain proposals and bounded evidence; implementation maturity is recorded there.

The first user workflow is still open: workflow design and execution, repository
work execution, or both connected through reusable workflow definitions. Its answer
will determine the first reading path, subsystem boundaries and acceptance scenario.

## Proposed closed category set

| Category | Type | Owned material | Template requirement |
| --- | --- | --- | --- |
| architecture | Fixed | System context, cross-subsystem flows and invariants | Optional template.md; focused pages under one declared system structure |
| subsystems | Folder collection | Stable behavioral boundaries and contracts | One populated template/; initial example below |
| research | Folder collection | Technology investigations and feasibility synthesis | One populated template/ with method, sources and findings |
| experiments | Folder collection | Bounded probes, protocols and execution evidence | One populated template/ separating protocol from iterations |
| decisions | Document collection | Reviewed choices, alternatives and consequences | One populated template.md |
| implementation | Fixed | Source organization, adapter conventions, testing and runbooks | Declare partitions from the actual Laomedo code; no Theseo language stack copied by default |
| views | Folder collection | One independently navigable surface and its owned UI | One populated template/ with ui/design.drawio, matching repository view-owned guidance |
| legacy | Document collection | Retired prose and indexes to retained historical assets | One populated template.md; retained asset-container shape must be declared before migration |

`views` retains Laomedo's existing view-owned convention. Theseo's `ui-design`
template supplies a reference for its content; its path is adapted to
`views/<view>/ui/`. Panels and dialogs belong to the surface that owns them.
Shared shell components remain under the repository-prescribed `ui/shared/`
support area, whose ownership and cardinality must be documented if introduced.

The category set expands only through a revision of this guide. A separate bugs
category can be proposed when durable diagnostic records justify it; GitHub already
tracks implementation work. No empty category tree is required during this draft.

## Root and category cardinalities

The target root owns `1 README.md`, `1 SPECS.md`, `1 spec.json`, `0..1 glossary.md`,
and `1` of each agreed category container. Each category owns `1 README.md`.
Each folder collection owns `1 template/` and `0..* <entry>/`; each document
collection owns `1 template.md` and `0..* <entry>.md`. Fixed categories declare
their own permitted documents and partitions in their README.

Each template is a populated example with `status: template`, resolving links and
its internal cardinalities. New entries are copied directly and renamed; their
metadata and content are replaced. Actual entry status begins at draft until its
requirements and evidence justify another documented state.

The first [subsystem template](subsystems/template/README.md) demonstrates a
small run catalogue. It is illustrative and does not establish a new Laomedo
storage or execution requirement. Other templates are pending the category review.

## Existing material and proposed owners

| Existing material | Proposed destination or ownership | Transition still needed |
| --- | --- | --- |
| components/agent-and-skill-components.md | architecture overview | Reconcile estimates with feasibility/124.md and preserve proposal status |
| components/contracts.md | Shared architecture identities plus owning subsystem interfaces | Assign each record to one behavioral owner before splitting |
| components/codex-agent.md and claude-agent.md | Agent execution contract and provider adapter design | Determine whether provider adapters are extensions under one host |
| components/skill-revision.md and skill-draft.md | Skill registry contract/design | Decide whether draft/promotion shares that boundary or owns a separate subsystem |
| sandboxing/runner-isolation.md | Runner contract; cross-owner invariants link from architecture | Preserve local/remote distinctions and verified limits |
| monitoring/run-traces.md | Run monitoring subsystem | Preserve raw events, projections and incomplete evidence semantics |
| feasibility/118.md through 124.md and docker-skill-draft.md | Research synthesis and experiment records | Classify surveyed evidence separately from model-backed probes and retain original revision links |
| deprecated/ui/ | Historical asset reference | Preserve editable geometry and screenshot links; decide archive support shape |
| Work Graph proposal in PR #152 | Candidate work-management subsystem and Work Graph view | Read the accepted revision before migration; the proposed page is not on main yet |

The Work Graph proposal is tracked in
[PR #152](https://github.com/amadou-6e/specs/pull/152). The migration must account
for its final disposition and update its links if its owning path changes.

## Guided authoring sequence

Use the [define-project-spec skill](../../shared/skills/define-project-spec/SKILL.md)
to clarify one user scenario, propose behavioral owners, review this category map,
then develop one real entry from its populated template. Record answers in their
owning documents and keep unresolved choices explicit. UI states are defined in
reviewed Draw.io before implementation.

After structure agreement, adapt the remaining templates, migrate each source with
a reviewed source-to-owner map, repair links and add manifest categories matching
the resulting structure. Run the specs validator before committing each slice.
