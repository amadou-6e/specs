---
title: EXP-01 filtered-readiness amendment results
status: complete
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Filtered-readiness amendment result

The [amendment plan](amendment-plan.md) and hand-checked [nine-case oracle](https://github.com/amadou-6e/laomedo/blob/de32cc8/experiments/exp01/oracle.json) were committed before the rerun. A fresh Laomedo 0.1.0 wheel from source revision `de32cc8` was installed into a new disposable Python 3.10.21 environment outside Git and executed via isolated Python (`-I`). The connector remained `github-gh-v1`, schema `1`; no product implementation code changed from the original run. No model turn, credential or GitHub access was used.

The amended probe compares each filtered item's readiness value with the handwritten oracle, in addition to item and edge membership. All nine corpus cases passed. Specifically:

| Case | Full graph | Filter to open `focus` items | Result |
| --- | --- | --- | --- |
| Original closed blocker | `P-101` closed; `P-909` ready | `P-909` ready; hidden `P-101 → P-909` context edge retained | Pass |
| New open blocker | `H-201` open; `H-202` blocked | `H-202` **blocked**; hidden `H-201 → H-202` context edge retained | Pass |

The new case would fail if filtering dropped the open blocker and promoted `H-202` to ready. Refresh retention and tamper rejection passed again, and the existing 12 Work Graph tests passed. The original [eight-case result](results.md) and its published JSON remain unchanged; the [sanitized nine-case JSON](https://github.com/amadou-6e/laomedo/blob/b2648e1b0f5803c149c12d45550ff44fd43eb9ed/experiments/exp01/result-amendment.json) records actual and expected values for each case.

This closes the specific filtered-readiness evidence gap for the synthetic corpus. It does not test live GitHub source access, cross-repository resolution or agent launch. The fixture and oracle were authored by the implementation author, separately from its development fixtures; no independent second party prepared them. The local wheel hash is an artifact identifier, not a byte-reproducibility guarantee. See the [evidence manifest](evidence/manifest.md) for exact pins and hashes.
