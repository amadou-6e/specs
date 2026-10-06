---
title: EXP-19 artifact retry results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

The first attempt's private native trace shows an agent-originated write command for the selected report path exiting 1 with a missing-directory error; its follow-up path check also exited 1. The source fixture lacked that parent, and no command in the failed turn created it. This explains the missing artifact without attributing the outcome to a general sandbox write denial. The direct agent-originated nested-write diagnostic then passed at turn 7/10. The fixture and pre-dispatch source check are corrected in Laomedo `42c8a5f` and tested without a model call. Raw command text and trace payloads remain private.

**Go for the bounded single-user local issue-to-agent-to-draft-PR path.** Turn 8/10 ran through the imported Langflow flow, completed a native Codex turn with two command results, and produced a report bound to the frozen issue and graph. The trusted host published exactly that artifact in [draft PR #71](https://github.com/amadou-6e/laomedo/pull/71). Its commit `769b47b36572251f702cf7e84674f96316d8bdde` changes only the selected report; an independent byte comparison matched artifact digest `sha256:b05e98c3bb4b42cf20c9a3e743bc4e1ec646c63b4a6501ab28b20b02f5dd6f15`. The private Work Graph binding records the source marker, snapshot, workflow run, trace, native thread, artifact, commit and PR URL. [Execution](execution.md) gives the exact identities.

The earlier 6/6 attempt and failed artifact gate remain negative evidence. The immediate missing-directory failure is established by the native command result. This retry shows that a source fixture with a pre-created output parent and a source-hash gate can support the positive path; it does not prove whether the fixture, explicit task wording, or both were needed to change the agent's behavior. The cumulative ledger is **8/10**. The remaining two authorized turns were not used.

This result meets the local evidence sought by [EXP-19 #49](https://github.com/amadou-6e/laomedo/issues/49) and the artifact-production outcome in [#69](https://github.com/amadou-6e/laomedo/issues/69). It does not establish EXP-18's deferred agent-originated push boundary, production browser-auth lifecycle, hosted service isolation, or multi-user safety. Those limits remain separate from the observed draft PR.

## Prerequisite disposition for EXP-19

The [#49 sequence](https://github.com/amadou-6e/laomedo/issues/49) requires completed evidence or documented blockers from these experiments. This table distinguishes inputs to this local run from gates that remain unverified.

| Experiment | Evidence used or accepted limit |
| --- | --- |
| [EXP-01 #50](https://github.com/amadou-6e/laomedo/issues/50) | **Unrun limit.** The independent adversarial Work Graph source/readiness corpus has no result. EXP-19 checked the selected issue and source-complete snapshot for this run, which does not substitute for EXP-01. |
| [EXP-02 #32](https://github.com/amadou-6e/laomedo/issues/32) | The [merged read-only issue adapter](https://github.com/amadou-6e/laomedo/pull/51) supplied selected issue identity, update marker and current body; a discovered PR was never treated as the authorized target. The issue was rechecked before publication. |
| [EXP-03 #33](https://github.com/amadou-6e/laomedo/issues/33) | The [partial graph-freeze result](../../../langflow-graph-freeze/iterations/2026-10-02/results.md) informed the explicit saved-flow digest and import/round-trip freeze. Native component-code attestation remains unproved. |
| [EXP-04 #34](https://github.com/amadou-6e/laomedo/issues/34) | The [synthetic durable pre-dispatch result](../../../durable-pre-dispatch/iterations/2026-10-02/results.md) informed run/trace reservation before dispatch and no blind replay. The live run retained its reservation. |
| [EXP-05 #35](https://github.com/amadou-6e/laomedo/issues/35) | The [synthetic crash/evidence result](../../../agent-evidence-crash/iterations/2026-10-03/results.md) informed private raw-event retention and failed-run evidence. This live run did not inject a crash. |
| [EXP-06 #36](https://github.com/amadou-6e/laomedo/issues/36) | The [UI/backend-death result](../../../ui-versus-backend-death/iterations/2026-10-02/results.md) distinguishes client disconnect from backend death. EXP-19 kept isolated Langflow state but did not repeat either fault. |
| [EXP-07 #37](https://github.com/amadou-6e/laomedo/issues/37) | The [synthetic 60-second orphan-lease result](../../../orphan-lease/iterations/2026-10-02/results.md) is a boundary limit, not a claim that this real agent used the supervisor or that a GitHub grant was exposed to the stage. |
| [EXP-08 #38](https://github.com/amadou-6e/laomedo/issues/38) | The [pinned-skill byte/cleanliness result](../../../pinned-skill-materialization/iterations/2026-10-03/results.md) informed revision and source-tree checks. Native discovery remained unverified there; EXP-19 reports the skill as offered, not proven used. |
| [EXP-09 #39](https://github.com/amadou-6e/laomedo/issues/39) | The [synthetic replay result](../../../agent-event-replay/iterations/2026-10-04/results.md) requires uncertainty for duplicate deliveries. EXP-19 retained private native events and did not infer unique external actions from receipt counts. |
| [EXP-10 #40](https://github.com/amadou-6e/laomedo/issues/40) | The [merged timeout probe](https://github.com/amadou-6e/laomedo/pull/63) observed late effects after caller/server timeouts and **did not pass safe-timeout acceptance**. EXP-19 counted timeouts in its turn cap, did not silently replay ambiguous attempts, and published only after a completed run and verified artifact. Its successful turn had no timeout; cancellation and effect reconciliation after a future timeout remain unverified. |
| [EXP-13 #43](https://github.com/amadou-6e/laomedo/issues/43) | **Unrun limit.** No approval-expiry/denial/Stop result exists. This run used a pre-recorded bounded grant and a runner with approval policy set to never, so no in-run access request was tested. |
| [EXP-14 #44](https://github.com/amadou-6e/laomedo/issues/44) | The [merged synthetic issue-publication result](https://github.com/amadou-6e/laomedo/pull/52) informed the no-blind-retry rule. EXP-19 published a PR, not an issue, and confirmed its remote head/base and commit; it did not fault-inject a lost PR-create response. |
| [EXP-16 #46](https://github.com/amadou-6e/laomedo/issues/46) | **Unrun limit.** The independent mock-runner stale-source/blocker/grant matrix is absent. EXP-19 froze and checked one real source-complete graph, but this is not independent EXP-16 coverage. |

## Credential boundary and publication scan

The subscription-backed Codex login was present in the runner's private Docker volume at `/home/runner/.codex/auth.json` inside the Codex controller container. It was not copied into `/draft`, `/canonical`, or the selected report. The command worker uses the named permission profile's exact-path deny for that file; the credential-free preflight observed a denied direct command read. This is an observed exact-path boundary, **not** an audit of every possible route from a model to the controller's credential. The runner API token stayed with the runner/Langflow side of the bridge; the host publisher alone used GitHub write access.

After publication, a no-output-value fingerprint scan compared six private credential strings from the runner's actual Codex login and API token against the diffs and bodies of Laomedo PRs #64 and #71, specs PR #209, and 31 selected text files across committed EXP-19 evidence and turn 8's workspace/canonical/post-run snapshots. It found **zero exact matches and zero recognized bearer/API-key shape hits**. This checks the known secrets and inspected files at this revision; it is not a claim that arbitrary unknown secrets or alternate credential access routes were exhaustively ruled out. The private login, token, raw events and scan inputs remain outside Git.
