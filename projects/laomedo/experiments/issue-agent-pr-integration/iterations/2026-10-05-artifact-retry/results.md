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
