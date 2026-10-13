---
title: Issue integration validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-13
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

## GitHub PR node local verification, 2026-10-13

The [PR contract](contract/pr-node.md) and [editable interaction model](design/github-pr-node.drawio)
were authored for the user-selected PR alignment. Implementation base is Laomedo
develop `c29c93f2af93dde0a57dcbb3d38f23336407f56c`; the visible implementation
checkout's `examples/github-pr/evidence.json` pins the changed source hashes.
These checks describe the local candidate, not a merged or activated release.

- Twelve credential-free host tests passed for PR discovery, filters, close/
  title/body/labels operations, target/head/merged/grant refusals, expiry,
  durable replay and partial/uncertain effects.
- Four native lfx 1.12.3 node tests and three authenticated inspection tests
  passed. Eight existing publisher, 23 mediator, 14 REST transport and 17 live
  Issue fixture regression tests passed.
- The historical four-node operation graph (implementation commit `fdd17a0`,
  now preserved as `examples/github-pr/four-node-flow.json`) executed twice
  through Graph.arun: one confirmed fixture metadata update, no repeated effect,
  zero model turns and zero live provider writes.
- Five React viewer tests passed with real Markdown rendering, covering exact
  link identity, read-only payload, refresh, unsafe markup, stale responses,
  missing selection and abort/error behavior. A temporary Node resolver and
  visible-path harness avoided a missing Windows native DLL and hidden-directory
  test discovery; the production overlay did not adopt either workaround.
- The overlay applied to upstream Langflow `fec71dca901949c09ed4d63315804337cd2eb13d`.
  Node 22.16.0 production build passed. TypeScript baseline and candidate each
  reported 253 diagnostics; comparison normalized line/column offsets and found
  zero added or removed diagnostic messages. Full typechecking remains red.
- The actual PR viewer was rendered and visually inspected in Edge using an
  isolated fixture entry and mocked read response. The [reference screenshot](design/references/github-pr-viewer.png)
  is bounded UI evidence, not live GitHub acceptance. Both editable diagrams were
  inspected through temporary raster previews; the previews are not tracked.

No active application connection or write grants were changed. Complete installed
application selection/browser regression, live PR operations, independent review,
merge and deployment remain unverified. The creation mode/run-result viewer is a
proposal. GitHub connector tracking creation returned 403; automatic approval
review rejected a credential-helper retry, so tracking/publication remain pending
human authorization. No issue, PR or remote branch was created by this task.

## Two-node PR and Agent verification, 2026-10-14

The user selected PR → Agent → the same PR. The revised
[operation diagram](design/pr-operation.drawio) and contract describe this bounded
one-shot loop. The implementation example now contains two nodes and two native
connections, with PR #1 selected. Its Agent is a deterministic fixture.

- Eleven actual Graph.arun tests passed: modify/close and exact feedback output,
  one Agent invocation, durable replay, absent selection, invalid response,
  Agent failure/cancellation, concurrent edit refusal, uncertain write and
  conflicting ordinary Operation input.
- Four native PR node, twelve host PR and three authenticated inspection tests
  passed after the change.
- The saved two-node flow executed successfully through the running Langflow
  build/events API. Its PR completed with no next runnable vertices. Edge checks
  confirmed exactly two visible nodes, selected PR viewing and its GitHub link.
  The [editor screenshot](design/references/github-pr-two-node.png) records this
  disposable local app; fake provider, zero real GitHub writes and no model turns.

The component scopes its parameter adapter to its own vertex: return feedback
is resolved by the isolated body after the read, rather than as an eager input.
Outer conditional exclusion prevents a second Agent execution. Existing PR
creation remains the separate proposal in the contract. Live model/provider
integration and remote publication remain unverified.
