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

Historical checks below include a PR-specific CLI adapter subsequently removed
at the user's request on 2026-10-15. They are not acceptance of the original
Laomedo Codex Agent or of the current merge candidate. The corrected contract
requires the existing agent and reports Docker unavailability as a blocker.

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

## Real-agent and live PR verification, 2026-10-14

The user required real-agent demonstrations and explicitly authorized creating
PRs/issues in `ga84jog/laomedo-exp104-disposable-20261007`. The trusted host created
[draft PR #20](https://github.com/ga84jog/laomedo-exp104-disposable-20261007/pull/20),
then the saved two-node graph read it, ran the installed Codex CLI once and
applied the returned body update through the same PR node and scoped gateway.
The graph stopped with no next runnable vertices. Native thread
`01a1382b-a05e-72e3-b18f-18af29d3d9dc` reported turn completion.

The host confirmed the write; independent GitHub connector readback confirmed
the appended description section. The live browser check confirmed exactly two
nodes, PR #20 selection, its updated body and exact external link. The
[editor screenshot](design/references/github-pr-real-agent.png) records the real
Agent and selected live PR. Implementation `examples/github-pr/real-flow.json`
and `real-evidence.json` preserve the importable graph and source hashes.

An initial live read-only attempt exposed arbitrary cycle entry: Codex ran
twice, with missing context on the first turn. No write occurred. The fix binds
feedback handling during payload component construction and scopes cycle entry
to the owning PR. A subsequent read-only run completed one real turn and refused
the absent grant. The final authorized PR #20 run completed one real turn and
one confirmed operation. Internal regression checks passed for the revised
scheduler and native node; they are not substitutes for this live evidence.

The connected GitHub app refused branch creation with 403. The user then
supplied a host token in `.env`; it was excluded from Git and child environment.
The grant targeted only PR #20's head/base and short-lived description update.
No issue was needed. No production Docker isolation, live close/labels operation,
merge, or implemented PR-node creation mode is claimed.

## Operation input with ordinary and feedback connections

The user selected a single Operation port for both modes. The current example
connects PR Task → real Codex Agent → the same PR Operation. The Task infinity
socket is absent from newly generated nodes. Normal acyclic inputs retain their
direct execution path; Data and JSON Message payloads are accepted. Conflicting
Operation sources, literal-plus-feedback values and unsupported longer feedback
chains are refused. Historical infinity graphs retain compatibility.

The real saved graph ran one completed Codex turn, native thread
`01a1398c-80bb-7861-9c45-59b8f3b10c2b`, and confirmed one description update on
[PR #20](https://github.com/ga84jog/laomedo-exp104-disposable-20261007/pull/20).
Independent GitHub readback and the live viewer confirmed the new description.
The browser check removed the feedback edge through the editor context menu
and manually dragged the Agent output to the PR Operation input successfully.
It confirmed two nodes and two PR input handles, with no infinity return socket.
The [editor reference](design/references/github-pr-operation-feedback.png) shows
the final wiring. The production frontend build emitted successfully.

Internal regression coverage passed for feedback execution, ordinary upstream
operations, Message JSON, ambiguous sources, failed reads, concurrent edits,
cancelled/failed Agents, unknown writes and durable replay. These tests supplement
the real integration evidence in `examples/github-pr/operation-feedback-evidence.json`.
