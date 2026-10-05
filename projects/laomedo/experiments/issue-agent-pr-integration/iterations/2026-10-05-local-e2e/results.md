---
title: EXP-19 local end-to-end results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

**No-go for the full issue-to-agent-to-PR claim.** The selected issue and Work Graph snapshot were coherent, the pinned Skill and Codex Agent flow imported into isolated Langflow, and the runner's local permission and API preflights passed. The final Langflow turn reached a completed native Codex thread with three command results, but no selected output file. The trusted host publisher correctly refused publication. The turn ledger is **6/6**; no `test/49` branch, output PR, or confirmed Work Graph publication binding exists.

The first four turns failed before an agent response. The new diagnostic classified the fourth as nine response-stream disconnects followed by one `other` error. The private login copy differed from and predated the current host login; an authenticated no-model rate-limit read failed before the private copy was refreshed and succeeded after. Turn five then completed a minimal direct-runner request with exactly `READY` and no native errors. This supports a stale private login as the practical cause of the early failures, but does not rule out concurrent service recovery. [#68](https://github.com/amadou-6e/laomedo/issues/68) records that finding; the production browser-auth lifecycle remains in [specs #129](https://github.com/amadou-6e/specs/issues/129).

The [local runner API contract](../../../../subsystems/agent-execution/contract/runner-api.md) permits only fixed protocol error codes and numeric status codes in the public diagnostic. The first three raw rollouts were not retrospectively classified by an ad hoc trace dump. Turn six ran only after the minimal direct gate passed; its missing artifact is a separate unresolved blocker in [#69](https://github.com/amadou-6e/laomedo/issues/69). A zero-model command proved that the nested output path is writable under the same container policy, so the agent-turn failure is not explained by that filesystem boundary. No further model turn is authorized under the exhausted grant.

This result does not change the completed phase-zero fake-agent observation, and it does not close [EXP-19 #49](https://github.com/amadou-6e/laomedo/issues/49).
