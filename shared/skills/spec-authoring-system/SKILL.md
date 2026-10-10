---
name: spec-authoring-system
description: Establish, migrate, or maintain a project's repeatable specification authoring system with typed categories, ownership, container READMEs, populated templates, evidence lifecycles, and PR spec-impact assessment; and interview a project owner to capture product intent as recorded decisions and owned specifications. Use for project-wide specification organization or authoring workflows, and whenever specs are drafted from conversation with the owner (new project, capability, release scope or user experience), rather than ordinary edits to a single existing spec.
---

# Build and maintain a specification authoring system

Create an authoring system that another contributor can use without relying on
the original author's memory. Its deliverables are a project structure guide,
machine-readable category declarations, structural READMEs, copyable examples,
canonical specifications, and a clear path from proposed behavior to evidence.

For a newcomer or a request to explain the complete workflow, read
[workflow.md](references/workflow.md): it presents ownership, manifest and metadata
schema, lifecycle distinctions, template contents, authoring/review steps and
validation limits in one standalone overview. Use project guides for local details.

## Establish the boundary

Read the repository guidance, project manifest, existing specs, and relevant
implementation/evidence before choosing structure. Determine whether the user
requested a new system, a migration, or maintenance. Preserve an existing
organization unless migration is authorized. Record the inspected revisions
and distinguish current behavior, target contracts, and historical observations.

Use the repository's [typed-folder convention](../../conventions/typed_folder_system/README.md).
The [Anysearch structure guide](../../../projects/theseo-anysearch/SPECS.md)
is a worked reference, not a mandatory category or technology list. Read its
relevant templates when useful; do not inherit Anysearch-specific domain facts.

## Define and instantiate the system

Read [authoring-system.md](references/authoring-system.md) for category and
template requirements. Define a closed project taxonomy in `SPECS.md` and
declare the same categories in `spec.json` using the existing validator's
schema. Choose categories by ownership needs, not by copying every reference
folder. Keep unneeded optional categories and partitions absent.

Create container READMEs with purpose, permitted child shapes, cardinalities,
authority, template usage, and an actual entry index. Populate directly copyable
templates with coherent project-specific examples. Templates have
`status: template`; their example conclusions must not appear as real findings
or accepted decisions. Concrete entries identify their actual maturity and
verification gaps. Links identify canonical owners instead of duplicating rules.

For migration, read [migration.md](references/migration.md). Classify existing
claims before moving files, preserve evidence identities and chronology, and
repair links. Split mixed documents by authority where useful. Keep a mapping
of old locations to new owners; use concise redirects for externally referenced
paths when needed rather than two active copies of the same contract.

## Interview the owner when intent is still forming

When specifications are drafted from conversation with the person who owns the
product intent, read [owner-interview.md](references/owner-interview.md) before
asking the first question. In short: read existing decisions and contracts first
and never re-ask a recorded choice; work on the issue branch; agree the goal,
seed new capabilities from one start-to-finish scenario, and show a question map
in which every question names what it unblocks; write the map and each answer to
the owning decision record as they arrive; ask breadth-first, one marked question
at a time, parking anything that does not serve the goal; checkpoint regularly;
then route confirmed choices to decisions, behavior to contracts and open
investigation to research. Do not let the next question follow only from the
last answer.

## Specification impact on each PR

Read [pr-impact.md](references/pr-impact.md) when establishing or applying PR
policy. Each implementation PR must identify a spec update, an existing contract
that covers its change, or a justified absence of spec impact. Behavioral,
interface, configuration, identity, permission, and failure-semantics changes
require current authoritative coverage. Evidence is linked separately.

Document the policy and propose repository-specific checks when requested.
Writing the skill or policy does not activate CI, branch protection, external
issue edits, or credentials. Apply enforcement configuration only within the
user's authorized scope. Distinguish authored policy, locally validated checks,
and actually active merge requirements in the handoff.

## Editorial pass for workflow diagrams

When authoring a workflow, user journey, or decision tree, read
[diagram-editorial.md](references/diagram-editorial.md). Apply its category,
marking, field, and sizing pass before presenting the first diagram. Use the
worked examples to guide discussion, not to impose Laomedo's categories on
other projects. Preserve confirmed behavior and existing user edits.

## Verify and hand off

Run the existing repository validator and content/link checks. Inspect template
usability by following a copy-and-rename path: does it yield a complete entry
with the right ownership and links, without unexplained placeholders or foreign
project facts? Validation passing is not proof of sufficient content.

Report the taxonomy, canonical reading path, migration mapping, templates to
copy, uncertain claims, checks run, and enforcement state. Follow the local
commit/publish rules while respecting an explicit local-review-only request.

When a user requests a trial or independent application, dispatch an agent with
this skill and the raw project sources. Give it the requested outcome and
authorized mutation boundary without prescribing the expected structure.
Review its actual files for lost claims, duplicate authority, ungrounded
examples, usability, and validation failures. Adapt the skill only to demonstrated
problems. Preserve the trial for user critique and separate that critique from
the agent's own verification.
