# Agent guidance

This repository contains specifications, not product implementation. Prefer changes
that make intent, behavior, constraints, and verification clearer.

## Reference map and skills

- [README.md](README.md): repository layout, project scaffolding, and validation commands.
- [Specification lifecycle](shared/conventions/spec_lifecycle.md): maturity, acceptance,
  and review requirements.
- [Typed folder convention](shared/conventions/typed_folder_system/README.md): structural
  types and template expansion; each project's `SPECS.md` chooses its taxonomy.
- [Spec authoring system](shared/skills/spec-authoring-system/SKILL.md): establish,
  migrate, or maintain project structure, ownership, READMEs, templates, and evidence.
  Use for system-level authoring work, not every single-file correction.
- [Owner interview](shared/skills/owner-interview/SKILL.md): interview a project owner
  to capture product intent as recorded decisions and owned specifications, with a
  goal-anchored question map and answers persisted as they arrive.
- [Research](shared/skills/research/SKILL.md): separate research and writing with an
  inspectable evidence handoff when that workflow is selected. Read applicable
  project/category guidance too; this skill does not own every project's research schema.
- [Create spec-linked PR](shared/skills/create-spec-linked-pr/SKILL.md): prepare or update
  PR coverage, acceptance checklists, verification, and blocker follow-up links.
  Start from its [PR body template](shared/skills/create-spec-linked-pr/assets/pr-body.md)
  and retain applicable sections from the repository's existing PR template.
- [Claude reviewer](shared/skills/claude-reviewer/SKILL.md): request an independent,
  read-only Claude Code review directly. Its reviewer session follows the current
  Codex conversation and reuses the existing subscription login.

Read the relevant skill before applying it. Skills guide authorized work; they do not
authorize implementing open proposals, changing issue state, or activating repository
settings. Follow the affected project's manifest, `SPECS.md`, category README, and
nearby guidance for its concrete structure and canonical owners.

## Approval boundaries

- Ask for explicit approval before editing an existing GitHub issue's title, body,
  labels, or state. Present the proposed changes first and preserve newer edits.
- Treat open issues as proposals. Implement only work selected by the user; a roadmap
  or a request to analyze the backlog is not authorization to implement it.
- Do not silently apply configuration changes. Present drafts and obtain approval
  before changing workflows, repository settings, or required merge checks.
- For user-selected work, an independent review of the PR's substantive change
  through the linked Claude reviewer skill or the requesting human's review
  authorizes merging without another permission request when `git diff --check`
  and every configured CI check on the final head pass. Re-review when the PR's
  own diff changes meaningfully, including logic changes; allow one focused
  recheck per blocking finding. For nonblocking wording or BOM/encoding fixes in
  non-executable documents, and clean parent merges with an unchanged own-diff
  and no new interaction risk, use deterministic diff checks and CI instead of
  another reviewer turn. Parser/tests remain required for executable encoding
  changes. A blocking finding is resolved
  only by reviewer recheck or a human decision. If a recommendation conflicts
  with the human's interests or instructions, pause the merge and ask them to
  decide. Do not merge with an unresolved blocker, failed check, or unmet stack
  dependency. This rule does not authorize issue edits, configuration changes,
  maturity changes, or user experience decisions. Do not describe an independent
  review or self-merge as human approval.

## Working rules

- Do specification work in this repository's visible top-level local checkout
  (`specs/` when embedded in a project workspace), never in an auxiliary specs
  worktree. Keep draft files at their canonical paths so the user can inspect
  them in the workspace. Before changing branches, inspect the checkout and
  preserve existing edits; if it cannot be switched safely, stop and ask the
  user rather than moving or overwriting their work.
- Read the project manifest and nearby specifications before editing.
- Preserve project-specific organization unless a migration is explicitly requested.
- Do not overwrite user-authored Draw.io changes. Inspect the current Git diff before
  editing and use branches and commits for design history; do not create backup copies.
- Keep reference screenshots beside their Draw.io workshop when they are used for
  fidelity comparison.
- Keep view-specific components under `projects/<slug>/views/<view>/ui/components/`.
  Use `projects/<slug>/ui/shared/` only for components with no single view owner.
- Keep live screenshots in `references/` and superseded multi-view studies in
  `ui/archive/`. Do not track Draw.io exports; generate them temporarily for visual
  inspection and discard them after review.
- Use editable geometry for UI proposals; screenshots are references, not substitutes.
- Treat each view's Draw.io as the sole authority for UI geometry, component states,
  interaction IDs, and transitions. Markdown, screenshots, and test plans are derived
  indexes or evidence and must not introduce behavior absent from the Draw.io.
