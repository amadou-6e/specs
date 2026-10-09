---
title: PR-check feedback protocol chronology
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol chronology

This is a post-run index of prospective frozen records, not a new preregistration.
Original [protocol](https://github.com/amadou-6e/laomedo/blob/bcc2fbceb7a9f7e048a92401ed0e9ef3fb7f19db/experiments/exp123/PROTOCOL.md)
preceded code. [Amendment 01](https://github.com/amadou-6e/laomedo/blob/44a6d238bee6c59ed6a9f0e5c46b06d32271f390/experiments/exp123/AMENDMENT-01.md)
selected a custom polling wait, conditional branch and unrolled two-agent cap
before implementation. It pins governing specs `86d6fcff5c6d51e6ad106daf59f3f7036c7f9e8b`.
The [S1 pre-run record](https://github.com/amadou-6e/laomedo/blob/029c9e0/experiments/exp123/S1-PRE-RUN.md)
pins source `f5b2e9a257fe59e3f281300358d209c41546b76a` before independent execution approval.

Seven single-dispatch cases: success, early success, unknown/pending then pass,
H1 failure/H2 pass with duplicate/conflict/stale controls, two-failure cap,
controller Stop, and backend death. Fail if a second graph or extra agent is
dispatched, a wrong head decides the gate, evidence cannot be reconstructed,
or cleanup is unverified. Zero models/provider writes; no automatic retry.
Gate limit 12 seconds, HTTP timeout 1 second, poll 0.1 seconds, controller
wait limit 25 seconds and post-terminal observation 1 second. The controller
limit is per wait rather than per case, a disclosed pre-run review deviation.
