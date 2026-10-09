---
title: PR-check feedback S1 results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Result and limits

Bounded candidate passed. Success/early/pending: one agent, Result1 passed.
Repair: two agents, H1 failed/H2 passed, Result2 passed. Cap: two agents, both
checks failed, Result2 failed while graph execution completed. Stop: interrupted,
one agent; crash: crashed, one agent. Exactly one graph per case. All component
records joined that graph ID. Failure branch selection preceded Agent2; neither
Stop nor crash produced a gate decision or corrective invocation, and both late
deliveries were explicitly inactive. Capture and cleanup checks passed.

This establishes a custom polling wait/router on Langflow 1.12.3 with an unrolled
cap, not built-in webhook waiting, arbitrary loops, production ingress security,
real-agent PR readback or the visible UI Stop. The flow was frozen after graph
construction and before arun, so it may include construction-time mutation.
Controller deadlines applied per wait; no deadline fired. Synthetic /node ingress
was unauthenticated, source mount included cached bytecode, and outbound network
access was not blocked. These limits were disclosed before interpretation.

The [implementation result](https://github.com/amadou-6e/laomedo/blob/4ab1d55cf0efed6de96ebbb045b808044cfa31cb/experiments/exp123/S1-RESULTS.md)
and [byte manifest](evidence/manifest.md) retain the complete observations.
Active-agent delivery and production event handling remain unverified.
