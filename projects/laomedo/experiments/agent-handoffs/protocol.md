---
title: Two-agent chain protocol record
status: complete
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Two-agent chain protocol record

Retrospective record of the concrete harness and authorization used; this prose
was not committed/frozen prospectively. Do not treat it as a pre-registered protocol.
The user granted four additional turns total across #27/#28; coordination allocated
two to this chain, failures/timeouts included. A dedicated #28 runner ledger caps
two and privately links the untouched earlier native-node ledger at 7/8.

Agent A returns a specific instruction for agent B. The explicit Handoff node
passes selected task and source provenance to a fresh B. Success requires two
completed native runs, distinct threads, B's exact expected marker, durable B->A
provenance, independent workspace policy and ledger exactly 2/2. No retries.

Prior Docker image/config/auth posture stays unchanged; reuse existing private
profile without copying login credentials. No model-backed loop calls are in scope.
The harness writes full graph results outside Git; only sanitized identifiers,
hashes, marker and accounting are published.
