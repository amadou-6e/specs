---
title: EXP-01 results
status: complete
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Frozen case | Independent expectation | Observed |
| --- | --- | --- |
| Two-page closed blocker | Stable IDs distinguish issue numbers; duplicate native edge collapses; closed prerequisite makes open dependent ready; filtered dependent retains hidden context | Pass |
| Cross-repository and textual reference | Native outside blocker remains an edge with its repository and URL; readiness unknown; body text creates no edge | Pass |
| Truncated and null connections | Missing label, blocker and issue nodes produce warnings and incomplete source; open item unknown | Pass |
| Interrupted second page | Partial source is incomplete, with fetch/pagination/count warnings; open item unknown | Pass |
| Unavailable repository | No fabricated item; incomplete source and explicit warnings | Pass |
| Cycle, self-loop and downstream item | Three cyclic members, one blocked downstream item and one isolated ready item | Pass |
| Refresh before and after | Same stable ID, changed source marker/state, distinct immutable artifact IDs; old and new both readable | Pass |
| Artifact tamper | A changed title under the saved digest is rejected | Pass |

All eight corpus cases matched the separately committed oracle exactly. The native provenance marker was preserved on each edge; source issue URLs, bodies, update markers, labels and numbers matched the response pages. The snapshot refresh produced two distinct digests and the tampered artifact raised `ValueError`. The existing Work Graph unit suite ran separately: 12 tests passed.

This first result did not compare projected item readiness, and its filtered case hid a closed blocker. It therefore did not, by itself, establish that filtering preserves readiness from the complete graph. The [amendment](amendment-results.md) retains this original result and tests the missing open-blocker case.

This tests the imported GraphQL response shape, not a live GitHub query or the account's access to private issues. Cross-repository dependencies deliberately remain unresolved unless their source is available; an open dependent is `unknown`, not ready. Readiness is inspection data and does not authorize dispatch. The synthetic corpus was prepared by the implementation author without reusing development fixtures, not by an independent second party.
