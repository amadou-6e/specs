---
title: Agent execution
status: draft
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution

Owns: Provider dispatch, private profiles, grants and session-to-workspace binding. Codex and Claude adapters share this boundary.

Maturity: Codex local pilot exists; Claude model-backed acceptance remains unknown. Draft target requirements remain broader than observed guarantees.
Consumers: flow adapters, execution services and inspection tools as applicable.
Dependencies: [shared records](../../architecture/shared-contracts.md) and peer contracts.

Read [contract](contract/README.md), [design](design/README.md), [validation](validation.md).
Entry schema: those pages and this overview (1 each), focused contract/design pages (0..*).
Add optional guides/extensions/migrations only when there is substantive owned content.
