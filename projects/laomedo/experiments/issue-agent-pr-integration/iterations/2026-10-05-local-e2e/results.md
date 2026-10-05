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

**No-go for the real issue-to-agent-to-PR claim.** The selected issue and Work Graph snapshot were coherent, the pinned Skill and Codex Agent flow imported into an isolated Langflow server, and the runner's local permission and API preflights passed. Two flow-triggered model turns and one minimal direct-runner turn reached native threads but ended `failed` before a command or selected artifact. The turn ledger is **3/6**. No draft output PR or confirmed Work Graph publication binding exists.

The same failure on the minimal direct-runner prompt places the observed blocker below Langflow, but does not distinguish login validity, model entitlement, service availability, CLI settings, or runner transport. A local login-status report and anonymous network checks are insufficient to resolve that distinction. [Follow-up #68](https://github.com/amadou-6e/laomedo/issues/68) must diagnose it with safe, structured evidence before another model turn. The separate browser-auth lifecycle remains in [specs #129](https://github.com/amadou-6e/specs/issues/129). The user-authorized `test/49` draft-PR publication was correctly not attempted because the artifact gate never passed.

The follow-up diagnostic is defined by the [local runner API contract](../../../../subsystems/agent-execution/contract/runner-api.md): it projects only fixed protocol error codes and numeric status codes. It is prospective for a later submitted turn. The three earlier raw rollouts are not retrospectively classified by an ad hoc trace dump.

This result does not change the completed phase-zero fake-agent observation, and it does not close [EXP-19 #49](https://github.com/amadou-6e/laomedo/issues/49).
