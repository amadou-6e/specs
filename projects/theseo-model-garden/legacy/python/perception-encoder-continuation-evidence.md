---
title: Encoder continuation and retention evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-encoder-continuation.md
  - perception-distance-retention.md
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/results.md
  - ../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/evidence/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/005-distance-retention/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/005-distance-retention/results.md
  - ../../experiments/encoder-continuation-and-context/iterations/005-distance-retention/evidence/README.md
  - ../../subsystems/encoder-models/README.md
---

# Encoder continuation and retention evidence

> This entry is historical, identity-bearing evidence and is not an
> authoritative specification for new work.

## Archived material

This record preserves the combined result summary for the fixed-architecture encoder
continuation and its subsequent distance-retention check. It records the reported
measurements, protocol and source revisions, report payload identities, disposition,
and stated limits on what the two studies established.

## Why it was archived

The two studies are now represented by the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md),
specifically [iteration 004](../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/README.md)
and [iteration 005](../../experiments/encoder-continuation-and-context/iterations/005-distance-retention/README.md).
This page remains in place because its historical hashes, issue references, compact
outcomes, and bounded interpretation are evidence used to audit those migrated
records.

## Authority ended

This page ceased to be the active account when the continuation and retention work
was migrated into the structured experiment. The exact migration date is not
recorded in the preserved evidence. New work must use the current experiment and
applicable [encoder-model contracts](../../subsystems/encoder-models/README.md).

## Current replacement

The current structured accounts are:

- [004 — Fixed-architecture encoder continuation](../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/README.md),
  including its [results](../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/results.md)
  and [evidence manifest](../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/evidence/README.md).
- [005 — Frozen distance retention](../../experiments/encoder-continuation-and-context/iterations/005-distance-retention/README.md),
  including its [results](../../experiments/encoder-continuation-and-context/iterations/005-distance-retention/results.md)
  and [evidence manifest](../../experiments/encoder-continuation-and-context/iterations/005-distance-retention/evidence/README.md).

The matching [continuation protocol](perception-encoder-continuation.md) and
[distance-retention protocol](perception-distance-retention.md) remain archived
alongside this evidence.

## Continuing evidential value

The preserved text below supplies the exact protocol revisions, executable source
revisions, report payload hashes, reported per-seed measurements, confidence
intervals, and interpretation limits behind the migrated results. It supports audits
of the old candidate encoders and reports; it does not authorize promotion, claim a
single causal pretraining factor, or establish current model behavior.

## Preserved evidence

Implementation issues#366/#368; specification issues#41/#43. No merges/promotion.

Three new same-architecture encoders completed2048 joint occupancy/ESDF updates.
At matched192-geometry probe exposure, boundary F1 rose from0.6343/0.6129/0.6239
to0.7380/0.7328/0.7374. Paired loss improvement CI[0.04678,0.06215].
Surface protocol4349ad2ac47cbad912a7a984407f97bbd9042628, source2423714.
Report payload3756d04628a9c6e377e9ae67853ac440fe4afeae46ae4160ea064d8965710390.

Fresh frozen-distance validation also completed: clearance errors new
0.0308/0.0320/0.0361 versus old0.0487/0.0492/0.0512; recovery new
0.0309/0.0324/0.0360 versus old0.0485/0.0503/0.0504. Both pass the preregistered
retention rule and have negative paired new-minus-old error intervals.
Retention protocol762262d657b4320dbce39d3b53bc028105a2896b, source577da2e.
Report payload01c0be1f42549c7c6a4638638e8a5a48120f3f3daee1c0d6a41098ad119bf577.

Retain new encoders as local-geometry candidates for new-family validation.
Architecture/probe exposure matched, pretraining histories did not. Old LG2 also
used dynamic masks; these results do not isolate a single pretraining factor.
No unseen-family, topology, occupancy-retention, planning or radius claims.
Full implementation assessments: docs/perception-encoder-continuation-assessment.md
and docs/perception-distance-retention-assessment.md. Weights remain untracked.
