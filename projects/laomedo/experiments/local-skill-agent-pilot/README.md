---
title: Local skill-agent pilot
status: complete
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Local Langflow skill-agent pilot

Question: can a saved flow run a pinned whole skill through local Codex, retain native
tools, and preserve fresh/resume/failure identity? Outcome: go for the tested single-user
route, not full product acceptance. Actual execution: 2026-10-01, four turns, ledger 4/4.

Read [retrospective protocol](protocol.md), [sources](sources.md), [attempt index](iterations/README.md)
and [preserved result](iterations/2026-10-01/results.md). Saved node starts fresh runs;
resume was runner-API only. Browser interaction, Claude parity, general read-only grants
and hosted readiness remain unverified. Consumers: capability reviewers and validation authors.

Schema: README.md, protocol.md, sources.md, iterations/README.md (1 each), attempts (0..*),
with the category attempt schema. This migration adds organization, not a new run or
independent replication. Target authority stays in subsystem contracts; exact reproduction
commands stay in the pinned implementation guide linked by the evidence manifest.
