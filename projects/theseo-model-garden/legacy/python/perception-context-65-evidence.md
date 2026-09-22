---
title: Frozen 33-to-65 context evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-context-65.md
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/execution.md
  - ../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/results.md
  - ../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/evidence/README.md
  - ../../subsystems/encoder-models/README.md
---

# Frozen 33-to-65 context evidence

> This entry is historical, identity-bearing evidence and is not an
> authoritative specification for new work.

## Archived material

This record preserves the compact outcome and integrity evidence for study
`voxel-context-65-v1`, run `voxel-context-65-v1-run1`. It identifies the governing
protocol revision, executable revision, measured quality and resource outcomes,
bounded interpretation, and report payload identity for the frozen 33-to-65 context
pilot.

## Why it was archived

The pilot is now represented by the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md),
specifically [iteration 008](../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/README.md).
This page remains in place because its historical hashes, issue references, run
identity, summary measurements, disposition, and artifact path are evidence used to
interpret that completed run.

## Authority ended

This page ceased to be the active account when the pilot was migrated into the
structured experiment record. The exact migration date is not recorded in the
preserved evidence. New work must use the current experiment and applicable
[encoder-model contracts](../../subsystems/encoder-models/README.md).

## Current replacement

The canonical structured account is
[iteration 008 - Memory-first 33-to-65 context pilot](../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/README.md).
Its [execution](../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/execution.md),
[results](../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/results.md),
and [evidence manifest](../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/evidence/README.md)
own the current structured description. The matching
[frozen protocol](perception-context-65.md) remains archived alongside this evidence.

## Continuing evidential value

The preserved text below records the exact protocol and executable revisions,
reported confidence intervals, resource observations, elapsed time, report payload
identity, disposition, and limits on promotion claims. These details support audit
of the migrated experiment and old artifacts; they do not authorize another run or
establish current model behavior.

## Preserved evidence

Issues specs#49 / theseo-anysearch#374. Governing protocol commit
2f9fa46f3c26f96b9f0e1c05f9fa101a09923ad3. Run voxel-context-65-v1-run1,
source f848db6 (authorized unmerged stack). No merges or promotion.

All four noninferiority checks pass; no gain interval excludes zero positively.
Occupied IoU improvement CI[-.00124,.00678], boundary F1[-.00551,.00883],
clearance error improvement[-.000527,.000482], recovery[-.000571,.000523].
Shared frozen encoder weights support65 central queries, but added context has
no demonstrated benefit over33. Separate adapted heads; no full-volume claim.

Batch4 accepted, total peak CUDA allocation107.70/610.98 MiB at33/65. Forward
latency13.25-15.60/86.70-86.75 ms per batch; local non-isolated measurements.
Elapsed84.797 seconds including preparation. No encoder updates. Corpus on CPU.
Prefer33 for this local task; next investigate tiled wider-output quality/cost
under a fresh contract, without assuming overlap or spatial norms are harmless.

Implementation report: docs/perception-context-65-assessment.md;
machine evidence: docs/perception-encoder-local-geometry/context65-report.json.
Payload SHA25636fef437a4d62fd505e27c39cba7b58c393bc2ca1d387e426d96f0f9ce12704c.
Disposition retain. Topology/P1-P8 remain separate; no certification or promotion.
