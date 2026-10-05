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

Next: freeze issue #49, a source-complete Work Graph snapshot, the current code and specs revisions, the fixture digest, the pinned Skill and saved flow; import and round-trip the flow; then submit at most the remaining three turns under the cumulative 10-turn ceiling. No new Langflow turn or GitHub write has occurred in this retry at this stage.
