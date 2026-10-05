---
title: EXP-19 artifact retry execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The first attempt and its private 6/6 ledger remain intact. A separate private grant records four added submitted turns and a cumulative cap of 10. Turn 7/10 used the same Docker permission profile, model `gpt-6-luna`, `low` effort, source workspace and pinned skill revision as the first attempt. The native run completed with no error events and created/read the exact nested path `/draft/experiments/exp19/agent-output.md` with the expected disposable canary. Native run ID `b1aeca41-3efb-4e34-8142-5ca86530dde4` remains private evidence; no artifact from this diagnostic is eligible for host publication.

The implementation at Laomedo `42c8a5f` now tracks the output parent in the disposable source fixture and refuses a missing parent, a pre-existing output file, or a source tree changed since the plan was frozen. Credential-free tests passed before the next Langflow attempt. The observed turn 7 preceded this protocol amendment and is recorded as diagnostic evidence, not as a retrospectively precommitted positive protocol.

The follow-up plan froze issue #49, source-complete Work Graph snapshot `sha256:089d4c23050a6e0304d147fa90b360d9334a2b66485e47896a0b4f76ba66f9d8`, code `42c8a5f`, specs `0905a16`, the changed source fixture, Skill revision `sha256:7c7462da8d7b3b68f1d05fea75d9e4f0904a55fb81a49bb40c00e24ba46c4b59`, and saved flow digest `sha256:b675b79f6301a99ed5d71981fd98e240029da16d4852b46cc64155c94cb894b2`. Isolated Langflow imported and round-tripped flow `f71de7b8-829d-4e26-8c81-a807310728fc` without a model turn. The runner ledger was 7/10 before dispatch.

Turn 8/10 ran through that imported flow. Native run `326dfc8b-7d1e-4360-bf71-002a9651a870` completed with two agent-originated command results. The private workflow record `d8e43144-a939-48c2-92bd-0c2eb75c6e14` retained trace `ab01656f-1654-4805-9e2c-0f29619d21d6` and verified the selected `experiments/exp19/agent-output.md` as UTF-8, at most 8 KiB, containing the exact issue URL, body digest and graph snapshot ID. Its artifact digest was `sha256:b05e98c3bb4b42cf20c9a3e743bc4e1ec646c63b4a6501ab28b20b02f5dd6f15`.

The trusted host used the previously recorded one-draft-PR grant for `amadou-6e/laomedo`, `test/49` into `develop`. It reselected and rehashed the same private artifact, committed only that file as `769b47b36572251f702cf7e84674f96316d8bdde`, pushed the branch, and confirmed [draft PR #71](https://github.com/amadou-6e/laomedo/pull/71) with the exact head and base. An independent byte comparison of the commit blob and selected private artifact matched, and the commit changed only `experiments/exp19/agent-output.md`. The private binding includes work key `github:I_kwDOUu9rs88AAAABUq5QtQ`, issue update marker `2026-10-05T10:09:25Z`, body digest `sha256:24fd4e512649b6c7436ab796d6f04f1c059a4761290cf5e2637fa932ea2cb23b`, graph snapshot, workflow run, trace, native thread, artifact hash, commit and PR URL.

The cumulative ledger is **8/10**. No further model turn was needed. The agent command container never received the host GitHub credential; private login and raw rollouts remain outside Git. The draft PR is an observed local single-user result, not proof of direct agent push, hosted or multi-user operation.
