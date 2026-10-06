---
title: Issue integration validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue integration validation

No product IF-01/IF-12 handoff test has run. EXP-14 and EXP-15 test bounded
publication mechanisms, not a deployed publisher. Proposed acceptance checks:

| Interface | Check before acceptance | Evidence status |
| --- | --- | --- |
| IF-01 | Selected issue reference reaches run setup; the agent fetches current GitHub content and reports a related PR without targeting it automatically | Not executed |
| IF-01 bypass | Direct prompt and timer launches do not fabricate an issue or call IF-01 | Not executed; timer is outside first slice |
| Launch context | A PR-opened event preserves its PR subject; a failed Actions event preserves workflow-run identity, revision and failure context without fabricating an issue | Not executed; both event paths are outside first slice and lack a selected trigger-service owner |
| Launch context | An issue-opened event supplies a real issue subject and delivery identity, which the future trigger service deduplicates before IF-01 | Not executed; outside first slice, dedup policy open |
| IF-12 review gate | An unreviewed or edited-after-review request cannot publish; exact reviewed body, marker, target, decision and attempt persist before POST | Synthetic guard and persistence checks in [EXP-14 at `602d6aa`](https://github.com/amadou-6e/laomedo/blob/602d6aace30df756f5455c2d8a2c6535dd7951da/experiments/issue-integration/44/README.md); no product handoff test. EXP-14 headers are not a GitHub body marker. |
| IF-12 uncertain effect | Kill before send or after acceptance but before acknowledgement: retain `unknown`, no issue reference and no automatic retry; distinguish confirmed publication | [EXP-14 synthetic three-kill-point test](https://github.com/amadou-6e/laomedo/blob/602d6aace30df756f5455c2d8a2c6535dd7951da/tests/test_issue_publication_probe.py) passes; full backend crash and production status projection not tested. |
| IF-12 reconciliation | After a lost acknowledgement, query/list and verify exactly one full body marker; absence is inconclusive, multiple exact matches require user resolution, and no automatic repeat POST occurs | [EXP-15 live record at `243c103`](https://github.com/amadou-6e/laomedo/blob/243c103a4f88d0b197f3a56224717e520c8805a7/experiments/issue-integration/45/README.md): two early negative lookup pairs followed by one exact match; zero repeat POSTs. One private disposable repository only; no safe timeout, load test or network partition. Multiple-match and user-resolution product paths not executed. |
| IF-12 known failure | A definitely unsent request or an acknowledged non-creating GitHub rejection retains the reviewed draft and reports `failed` without an issue reference; HTTP 5xx, transport loss and zero search results remain `unknown` | No rejected-POST live control or product test. The [create-issue status documentation](https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28) lists rejection statuses, but this spec does not treat an arbitrary error as proof of non-creation. |

The [handoff graph](../../architecture/subsystem-handoffs.md) is design evidence,
not a runtime result. Pin implementation and API versions when these checks run.
