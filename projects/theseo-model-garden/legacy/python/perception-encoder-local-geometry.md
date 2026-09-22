---
title: Local-geometry encoder study LG1
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/local-geometry-encoder/README.md
  - ../../experiments/local-geometry-encoder/iterations/lg1/README.md
  - ../../subsystems/encoder-models/README.md
  - ../../subsystems/pretraining-and-qualification/README.md
---

# Local-geometry encoder study LG1

> This entry is a preserved historical protocol and is not an authoritative
> specification for new Model Garden work. Its frozen identities, gates, and
> claims remain unchanged as evidence of the registered LG1 study.

## Archival context

This page preserves the prospective LG1 protocol, including its original scope,
registration identities, engineering gates, and links to completion evidence. Its
active authority ended when LG1 completed and the local-geometry program was
reconstructed under the structured
[local-geometry encoder experiment](../../experiments/local-geometry-encoder/README.md).
The exact historical authority remains the immutable registration commit identified
below; this relocated copy must not be used to revise that protocol retrospectively.

Use the [LG1 iteration](../../experiments/local-geometry-encoder/iterations/lg1/README.md)
for the current experiment narrative and evidence map. Current reusable encoder
behavior belongs to the [encoder-model contract](../../subsystems/encoder-models/README.md),
while current qualification rules belong to
[pretraining and qualification](../../subsystems/pretraining-and-qualification/README.md).
This archive remains valuable for interpreting the LG1 report, assessment, model
artifacts, hashes, and historical pass/fail decisions.

Status: preregistered engineering screen, not encoder certification.
Implementation: `amadou-6e/theseo-anysearch#341`; specification: `amadou-6e/specs#29`.

## Authority and scope

The carve-out in `perception-encoder-pilots.md` at merged specs commit
`0060366f43892bade5acf734cf2e189d8a666ad2` governs this separate program:
`voxel-encoder-local-geometry-v1`. The user explicitly authorized independent
execution on 2026-09-08 before review/merge of implementation #352 and specs #28.
This is an ordering exception, not permission to merge either PR or import its
unmerged R0 implementation. Source starts from merged integration commit
`2844775ffda682c51d414a3b8f80e01b8d958975`.

The recorded R0 result remains `no_topology_identifiable`; LG1 neither repairs nor
overrides it. No result advances P1-P8. Claims concern frozen **local features**
for occupancy, boundary, clearance and clearance recovery only. No connectivity,
planning, topology, wide-context, global-embedding or architecture-selection claim
is authorized. The global projection receives no local-loss gradients and is
explicitly excluded from optimization and qualification.

## Question and candidates

Does occupancy or signed-distance pretraining produce reusable local features
under an equal small compute budget? Use one existing dense mask-aware partial-
convolution residual pyramid, stem width 8, stage widths 8/16/32/64, eight local
channels and its existing lateral interpolation decoder. This dense fallback
does not claim sparse-execution savings. Compare two objectives, seeds 0 and 1
each, paired at identical encoder initialization. There is no architecture sweep.

Both recipes discard a disposable 1x1x1 single-output convolutional head after
pretraining. Occupancy uses unweighted binary cross-entropy with logits; ESDF uses
Smooth L1 against signed distance clipped to +/-8 voxels and divided by 8.
Both supervise only independently hidden cells, with no boundary weighting.
Class imbalance is an explicit limitation of the occupancy recipe, not a reason
to tune its weighting after seeing results.

## Fresh identities and splits

- Study: `voxel-encoder-local-geometry-v1-lg1`.
- Dataset: `voxel-encoder-local-geometry-v1-dataset-1`.
- Queries: `voxel-encoder-local-geometry-v1-queries-1`.
- Runs: study ID followed by `-occupancy-seed-0`, `-occupancy-seed-1`,
  `-esdf-seed-0`, or `-esdf-seed-1`.
- Preregistration: write-once canonical payload hash pinning this spec's exact
  commit, executable source commit, resolved plan and all geometry IDs.
- Report: its own canonical payload SHA and hashes of untracked model artifacts.

There are 96 encoder-training, 48 probe-fitting and 48 evaluation geometries,
mutually disjoint by identity. Each split is evenly allocated across all 12
family/density strata: `open`, `thin_obstacle`, `topology`, `imported`, crossed
with low/medium/high occupancy bands. These are existing **procedural** native
voxel generators: `imported` is the historical name for synthetic ellipsoids,
not real imported data; `topology` is a wall generator, not a topology target.
Use the new program seed namespace with no prior-study corpus/query reuse.

Each geometry supplies observation index 1, radius 8 (17x17x17 cells). Existing
crop selection ensures some occupied cells; this is not an unbiased natural-world
sample. No external generator or domain-transfer claim is made. Clean crops are
required; no built-in unknown slab is used. Masks are independent Bernoulli(0.20)
at native cells, independent of labels. Training resamples masks each update.
Probe/evaluation use fixed independent masks, seeded 34101/34102. All candidates
share the resulting query banks. Hidden values in every input channel are excluded
by the existing partial-convolution support path. Missing-cell recovery is a
synthetic corruption test, not an embodied visibility model.

## Frozen budgets and probes

