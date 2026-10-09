---
title: Visible Playground host-bridge seam bounded result
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded result

The [Laomedo result at `6c6bf37`](https://github.com/amadou-6e/laomedo/blob/6c6bf37558fbafb2697f6e6c279a19cdcad49a5c/experiments/exp22/PHASE-G-SEAM-RESULTS.md)
reports one visible Send reaching a fake host bridge. The fake wrote one
synthetic runner binding into `WorkflowRunStore`; reopening its SQLite file
found that binding and a cancel receipt. After the visible Stop click, the
fake observed a lookup by the same client UUID followed by an exact cancel
before the browser closed. A host-side fake self-test returned 202 for the
same body and 409 for a changed body. Those status codes do not demonstrate
product bridge retries. The client UUID differed from the host-minted
invocation ID; the synthetic runner request used that invocation ID.

This is positive evidence for a visible first-call and Stop routing seam only.
There was no separate runner POST or acknowledgement, native cancellation,
executing-graph attestation, Langflow restart, or durable cross-store trace
join. The host graph record came from the repository fixture. The browser
observer saw the build monitor, not the exact Send endpoint. The shared ledger
remained **6/12** with zero model calls; container and fake bridge teardown
passed. #22/Q11 remain open.
