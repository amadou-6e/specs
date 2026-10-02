# Skill Draft component

Status: proposed. This component asks Codex or Claude Code to edit a skill in
an isolated draft workspace and returns a reviewable proposal. It does not
promote the proposal automatically. Its UI needs a view-owned Draw.io spec.

Implementation status: core draft storage/validation is reviewable in
[Laomedo PR #5](https://github.com/amadou-6e/laomedo/pull/5), with native and
Docker edit evidence in [#122](../feasibility/122.md) and the
[Docker study](../feasibility/docker-skill-draft.md). The
[2026-10-01 Langflow pilot](../implementation/local-skill-agent-pilot.md)
tests skill consumption and workspace writes, not this full edit/promotion
component or a Langflow skill-edit node.

## Input and output

Required inputs are a base `SkillSnapshotRef`, an `EditPolicyRef`, an edit
request, a selected Codex or Claude adapter and model/effort settings, and
fixed evaluation cases if requested. Output is `SkillDraftResult` from
[shared contracts](contracts.md): draft revision and tree hash, changed paths,
patch, edit run and trace IDs, validation results, evaluation results, and
promotion eligibility. Even a failed edit returns available trace and diff.

## Editing rules

Editing rules are a separate versioned policy, never just prose appended to
the consumer skill. The policy states at least:

- allowed and forbidden paths and file types;
- whether new files, scripts, dependencies, and assets may be added;
- required frontmatter, rule/example format, and invariants;
- permitted validation commands and evaluation cases;
- limits and permission scope for the editing agent.

Record the exact policy revision and hash on the draft. A policy can constrain
an edit but cannot grant powers beyond the runner's permission boundary. A
natural-language instruction alone is not sufficient to enforce path limits.

## Lifecycle

1. Copy the pinned base bundle to a fresh draft worktree. Check the worktree
   path is confined to the runner's draft root.
2. Materialize the policy and edit request. Start the chosen agent with write
   access only to the draft worktree and declared validation dependencies.
3. Capture every observed file change and the agent trace. Reject or quarantine
   paths outside the policy, symlinks that escape the draft, and unsupported
   file types. Do not copy such changes to the proposed revision.
4. Run deterministic structural validation, then optional fixed-case
   evaluations against both base and draft. Link all runs and record inputs,
   outputs, and comparison method.
5. Freeze the proposed bundle and return its patch and results. Promotion to
   the canonical skill is a separate action with a reviewed diff and conflict
   check against the current base.

If the edit times out, crashes, or violates policy, preserve the partial trace
and quarantined draft evidence, mark it ineligible for promotion, and leave the
base untouched. A later retry creates a new draft and run ID.

## Acceptance

- The original skill tree hash remains unchanged after success and failure.
- An edit to an allowed rule yields a distinct draft hash, patch, and complete
  policy and agent provenance.
- A forbidden path change is rejected even if the agent claims it is allowed.
- A concurrent canonical update cannot be overwritten by promoting a draft
  based on an older revision.
- Evaluation results distinguish deterministic validation from model-based
  quality judgments. A passing evaluation is not a guarantee of identical
  future behavior.
