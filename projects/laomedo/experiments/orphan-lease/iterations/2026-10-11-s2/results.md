---
title: S2 bounded result
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-11
applies_to: [laomedo]
supersedes: null
related: []
---

# S2 bounded result

**Incomplete**, failure_code service_cleanup_unverified_or_late after an active commandExecution boundary and completed runner-tree kill (inferred from failure stage; timing not captured). Independent service diagnostic says heartbeat_lost and never_observed: no verified service cleanup. Final harness cleanup is not service-attributed cleanup. Refusal, B continuity, delayed sentinel and restart checks were not reached.

The original capture lacks kill-completion/command-start timing because those fields were only populated after successful cleanup. Revocation within60seconds of the kill cannot be assessed from this public observation. native_identity.turn_id is null; do not invent a turn ID. Retrospective whitelisted lease diagnostics are separate from the machine capture. B's grant-expired cleanup is not a continuity pass.

Docker removing the attached container before the service's first check is a hypothesis, not established cause. No relaxed acceptance is applied to S2. Shared14/16; two turns remain. Any follow-up requires a fresh frozen identity and independent pre-run review.
