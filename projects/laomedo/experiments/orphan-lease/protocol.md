---
title: Orphan lease protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The user selected an independent stage lease supervisor plus a backend startup sweep for Q01/Q25, with a maximum tolerated exposure window of **60 seconds**. The canary service owns a disposable 256-bit test grant, accepts only local-network synthetic writes, enforces expiry independently, and records every accepted/denied write and revoke. While a pinned Langflow 1.12.3 backend is alive, an independent host supervisor renews the lease. A separate worker container keeps attempting writes. Hard-kill only the disposable backend; the supervisor must detect death, revoke the grant and stop the worker. Restart the backend with the same private state volume and confirm its run record is terminal crashed with no redispatch.

Measure from just before the backend kill to (a) the earliest confirmed grant end by revoke or expiry, and (b) observed worker exit. Both upper bounds must be no greater than the user-selected window. A post-death write with the same disposable grant must return 403. Record any accepted writes after kill and the final counter/trace state. If either bound fails, if revocation is unobserved, or if the worker remains alive, block live writable first-slice dispatch. No production repo, personal credential, real Git push or model turn is used. This is an experiment of an external-write grant; it does not prove every Git credential lane is covered.

The supervisor runs outside the fate-shared backend and retains no production Docker socket mount. The canary's expiry remains a fallback if the supervisor dies. Startup sweep reports the run state but does not substitute for the independent outage-time lease bound.
