---
title: Skill registry and drafts validation
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill registry and drafts validation

The proposed [library-facing and agent-facing interfaces](contract/interfaces.md)
extend the existing registry boundary. Existing pilot evidence for exact
whole-bundle lookup does not prove prompt-library versioning, backend
publication or all-item materialization.

No implementation test was executed in this authoring migration. Evidence is bounded
by its original version, task, grant and date.

| Guarantee | Evidence | Boundary / gap |
| --- | --- | --- |
| Whole-skill bytes | 2026-10-01 pilot | Exact revision/hashes materialized before effective hash |
| Draft policy / candidate / resume | #122 and Docker source | Validated edit and pinned candidate; no promotion |
| Isolated rules/examples | #119 | Combined channels do not prove isolated subsets |
| Concurrent base update | #122 deterministic fixture | Eligibility guard checked; full promotion incomplete |
| IF-03/IF-14 library resolution and draft submission | No new check | New catalog integration is a target, not proven by the pilot |

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
