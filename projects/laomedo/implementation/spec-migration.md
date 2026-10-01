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

Local trial prepared and agent-checked 2026-10-01; user critique pending; source specs revision 2854612a32a40b6b455734cd2d758f92f86f1897.
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
The old implementation pilot location remains a compatibility pointer. Other old locations
had no cross-project Markdown references in this local inventory. Historical revision links
remain valid; current external links to removed paths may need updating by their owners.
The deprecated UI path and binary artifacts remain unchanged.

No new experiment, independent replication, issue edit, accepted decision or production
readiness is inferred. Source 122 includes mutable branch links for intermediate probes;
not all intermediate revisions are available. Raw artifacts remain private outside Git,
with retention unspecified. The migration did not recheck upstream URLs or private artifacts.
The validator checks structure/local links, not chronological truth or substantive coverage.
PR policy is authored but no CI, agent configuration or merge rules are activated.
