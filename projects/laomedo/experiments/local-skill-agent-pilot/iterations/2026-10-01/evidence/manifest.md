---
title: Pilot evidence manifest
status: complete
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Pilot evidence manifest

| Artifact | Producer | Stable identity/location | Access and retention |
| --- | --- | --- | --- |
| Sanitized acceptance JSON | Original pilot author | [e2e-results at 8bfd0af](https://github.com/amadou-6e/laomedo/blob/8bfd0af/examples/skill-agent-pilot/e2e-results.json) | Public repository history |
| Reproduction guide | Original pilot author | [README at 8bfd0af](https://github.com/amadou-6e/laomedo/blob/8bfd0af/examples/skill-agent-pilot/README.md) | Public setup/four steps |
| Runner/component code | Laomedo PRs #13/#14 | Commit 5e14c7a | Branch implementation, not asserted merged |
| Raw responses/events, records/snapshots | Langflow, Codex and runner | Original report's private matching IDs/hashes | Outside Git; full-corpus digest/retention unavailable |
| Preserved local report | Original specs pilot author | Source 2854612, [result](../results.md) | Migration adds no independent verification |

No private data is copied or hashes invented where only a commit pin exists. The original
author reports checking sanitized JSON against private evidence; this migration did not
repeat that verification. Evidence directory is support for this attempt, not another collection.
