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

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
