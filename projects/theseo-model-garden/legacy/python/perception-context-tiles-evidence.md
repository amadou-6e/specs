---
title: Frozen tiled spatial coverage evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-context-tiles.md
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/009-tiled-context/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/009-tiled-context/evidence/README.md
---

# Frozen tiled spatial coverage evidence

> This entry is historical, identity-bearing run evidence and is not an
> authoritative specification for new work.

## Archived material

This record preserves the outcome summary for study `voxel-context-tiles-v1`, run
`voxel-context-tiles-v1-run1`. It reports the tiled 33-cubed versus dense 65-cubed
quality and resource comparison conducted under protocol commit
`76bb3c403fb36b30ebf5335dcbc8f77005cf2db4` on source `c4f1787`.

## Why it was archived

The run is now represented by the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md),
specifically [iteration 009](../../experiments/encoder-continuation-and-context/iterations/009-tiled-context/README.md).
This copy remains intact because its run identity, measured values, artifact paths,
report hash, and bounded conclusions are historical evidence.

## Authority ended

This page ceased to be the active navigational owner when the tiled-context work was
migrated into the structured experiment. The exact migration date is not recorded in
the preserved evidence. New work must use the current experiment and applicable
subsystem contracts rather than extend this page.

## Current replacement

The canonical account is
[iteration 009 — Frozen tiled spatial-coverage diagnostic](../../experiments/encoder-continuation-and-context/iterations/009-tiled-context/README.md).
Its [evidence index](../../experiments/encoder-continuation-and-context/iterations/009-tiled-context/evidence/README.md)
links this record with the identity-bearing
[frozen protocol](perception-context-tiles.md).

## Continuing evidential value

The preserved text below is required to interpret the historical report, its SHA-256
identity, the reported quality intervals, and the measured memory/latency trade-off.
It supports audit and reproduction of that run; it does not promote tiled inference,
certify larger radii, or define current deployment guidance.

## Preserved evidence

Issues specs#51 / theseo-anysearch#376. Protocol commit
76bb3c403fb36b30ebf5335dcbc8f77005cf2db4; source c4f1787.
Run voxel-context-tiles-v1-run1,51.812 seconds including preparation. No fits.

All four noninferiority checks pass versus both dense controls. Same-head
comparison: surface gain intervals cross0; clearance/recovery improve about.0022.
Tiled versus adapted65 head: all four pilot intervals positive (not adjusted for
multiple comparisons). Tiled boundary F1 .6905/.6838/.7021; sampled central49,
not exhaustive output. Source heads, thresholds and normalization unchanged.

Dense65 encoder coverage21.8-23.5 ms/scene,176.60 MiB allocated peak. Tiled33
96.9-104.7 ms/scene,112.19 MiB. Tiling is4.1-4.8 times slower for36.5% lower
allocation; retain as memory option, not speed/default deployment. Profiles
exclude transfer, heads and stitching; no device-total or radius512 extrapolation.
Prefer dense where memory fits and retain shared frozen weights/33-context heads.

Implementation docs/perception-context-tiles-assessment.md and
docs/perception-encoder-local-geometry/tiles-report.json contain full evidence.
Report SHA2560923d9216166f5e2e9ef259a68b7f1723f1d848e4b5486e9d6830dcb8e740ed2.
Fresh parents disjoint from context65 corpus;36 prediction artifacts hashed.
Full garden418 passed before extra evidence replay test. No merges, promotion,
topology or planning claims. Disposition retain.