Train each encoder for exactly 1,024 updates, batch 8, AdamW learning rate 0.001,
weight decay 0.01, FP32, no scheduler/early stopping/AMP/compile or tuning.
Training sample/mask stream is seeded 34100 + initialization seed, shared between
objectives. All four encoders finish training before evaluation materialization.
Use CUDA with deterministic algorithms, TF32 disabled and four CPU threads.
Total wall-time cap: four hours. An invalid corpus, numerical failure, unsupported
deterministic operation or cap breach produces an incomplete run, not a pass.
Development fixtures must use separate development identities and cannot inform
study hyperparameters from the sealed evaluation data.

Freeze the encoder, hash its parameters/buffers and extract local features.
Discard all pretraining heads. Fit a fresh eight-input MLP probe per task:
Linear(8,32), SiLU, Linear(32,1). Fit feature mean and standard deviation on the
probe-fitting split only; clamp standard deviation at 1e-5. Fit each probe for
512 updates of 1,024 query samples, AdamW lr 0.001, weight decay 0.01. Binary
targets use BCE-with-logits; normalized clearance targets use Smooth L1. No
probe/checkpoint selection or evaluation-dependent threshold: final checkpoint,
classification threshold 0.5, regression predictions clipped to [0,1].

Uniformly query 256 eligible cells per geometry/task, without replacement where
possible, otherwise with replacement; do not balance queries by target label.
Occupancy and boundary query hidden cells. Clearance queries observed ground-truth
free cells. Recovery queries hidden ground-truth free cells. Free-only selection
defines a conditional error metric; it cannot be interpreted as free-space
classification accuracy. Fail as invalid if any eligible pool is empty or either
classification task has fewer than 100 positive or 100 negative query rows in
either probe-fitting or evaluation split. Do not redraw a failed corpus.

Targets are computed from the clean crop using existing geometry utilities:
occupied boundary is an occupied voxel adjacent to a free six-neighbor. Report
exact binary boundary F1 with **no spatial tolerance** across queried rows.
Clearance is positive signed distance clipped at eight voxels, divided by eight;
recovery uses the same target at hidden-free queries. Distances are crop-local,
not a full-world clearance guarantee. No topology labels are used.

## Controls and validation bars

Each seed uses a paired random encoder with the exact same initial state and the
same separately fitted probe architecture/budget. For each trained probe evaluate
zeroed and row-shuffled features (before train-only normalization). Also fit a
probe on globally shuffled probe-training labels with the same capacity, update
budget and minibatch sequence, and evaluate against true held-out labels.

Diagnostic only: fit a 32-hidden-unit raw-neighborhood MLP on visible 3x3x3
occupied/free/unknown channels (81 inputs), with the same optimization budget.
Its parameter count differs, so it is not a capacity-matched superiority gate.
An exact full-information target oracle establishes metric endpoints; it is not
a trained reference. There are no empirical ceilings or headroom normalizations.

These **engineering screening thresholds** are not literature-established minima
for deployment or planning. A recipe qualifies for a local follow-up only if all
four tasks pass in **both** seeds:

| Component | Absolute bar | Improvement over each control |
| --- | --- | --- |
| Hidden occupied IoU | >=0.60 | >=0.05 absolute |
| Hidden exact boundary F1 | >=0.70 | >=0.05 absolute |
| Observed-free clearance NMAE | <=0.15 | >=10% relative error reduction and positive gain |
| Hidden-free recovery NMAE | <=0.20 | >=10% relative error reduction and positive gain |

Controls in this gate are random encoder, zeroed features, shuffled features and
shuffled-label probe. Additionally each two-seed mean paired gain must have a
strictly positive lower 95% percentile geometry-bootstrap bound. Use 2,000 draws,
seed 341, resampling four geometries with replacement independently inside each
of the 12 evaluation strata. Share each draw across seeds and compared methods.
For IoU/F1 sum geometry confusion counts and recompute the ratio; for NMAE sum
absolute error and query counts. Average the resulting scores across the two
seeds, not predictions. These intervals describe geometry uncertainty conditional
on two seeds; they do not estimate training-seed population uncertainty. No
max-over-strata, recipe selection on evaluation, or composite score is used.

Hard integrity checks: unchanged frozen encoder hash, exactly zero hidden-value
mask-isolation difference, finite losses/predictions, centered local-feature
covariance entropy effective-rank fraction >=0.25, and at most 5% of local
dimensions with evaluation standard deviation <1e-5. Rank is over queried local
features, not the excluded global projection. Report each check and failure;
do not relax gates if neither recipe qualifies.

## Assessment and publication

Publish compact resolved preregistration and per-geometry sufficient statistics,
training curves, every control score, paired intervals, integrity checks, artifact
hashes and a written interpretation. Keep weights, tensor predictions and volumes
outside Git. Report both recipes even if only one qualifies. A failed screen is
a completed experiment, not permission to launch repeated evaluation-guided runs.
Any changed objective/budget/threshold requires a recorded deviation and a fresh
study registration and evaluation identity before further comparisons.

Possible result: `qualifies_local_followup` or `not_qualified` per recipe.
Neither is model-garden certification. Even a passing recipe requires separate
external-domain, larger-radius and seed-replication work; this study does not
choose a large-scale architecture or enable any topology-dependent pilot.

## Completion evidence

The [LG1 assessment and diagram](perception-encoder-local-geometry/lg1-assessment.md)
record the completed run. The frozen protocol remains the original registration
commit; this link and the evidence do not amend its gates or identities.
