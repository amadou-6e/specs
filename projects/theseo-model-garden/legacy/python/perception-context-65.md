---
title: Memory-first frozen 33-to-65 context pilot
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/README.md
  - perception-context-65-evidence.md
---

# Memory-first frozen 33 to 65 context pilot

> This entry is a historical, identity-bearing protocol and is not an authoritative
> specification for new work.

## Archived material

This record preserves the frozen protocol for study `voxel-context-65-v1`, run
`voxel-context-65-v1-run1`. It defined a memory-first pilot comparing frozen
65-cubed and 33-cubed local-geometry context with unchanged continuation encoders.

## Why it was archived

The protocol and its outcome are now represented by the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md),
including [iteration 008](../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/README.md).
The archival copy remains intact because its study and run identities, scene IDs,
seeds, hashing rules, resource gates, and comparison thresholds are historical
evidence.

## Authority ended

This page ceased to be the active owner when the 33-to-65 pilot was migrated into
the structured experiment record. The exact migration date is not recorded in the
preserved protocol; new work must use the current experiment and relevant subsystem
contracts rather than extend this page.

## Current replacement

The canonical account is
[iteration 008 — Memory-first 33-to-65 context pilot](../../experiments/encoder-continuation-and-context/iterations/008-context-33-to-65/README.md).
Its execution, results, and evidence index provide the current navigational entry
points. The original run evidence is preserved separately in
[perception-context-65-evidence.md](perception-context-65-evidence.md).

## Continuing evidential value

The text below records the original corpus construction, query sampling, probe
training, CUDA-memory fallback, bootstrap comparison, and decision gates. It remains
necessary for interpreting the historical report and reproducing the
identity-bearing run. It must not be read as authorization for new 65-cubed runs or
as a current model-promotion decision.

## Preserved protocol

Issues specs#49 / theseo-anysearch#374. Authorized unmerged stack on #372 and
specs#48; no merge or promotion. Prior protocol b950249860b3e33640e9faadc3fe0a7ecabc92fc.
This is a separate local-geometry pilot, not a reopening of topology gates.

## Frozen design

Study/run `voxel-context-65-v1` / `voxel-context-65-v1-run1`. Fresh scene IDs
`voxel-context-65-v1-data-<split>-<index>`. Train48 / selection24 / assessment48,
balanced over random_field and oblique_sheets, densities 0.08/0.16/0.28.
Generate81-cubed parents, crop65 and33 at identical spacing, query central17 only.
Use the previous generators with parent coordinates -40..40 divided by8; Gaussian
sigma1.5 reflect; oblique absolute sine frequency uniform[4,8], random unit normal
and phase uniform[-pi,pi]. Threshold the parent quantile once, never per crop.
Seed NumPy with first8 little-endian SHA256 bytes of scene ID. Parent targets:
boundary and signed distance truncated/divided by8. Shared20% hidden mask seeded
from scene ID plus `-mask`. Parent margin8 beyond65 preserves target support.

Query256 eligible central cells/task/parent, replacement only for undersized
nonempty pools, RNG37400+split index (train, selection, assessment). Occupancy and
boundary use hidden cells; clearance visible free, recovery hidden free. Reject
duplicate parents and fewer than20 instances of either class in any binary
family/split pool. Hash parents, input arrays, targets and queries before fitting.

Use the three validated continuation encoder checkpoints unchanged (seeds0/1/2),
with file/state hashes verified against the continuation report. No encoder
updates. Each scale/task/seed receives its own fixed32-hidden probe, same train
queries and1024 updates, AdamW0.001/wd0.01, batch1024, train-only normalization.
Choose classification thresholds on selection F1 over0.01..0.99, lower ties;
distance predictions clamp[0,1]. Encoder states must remain unchanged.

## Memory-first execution

Keep corpus on CPU and stream only each forward batch to CUDA. Before any fitting,
profile both scales for all three encoders at batch4 (3 warmups,20 synced timed
forwards). Maximum total CUDA allocated peak6 GiB. If any profile exceeds this or
raises CUDA OOM, discard batch4 profile set, clear cache, and repeat all profiles
at common batch1. If batch1 fails, record `resource_limited` and no quality verdict.
No other fallback or parameter tuning. All feature extraction uses the common
accepted batch. Do not preload targets/volumes on CUDA. Use float32, deterministic
algorithms, no TF32/cuDNN autotuning, CPU threads4. Timings are local pilot
measurements; allocated memory is not total device usage. Record incremental peak
as well as total, and batch-choice attempts. Overall7200 seconds including manifest
preparation, checked between bounded operations/probe fits. Invalid/incomplete runs
cannot establish quality. No65 encoder training is authorized by this protocol.

## Decision and limits

Compare frozen65 versus frozen33 by whole-parent paired bootstrap within six
family/density strata,2000 draws, seed372 retained from the prior comparison
helper. Report all seed scores, family scores, and95% improvement intervals.
Noninferiority lower bound >=-0.03 classification or >=-0.02 distance. Positive
lower bounds indicate added-context benefit; noninferiority alone does not.
Retain shared weights if all four checks pass, but prefer33 if65 adds no clear
quality benefit at higher resource cost. A task regression directs a targeted
diagnostic; it does not erase earlier evidence. Memory failure directs streaming,
tiling or sparse/multiscale design under a new protocol. Any larger-scale run or
method change needs a new contract. No full65-volume, radius512, topology,
planning, universal generalization or promotion claim. Scale-adapted heads are
not unchanged-head transfer. Pin source/spec commits before fits; commit compact
report/artifact hashes only, never corpora or weights.
