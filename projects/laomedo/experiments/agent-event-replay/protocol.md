---
title: Agent-event replay protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The [source protocol](https://github.com/amadou-6e/laomedo/blob/c3b46f9a1f9ef4e2b35d5e6a7102615e9eb632de/experiments/exp09/PROTOCOL.md)
was committed at `c3b46f9` **before** the probe ran. This page indexes that
frozen design; it does not retroactively change thresholds.

The hypothesis was that receipt-backed projection can preserve every
committed IF-08 delivery while leaving native action identity uncertain. It
would fail if a committed receipt vanished, a conflicting payload collapsed,
an unverified source ID or receipt sequence became a unique-action key, or
stream completeness was inferred from identity certainty.

The frozen cases covered identical redelivery across a new SQLite store
instance, conflicting payloads with one source ID, keyless result-before-call
and redelivery followed by a crash sweep, the same source ID in separate
invocations, and idempotent reprojection. The planned environment was a
temporary SQLite WAL database with `synchronous=FULL`, synthetic payloads,
no model turns, and no provider, network or GitHub write in the probe. The
selected draft oracle was specs `6b614e34eac93dea31ce4e80143c001fb4cdd066`.

The exact file and source revision are in the [evidence manifest](iterations/2026-10-04/evidence/manifest.md).
