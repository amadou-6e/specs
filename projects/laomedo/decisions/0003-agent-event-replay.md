---
title: Preserve agent-event redelivery uncertainty
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Preserve agent-event redelivery uncertainty

## Status and source

This is a reconstructed decision from the 2026-10-04 conversation following
the merged [EXP-05 evidence](../experiments/agent-evidence-crash/iterations/2026-10-03/results.md).
The user asked to continue after the assistant recommended T07's
at-least-once/explicit-uncertainty option. The exact transcript is not stored
here; [specs #202](https://github.com/amadou-6e/specs/issues/202) records the
selected scope. This record is draft pending review. No provider replay test
has yet validated implementation behavior.

## Context and alternatives

[T07](../subsystems/run-traces/design/decision-readiness.md) offered either a
producer-stable key required for deduplication or at-least-once receipts with
visible uncertainty. IF-08 source IDs are optional, and an ingest-assigned
receipt sequence changes on redelivery. Neither can establish that two
receipts represent one native action.

## Decision and scope

For the first-slice IF-08 agent-activity stream, preserve every committed raw
delivery and label action uniqueness **uncertain** unless a producer-stable key
has been independently verified for that source. A repeated-looking receipt
must not be presented as a confirmed new action; a conflicting payload must
not be collapsed. Counts of deliveries may be exact, but a unique-action count
must be absent or explicitly uncertain when identity is unverified. Receipt
sequence is order, not deduplication identity.

This does not select a producer-key contract, IF-07 lifecycle deduplication
(T10), raw writer/storage and durability (T01/T03/T04), or a production trace
implementation. The [run-traces contract](../subsystems/run-traces/contract/README.md)
owns the resulting target behavior.

## Consequences and verification

The first slice can ingest keyless provider streams without fabricating
uniqueness, but an action count may remain uncertain and repeated deliveries
remain visible. [EXP-09](https://github.com/amadou-6e/laomedo/issues/39)
must test keyed, keyless, reordered, conflicting and reconnect deliveries
against this policy before claiming replay handling works. The experiment is
synthetic and cannot prove a real provider supplies stable keys.

## Open questions

T10 remains a separate lifecycle-event choice. If a provider later offers a
verified stable event identity, a reviewed contract revision may introduce
source-specific deduplication without rewriting historical raw receipts.
