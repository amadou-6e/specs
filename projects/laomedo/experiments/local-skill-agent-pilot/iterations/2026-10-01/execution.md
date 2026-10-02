---
title: Pilot execution reconstruction
status: complete
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Reconstructed execution record

Actual test: 2026-10-01. Implementation 5e14c7a; evidence 8bfd0af. Codex CLI 0.159.2,
Langflow 1.12.3, gpt-6-luna/low, Docker Desktop Windows host. Exact runtime/permission/
skill hashes remain in [results](results.md). Detailed hardware and wall-clock step
timestamps are unavailable in this source record.

Reported sequence: saved-flow execution/marker write, host-runner restart/API resume,
independent fresh saved-flow run, cancellation after command start. Negative snapshot
and exhausted-cap checks did not allocate extra native turns. Ledger ended 4/4.
The pinned [reproduction guide](evidence/manifest.md) owns exact setup and commands.

Limits/deviations: API resume instead of a Langflow resume control, existing writable
Docker grant and single-user login, inner usage unknown, browser untested. No new run,
credential operation, independent artifact check or model spend occurred in reconstruction.
Private source responses/events and snapshots remain outside Git.
