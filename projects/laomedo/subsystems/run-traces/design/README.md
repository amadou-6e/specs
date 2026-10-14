---
title: Run traces design
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Run traces design

Persist raw events before derived display records. Preserve native IDs and receipt order. Synthetic projection tests exercise duplicate and missing-value handling; they do not establish provider reconnect behavior.

Reconstructed from local specs and evidence reports; implementation was not re-executed
or independently verified by this migration. [Validation](../validation.md) pins the
observation boundary. Public behavior belongs to [contract](../contract/README.md).
Design container: README.md (1), focused mechanism pages (0..*). No language partitions
are needed for currently inspected material.

The [decision-readiness ledger](decision-readiness.md) tracks raw-writer,
deduplication, crash-prefix and retention choices without claiming the
synthetic projection tests prove provider replay or hard-crash durability.

The user-selected [Agent activity viewer](agent-activity.drawio) is a bounded
native Codex inspection modal: invocation history, capture status, usage and
ordered native receipts. It does not settle the deferred multi-agent layout.
