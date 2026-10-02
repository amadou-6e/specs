---
title: Skill registry and drafts validation
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill registry and drafts validation

No implementation test was executed in this authoring migration. Evidence is bounded
by its original version, task, grant and date.

| Guarantee | Evidence | Boundary / gap |
| --- | --- | --- |
| Whole-skill bytes | 2026-10-01 pilot | Exact revision/hashes materialized before effective hash |
| Draft policy / candidate / resume | #122 and Docker source | Validated edit and pinned candidate; no promotion |
| Isolated rules/examples | #119 | Combined channels do not prove isolated subsets |
| Concurrent base update | #122 deterministic fixture | Eligibility guard checked; full promotion incomplete |
| Langflow Skill reference wiring | Nine pinned component/graph checks, 34 host checks; real run 6af56062-03f7-43b1-9a50-7000d3269d98 | Same whole-skill revision; native fixture read observed; reference node does not browse/edit/resolve store contents |
| Multiple skill references | 37 host checks and 11 pinned Langflow checks, including two connected Skill nodes in an actual graph | Synthetic runner traffic; materialization, resume preservation and failure cleanup verified; no multi-skill model-backed turn yet |

Skill node evidence: Laomedo examples/native-codex-node/skill-node-evidence.json,
paired with its #25 implementation PR. The authorized ledger was 7/8 after this
separate follow-up; the earlier six-turn agent-node evidence remains historical.

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
