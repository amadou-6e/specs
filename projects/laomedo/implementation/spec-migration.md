---
title: Specification migration record
status: complete
kind: migration-record
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Specification ownership migration

Local trial prepared and agent-checked 2026-10-01; user review requested compatibility fixes; revised acceptance pending. Source specs revision 2854612a32a40b6b455734cd2d758f92f86f1897.
Historical implementation/evidence identities and observations remain unchanged.

| Original path | Canonical owner |
| --- | --- |
| `capabilities/work-graph.md` | [subsystems/work-graph/contract/work-graph.md](../subsystems/work-graph/contract/work-graph.md) |
| `components/agent-and-skill-components.md` | [architecture/component-proposal.md](../architecture/component-proposal.md) |
| `components/contracts.md` | [architecture/shared-contracts.md](../architecture/shared-contracts.md) |
| `components/codex-agent.md` | [subsystems/agent-execution/contract/codex.md](../subsystems/agent-execution/contract/codex.md) |
| `components/claude-agent.md` | [subsystems/agent-execution/contract/claude.md](../subsystems/agent-execution/contract/claude.md) |
| `sandboxing/runner-isolation.md` | [subsystems/agent-execution/contract/isolation.md](../subsystems/agent-execution/contract/isolation.md) |
| `components/skill-revision.md` | [subsystems/skill-registry/contract/revisions.md](../subsystems/skill-registry/contract/revisions.md) |
| `components/skill-draft.md` | [subsystems/skill-registry/contract/drafts.md](../subsystems/skill-registry/contract/drafts.md) |
| `monitoring/run-traces.md` | [subsystems/run-traces/contract/README.md](../subsystems/run-traces/contract/README.md) |
| `implementation/local-skill-agent-pilot.md` | [experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md](../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md) |
| `feasibility/118.md` | [research/runner-feasibility/sources/118.md](../research/runner-feasibility/sources/118.md) |
| `feasibility/119.md` | [research/runner-feasibility/sources/119.md](../research/runner-feasibility/sources/119.md) |
| `feasibility/120.md` | [research/runner-feasibility/sources/120.md](../research/runner-feasibility/sources/120.md) |
| `feasibility/121.md` | [research/runner-feasibility/sources/121.md](../research/runner-feasibility/sources/121.md) |
| `feasibility/122.md` | [research/runner-feasibility/sources/122.md](../research/runner-feasibility/sources/122.md) |
| `feasibility/123.md` | [research/runner-feasibility/sources/123.md](../research/runner-feasibility/sources/123.md) |
| `feasibility/124.md` | [research/runner-feasibility/sources/124.md](../research/runner-feasibility/sources/124.md) |
| `feasibility/docker-skill-draft.md` | [research/runner-feasibility/sources/docker-skill-draft.md](../research/runner-feasibility/sources/docker-skill-draft.md) |

