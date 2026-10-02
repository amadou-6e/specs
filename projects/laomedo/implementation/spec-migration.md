---
title: Specification migration record
status: complete
kind: migration-record
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Specification ownership migration

Local trial prepared and agent-checked 2026-10-01; user review requested compatibility fixes; revised acceptance pending. Source specs revision 2854612a32a40b6b455734cd2d758f92f86f1897.
Historical implementation/evidence identities and observations remain unchanged.

| Original path | Canonical owner |
| --- | --- |
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
Every original document path in the table remains a short compatibility pointer.
Full bodies exist only at their canonical destinations. The local Markdown
inventory was insufficient: published issue and PR references also depend on
these paths. Historical revision URLs remain valid, and mutable `main` or
branch URLs can now reach the pointers after migration. The four restored
containers own only closed pointer sets, not additional active contracts.
The deprecated UI path and binary artifacts remain unchanged.

No new experiment, independent replication, issue edit, accepted decision or production
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
| [specs #120](https://github.com/amadou-6e/specs/issues/120), [PR #136](https://github.com/amadou-6e/specs/pull/136) | `components/codex-agent.md`, `feasibility/120.md` | Pointers retained |
| [specs #121](https://github.com/amadou-6e/specs/issues/121), [PR #137](https://github.com/amadou-6e/specs/pull/137) | `components/claude-agent.md`, `feasibility/121.md` | Pointers retained |
| [specs #122](https://github.com/amadou-6e/specs/issues/122) | `components/skill-draft.md`, `feasibility/122.md` | Pointers retained |
| [specs #123](https://github.com/amadou-6e/specs/issues/123) | `monitoring/run-traces.md`, `feasibility/123.md` | Pointers retained |
| [specs PR #113](https://github.com/amadou-6e/specs/pull/113) | `components/agent-and-skill-components.md` | Pointer retained |

Pointers are also retained for the remaining migrated paths, so uninspected
consumers have a compatibility route. Review summaries other than #156,
other repositories, external bookmarks, and URL fragments were not audited.
The pointers preserve document access; they are not HTTP redirects and do not
guarantee that old section fragments navigate into the new document. No
published issue or PR reference was edited by this fix.

## Concurrent proposals

[PR #154](https://github.com/amadou-6e/specs/pull/154) proposes a conversational
`define-project-spec` skill for eliciting user scenarios and ownership choices.
That is distinct from this trial's repeatable authoring-system migration skill;
neither is treated as a substitute for the other. Reconcile their overlapping
Laomedo structure guides and templates before merging both approaches.
[PR #152](https://github.com/amadou-6e/specs/pull/152) proposes Work Graph behavior.
This trial does not incorporate or approve that capability. Its eventual
contract owner and reading paths need reconciliation with the chosen taxonomy.
No changes to those PRs or their issues are included here.
