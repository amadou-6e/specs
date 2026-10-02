---
title: Resume validation example
status: template
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Resume validation example

| Requirement | Proposed check | Evidence status |
| --- | --- | --- |
| Restore post-run files | Create marker, restart, resume and read marker | Not executed for example |
| Reject absent snapshot | Hold snapshot, call resume, compare ledger | Not executed for example |
| Fresh separation | Start independent run and assert marker absent | Not executed for example |

[Real pilot](../../experiments/local-skill-agent-pilot/README.md) supplies related bounded
observations, not acceptance of this entry. Record actual implementation/artifact pins
before replacing gaps. Model-backed tests require separate authorization and budget.