All original report and contract bodies are preserved, with metadata and repaired links.
The mixed component proposal retains historical planning estimates and open choices.
Feasibility reports are source records, not accepted decisions. The original pilot report
is the sole result authority; added protocol/execution pages are retrospective reconstruction.
At the original migration, every old path in the table retained a short
compatibility pointer. Full bodies exist only at their canonical destinations.
The local Markdown inventory was insufficient: published issue and PR
references also depended on old paths. The later [#169 cleanup](#retirement-of-two-pointer-folders)
removes only `sandboxing/` and `monitoring/`; the three remaining compatibility
containers (`capabilities/`, `components/` and `feasibility/`) still own closed
pointer sets, not active contracts.
The deprecated UI path and binary artifacts remain unchanged.

The original migration created no new experiment, independent replication,
issue edit, accepted decision or production
readiness is inferred. Source 122 includes mutable branch links for intermediate probes;
not all intermediate revisions are available. Raw artifacts remain private outside Git,
with retention unspecified. The migration did not recheck upstream URLs or private artifacts.
The validator checks structure/local links, not chronological truth or substantive coverage.
PR policy is authored but no CI, agent configuration or merge rules are activated.

## Published-reference audit

On 2026-10-01, inspected all paginated issue/PR bodies, issue conversation
comments, and inline PR comments in `amadou-6e/laomedo` and `amadou-6e/specs`.
The snapshot covered respectively 17/156 issue-or-PR bodies, 4/49 conversation
comments, and 0/11 inline comments. PR #156's review summary was also read.
Path mentions and URLs were treated as consumers; an exact-revision URL was
not silently rewritten to a current target.

| Published consumer | Original paths referenced | Disposition |
| --- | --- | --- |
| [Laomedo #8](https://github.com/amadou-6e/laomedo/issues/8) | `feasibility/124.md`, `feasibility/docker-skill-draft.md` | Pointers retained |
| [specs #146](https://github.com/amadou-6e/specs/issues/146) | `feasibility/docker-skill-draft.md` | Pointer retained |
| [specs #118](https://github.com/amadou-6e/specs/issues/118), [PR #125](https://github.com/amadou-6e/specs/pull/125) | `feasibility/118.md` | Pointer retained |
| [specs #119](https://github.com/amadou-6e/specs/issues/119), [PR #126](https://github.com/amadou-6e/specs/pull/126) | `components/skill-revision.md`, `feasibility/119.md` | Pointers retained |
| [specs #120](https://github.com/amadou-6e/specs/issues/120), [PR #136](https://github.com/amadou-6e/specs/pull/136) | `components/codex-agent.md`, `feasibility/120.md`, `sandboxing/runner-isolation.md`, `monitoring/run-traces.md` | Issue body now names canonical isolation and trace contracts; other pointers retained |
| [specs #121](https://github.com/amadou-6e/specs/issues/121), [PR #137](https://github.com/amadou-6e/specs/pull/137) | `components/claude-agent.md`, `feasibility/121.md`, `sandboxing/runner-isolation.md`, `monitoring/run-traces.md` | Issue body now names canonical isolation and trace contracts; other pointers retained |
| [specs #122](https://github.com/amadou-6e/specs/issues/122) | `components/skill-draft.md`, `feasibility/122.md`, `sandboxing/runner-isolation.md` | Issue body now names canonical isolation contract; other pointers retained |
| [specs #123](https://github.com/amadou-6e/specs/issues/123) | `monitoring/run-traces.md`, `feasibility/123.md` | Issue body now names canonical trace contract; feasibility pointer retained |
| [specs PR #113](https://github.com/amadou-6e/specs/pull/113) | `components/agent-and-skill-components.md`, `sandboxing/runner-isolation.md`, `monitoring/run-traces.md` | PR body now names canonical isolation and trace contracts with a path-history note; component pointer retained |

Pointers remain for other migrated paths, so their uninspected consumers have
a compatibility route. Review summaries other than #156, other repositories,
external bookmarks, and URL fragments were not covered by the original audit.
The remaining pointers preserve document access, not HTTP redirection or old
section-fragment behavior.

## Retirement of two pointer folders

On 2026-10-02, [issue #169](https://github.com/amadou-6e/specs/issues/169)
authorized removal of the pointer-only `sandboxing/` and `monitoring/` folders.
The complete isolation and trace contracts were already in the subsystem
destinations in the table above; no substantive contract or evidence body was
deleted. `spec.json`, the project taxonomy and root navigation now list only
`capabilities/`, `components/` and `feasibility/` as compatibility categories.

Before removal, searches in the known `amadou-6e/specs` and
`amadou-6e/laomedo` issue/PR bodies found the retired paths in specs issues
#120–#123 and specs PR #113. With explicit user approval, their bodies were
re-read and edited to point to the canonical subsystem files. PR #113 retains
a note that its original diff used the old paths. Conversation comments on
those four issues and PR #113, plus PR #113 review and inline comments, had no
matches for these two paths at the time of inspection. Local project navigation
and the manifest no longer point to the deleted folders.

Deletion intentionally means mutable links to those two old paths will fail
after merge. Historical URLs pinned to a commit containing the pointers remain
available. Unsearched repositories, external bookmarks, and future references
cannot be rewritten or guaranteed; the direct canonical links above are the
replacement. This is a compatibility tradeoff accepted to avoid legacy folder
clutter, not a change to runner isolation or trace behavior.

## Related proposal history

[PR #154](https://github.com/amadou-6e/specs/pull/154) was closed as superseded
by the merged authoring system. Its distinct focused owner-interview method
was later revised and merged as the shared
[owner-interview skill](../../../shared/skills/owner-interview/SKILL.md) (specs #326, #330). [PR #152](https://github.com/amadou-6e/specs/pull/152)
merged the Work Graph contract into its owned subsystem; this migration record
preserves the `capabilities/` pointer and does not change Work Graph behavior.
