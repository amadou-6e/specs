---
title: Agent-event replay results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Synthetic case | Committed deliveries / display records | Action uniqueness | Stream | Observation |
| --- | ---: | --- | --- | --- |
| Identical source-ID redelivery after reopening store | 2 / 2 | uncertain; count absent | complete | Both payload digests equal; neither delivery collapsed |
| One source ID, conflicting payloads | 2 / 2 | uncertain; count absent | complete | Both summaries and distinct digests retained |
| Keyless result-before-call plus redelivery | 3 / 3 | uncertain; count absent | partial | Receipt order is result, call, result after restart sweep; all expose `call-1`, but no link is inferred |
| Same source ID in two invocations | 1 / 1 per invocation | uncertain; count absent | complete in each | Separate histories retain call and result with shared source ID and `call-2`, without a cross-invocation link |

Reprojecting each case twice left raw receipts and stored projection rows
unchanged. A completed stream still had an unknown unique-action count;
completeness did not imply action identity. Receipt sequence ordered
deliveries, not provider actions. The sanitized [observation](evidence/manifest.md)
contains synthetic summaries and hashes, not native provider payloads.

The amended run applied the same delivery/uncertainty oracle to a negative
control. The historical #123 projector retained only **1 of 2** identical
reconnect deliveries and rejected the two distinct payloads sharing an ID.
The oracle also rejected a fabricated `verified` uniqueness/count assertion.
These failures show that the amended checks detect those specific invalid
projections; they do not establish native-provider replay behavior.

This passes the **bounded synthetic** T07 oracle, including the disclosed
negative control at Laomedo `e285068`. It does not establish that
real Codex/Claude events redeliver in this way, supply stable IDs, or that a
production trace adapter and UI render uncertainty. IF-07 lifecycle T10,
power-loss durability, and the raw writer/storage decisions remain open.
