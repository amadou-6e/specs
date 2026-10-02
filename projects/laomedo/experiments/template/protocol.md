---
title: Snapshot-rejection protocol example
status: template
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Snapshot-rejection protocol example

Illustrative prospective design, not frozen/executed. Hypothesis: absent snapshot returns
mismatch and leaves ledger unchanged. Control: synthetic run with matching thread/profile
and accessible snapshot. Negative condition: hold only its snapshot, request matching
resume, capture response/counters, restore snapshot. A synthetic dispatcher avoids model cost.

Metrics: error category, dispatch count, reservation count, restored hash. Proposed gate:
any dispatch/reservation fails; absent evidence is inconclusive. Fixture-path substitution
is allowed before freezing; runtime change requires new protocol revision. Resources:
disposable fixture, zero model turns in this deterministic design, no credentials or
personal sessions. A real copy records authorizing review and frozen implementation pins.
