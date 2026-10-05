---
title: Work Graph dispatch-binding protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Prospective protocol

## Question and scope

Can a selected immutable Work Graph item and graph snapshot become a frozen mock-runner input while freshness, prerequisite and grant checks are repeated immediately before dispatch? EXP-01 [#50](https://github.com/amadou-6e/laomedo/issues/50) verified source integrity at a synthetic scope. EXP-02 [#32](https://github.com/amadou-6e/laomedo/issues/32) verified selected-issue context, EXP-04 [#34](https://github.com/amadou-6e/laomedo/issues/34) verified synthetic durable reservation, and EXP-03 [#33](https://github.com/amadou-6e/laomedo/issues/33) failed native component revision identification. Use those results as inputs; do not reinterpret EXP-03 as a pass.

Freeze the Laomedo source and specs contract revisions, connector/schema versions, fixture bytes, a hand-written expected matrix, mock grant fields and fixed clock before executing. Use the installed package, not only source-tree unit tests. Import synthetic GitHub response pages and preserve immutable snapshot artifacts, run records, invocation events and a sanitized per-case comparison. No live GitHub read or write, real agent, model turn, PR write, or production grant.

## Required observations

The preflight must operate on the complete snapshot, not a filtered projection. It must compare a selected snapshot with current source evidence at dispatch. Any change requires an explicit `pinned` or `refreshed` choice; a pinned choice retains the old work/input refs, a refreshed choice binds the current refs. Acknowledging staleness cannot silently override a newly opened blocker or an incomplete source. An override is considered only for a complete, known, open prerequisite; it identifies the exact edge and contains nonempty rationale. Unknown or cyclic prerequisites remain refusals. A mock grant is valid only when authorized, unexpired at the fixed clock, and bound to the selected work/graph ref and mock runner; this tests binding fields, not production grant cryptography.

Every accepted case must persist work key, source URL/update marker, graph snapshot ID, frozen input digest, definition and mock component revisions, choice and any override evidence before one mock dispatch. Read the durable run and retained trace after dispatch and compare them to the selected refs. A runner refusal or unknown outcome must keep the run/trace identity and must not be automatically retried. Every rejected case must have zero mock dispatch calls and a specific refusal reason.

## Frozen case matrix

| Case | Expected decision |
| --- | --- |
| Fresh ready item with valid grant | One dispatch with selected work, graph and input refs retained |
| Source text/update marker changed, no choice | Refuse staleness before dispatch |
| Ready source changed, explicit pinned choice | Dispatch old work/graph/input refs; record pinned acknowledgement |
| Ready source changed, explicit refreshed choice | Dispatch current work/graph/input refs; record refreshed choice |
| Newly opened blocker, pinned or refreshed choice without override | Refuse despite explicit freshness choice |
| Known open blocker with exact-edge rationale and valid grant | One mock dispatch; record exact edge and rationale |
| Missing rationale or wrong-edge override | Refuse before dispatch |
| Hidden open blocker in filtered view | Refuse; projection does not change full-graph readiness |
| Unresolved external blocker, cycle, or incomplete source | Refuse, even if an override is offered |
| Expired, wrong-work, wrong-graph, wrong-runner or unauthorized grant | Refuse before reservation or dispatch |
| Mock runner rejection or uncertain outcome | Preserve one durable run/trace identity and partial/unknown status; never replay |

Run one valid case as a control, mutate one field per negative case where possible, and retain expected versus observed outcomes. The no-dispatch claim requires a mock invocation counter and durable store counters, not just an absent output file. A mismatch, missing frozen ref, untracked override, or unsafe dispatch is a no-go. Passing this matrix is a **bounded mock-binding result**, not acceptance of the real stage adapter or native component attestation. Keep EXP-03's failure and #77 as a separate integration limit.