- When an implementation issue needs a new UI control, state, or transition, update and
  review the owning Draw.io before implementation or in a stacked specification PR.
- Visually inspect Draw.io changes at component level and at full-page scale.
- Record unresolved decisions explicitly instead of inventing product behavior.
- Never add credentials, browser profiles, cookies, tokens, or captured login URLs.
- Do not vendor generated caches, virtual environments, model weights, dependency
  trees, or cloned upstream repositories.
- Run `python tools/validate_specs.py` before committing.
- Treat this repository as the system of record for specifications. Completed changes
  to specifications and their evidence must be committed on the issue branch and
  pushed to this repository; do not leave specification work only in an ignored
  checkout or in an implementation repository.

## Change workflow

Problem or feedback -> specification issue -> typed issue branch -> spec and evidence
-> validation -> pull request -> review -> merge.

Use `<type>/<issue-number>` branches, for example `feat/12`, `fix/18`, `docs/21`, or
`chore/24`. Pull requests should link the issue and identify the specifications whose
status or behavior changed.

1. Inspect Git status and the intended base before editing. Preserve unrelated work;
   use an issue branch in the visible checkout, or ask for direction if concurrent
   work prevents a safe switch.
2. Read the owning project/category guidance and accepted coverage. For new projects,
   use `tools/new_project.py` as described in the README. For new entries, copy the
   owning category's template; do not invent a parallel structure.
3. Write observable behavior, scope, failure conditions, and acceptance criteria.
   Keep authoritative contracts separate from historical evidence and illustrative
   templates. Record source revisions, actual checks, and unknowns honestly.
4. When moving files, inspect local and published consumers, preserve necessary
   compatibility pointers, and repair indexes and links. Never silently discard evidence.
5. Run `python tools/validate_specs.py` and `git diff --check`, then inspect content,
   references, and changed artifacts. Documentation-only changes need content/link
   checks, not a product rebuild. Changes to tools need relevant existing tests too.
   Validate changed skills using the skill-creator validator when available; disclose
   unavailable checks. Passing structural validation does not prove runtime behavior.
6. Commit and push completed work on the selected issue branch. Use
   [create-spec-linked-pr](shared/skills/create-spec-linked-pr/SKILL.md) whenever
   creating or substantively updating a PR, including a fix or documentation PR.
   Read the skill, derive the acceptance checklist from governing specifications,
   record verification and definitive blockers with follow-up issue links, and
   prepare the body using its template and the repository template.
   State the actual head/base and stack dependencies; do not conflate a reviewed
   branch with merged coverage.
7. Address review feedback, rerun checks affected by the changes, and update the
   PR to describe the final result. Follow the linked reviewer skill's bounded
   re-review rule; record the reviewed revision and deterministic checks for any
   later non-substantive edits or clean parent merges. Merge after final-head
   checks pass and no blocking finding or human-interest conflict remains. Issue
   closure still requires explicit approval under the rules above.

## PR requirements

The PR creation skill is the reusable procedure for these requirements. Keep
procedural changes in that skill and project-specific rules in the owning project
policy; update these links and requirements when either changes. Do not maintain
a competing copy of the full skill workflow here.

Every PR, including fixes, includes:

- Links to its issue, canonical spec sections and inspected revisions, and relevant
  specification PRs. Follow project-specific spec-link exemptions and merge order;
  Laomedo's non-`fix/` link rule is in its
  [PR policy](projects/laomedo/implementation/spec-impact.md), not a universal branch rule.
- A checklist derived from applicable specification or authoring acceptance criteria.
  Check only verified outcomes, with evidence; explain failed, untested, inconclusive,
  or inapplicable items. Generic lint/build checkboxes are not a substitute.
- Commands/results and the tested revision, with limits on what those results establish.
- Definitive unresolved blockers, their evidence and merge impact, and follow-up issue
  links. Create a new issue when authorized or link an existing issue that owns the
  same problem. If a required issue link cannot be supplied, report that requirement
  as incomplete. Record recovered failures separately; say `None observed` when there
  are no definitive blockers, while retaining any verification gaps.

A follow-up issue does not waive an unmet acceptance criterion. Missing criteria are
gaps, not permission to invent approved requirements. Never publish credentials or
private raw transcripts as evidence.

The existing GitHub workflow runs the specs validator. These instructions and skills
do not activate automatic spec-link, checklist, blocker, or semantic coverage gates.
Required-check configuration needs its own tested proposal and approval.
