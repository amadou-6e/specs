---
title: Compact C0-C3 smoke evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-encoder-compact-smoke.md
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md
---

# Compact C0-C3 smoke evidence

> This entry is historical and is not an authoritative specification. The original
> execution evidence is preserved below without normalizing its identity-bearing
> issues, revisions, hashes, run labels, limits, or reported outcomes.

## Archived material

This record captured the outcome of the bounded `compact-c0c3-smoke-v2` engineering
run governed by the adjacent archived smoke contract. It recorded the invalid v1
attempt, deterministic-pooling replacement, profiling and fit measurements, probe
outcomes, limitations, and prerequisites that remained before C4.

## Why it was archived

The smoke evidence became provenance for the engineering-screen iteration in the
structured compact perception-encoder campaign. That experiment now owns the
campaign chronology and current interpretation; this file retains the original
evidence wording and identities.

## Authority ended

By the 2026-09-22 structured migration, current interpretation moved to the compact
encoder campaign. This record does not independently authorize promotion, HPO,
scaling, threshold changes, or continuation beyond the historical smoke run.

## Current replacement

- [Compact encoder campaign](../../experiments/compact-encoder-campaign/README.md)
- [Engineering-screen iteration](../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md)
- [Engineering-screen execution](../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md)
- [Engineering-screen results](../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md)

## Continuing evidential value

Keep this record to interpret artifacts and later documents that cite specs issue 54,
Theseo AnySearch issue 379, governing protocol
`04673aba3906a50c9a51e4631ef910f8a3e767e7`, source revision `d34e534`, or report
payload `988ea76cf01b44252cfe3a6d3fc1ca87e2436486de36978a03d4330850eb5d61`.
The matching frozen protocol remains in the
[compact smoke contract](perception-encoder-compact-smoke.md).

---

## Preserved historical evidence

Specs#54 / implementation#379. Governing spec04673aba3906a50c9a51e4631ef910f8a3e767e7;
source d34e534. Campaign foundations remain PARTIAL; this is not HPO or a usable
compact encoder certification. No merges or promotion; #378 scaling is paused.

V1 failed deterministic CUDA adaptive pooling backward. Preserved incomplete;
explicit-bin deterministic replacement and fresh identities used in v2.
V2 completed18 profiles, six short128-dimensional training paths and fresh probes
in43.766 seconds including preparation. Trained grid/strided/attention aggregation
with both frozen and joint backbones, no spatial bypass into query heads.

Batch4 allocated peak108.3-109.0 MiB.96-step frozen fits2.406-2.547 seconds;
joint fits7.657-7.906 seconds. Short local profiles do not establish production
throughput, best aggregation or resource saturation. No precision/cache/concurrency
optimization yet. Only64/128/192 shape/profiling checks; no dimension-quality search.

Five configurations have zero thresholded occupied IoU and boundary F1 at0.5;
grid-joint gives.152/.138. Some null/shuffled controls match or beat distance
predictions. No selection from these scores. Next: class support/probe calibration,
learning curves and full controls, not larger fields or retroactive thresholds.

Required before C4: richer data/corruptions, raw/random/spatial controls, full
input contracts, steady-state batch/worker/cache/precision profiling and calibrated
numeric acceptance.48 GPU-hour budget not launched. No final evaluation accessed.
Implementation assessment: docs/perception-compact-c0c3-assessment.md.
Report payload988ea76cf01b44252cfe3a6d3fc1ca87e2436486de36978a03d4330850eb5d61.
