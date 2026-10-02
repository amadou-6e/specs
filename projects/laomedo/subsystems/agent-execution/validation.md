---
title: Agent execution validation
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
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
| New IF-05/IF-06 stage invocation and same-session conflict | No new check | Target interface only; not executed |
| Three-attempt same-session crash recovery and run-scoped approvals | No new check | Newer user decision; earlier pilot does not establish this behavior |

The [decision-readiness triage](design/decision-readiness.md) proposes E01-E08;
**none was executed** in this authoring task. In the first slice, automatic
mid-turn container recovery is deferred and a crash reports a failed
invocation. A Docker reduced-protection policy is also deferred until its
experiment is designed, reviewed and run. The pilot's clean restart/resume
does not test either container crash recovery or an orphaned writable stage.

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
