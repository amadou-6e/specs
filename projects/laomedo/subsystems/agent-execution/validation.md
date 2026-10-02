---
title: Agent execution validation
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution validation

No implementation test was executed in this authoring migration. Evidence is bounded
by its original version, task, grant and date.

| Guarantee | Evidence | Boundary / gap |
| --- | --- | --- |
| Snapshot-bound restart/resume | 2026-10-01 pilot, Codex 0.159.2 | Same native thread and snapshot observed; API only |
| Missing snapshot / cancellation / cap | Same four-turn pilot | HTTP 400 before reservation; 39 partial events; ledger 4/4 |
| Isolation / read-only / remote mode | #120, #122, Docker sources | Earlier failures retained; general grant and remote storage unproven |
| Claude parity | #121 | CLI blocker before model call; acceptance unknown |
| OpenCode authenticated prototype | [2026-10-02 verification](../../experiments/opencode-agent/iterations/2026-10-02/results.md) | Native multi-skill fresh/resume and tested worker credential denial observed; live cancellation status race fixed by synthetic regression; no exhaustive boundary or hosted claim |
| Reusable Langflow custom node | Eight synthetic component/graph checks, 34 host checks, installed catalog/flow round trip | UI Stop propagation deferred to Laomedo #22; browser visual placement not separately inspected |
| Installed native-node fresh/resume | [Four-turn attempt](../../experiments/native-codex-node/iterations/2026-10-01/results.md) | Catalog, flow round trip, tool results, bound restart/resume and host isolation observed; cancellation inconclusive, sample fresh task failed |
| Explicit node cancel / successful fresh task | [Authorized retry](../../experiments/native-codex-node/iterations/2026-10-01-retry/results.md) | Runner cancelled via transport teardown, 33 partial events; fresh native command confirms no marker; aggregate ledger 6/6 |

Current native-node detail: [implementation/acceptance record](../../implementation/native-langflow-node.md).

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
