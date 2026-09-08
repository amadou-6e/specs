# LG2: joint occupancy and distance pretraining

Status: prospective engineering screen, not model certification.
Implementation issue: `amadou-6e/theseo-anysearch#354`; spec issue: `amadou-6e/specs#31`.

## Authority and historical boundary

The user explicitly authorized stacking LG2 on unmerged LG1 implementation PR #353
and specs PR #30, and executing before review. No PR merge is authorized. The
implementation base is `6af6b86e665b90f6fc8a05b34a185395a541efbf`; the specification
base is `146faf7` on `docs/29`. This exception is specific to LG2 execution.

LG1's [frozen protocol](https://github.com/amadou-6e/specs/blob/062acdd3964c50c9d9c588734073d340a21ccf2e/projects/theseo-anysearch/python/perception-encoder-local-geometry.md)
and `not_qualified` verdicts remain unchanged. LG2 is a new study in the separate
local-geometry program. No topology, connectivity, planning, global-embedding,
wide-context or P1-P8 claim is authorized. Topology remains stopped.

## Hypothesis and arms

Joint pretraining may preserve occupancy/boundary information while learning
distance accuracy comparable to ESDF-only pretraining. Compare **occupancy, ESDF,
and joint**, initialization seeds **0, 1, 2** each, on one unchanged small partial-
convolution residual encoder: widths 8/16/32/64, eight local output channels,
existing lateral decoder, radius eight (17 cubed voxels). Do not train or qualify
the global projection. This is not an architecture comparison.

Every arm instantiates the same disposable Conv3d(8,2,1) head so initialization is
paired. Occupancy supervises output zero using unweighted BCE-with-logits; ESDF
supervises output one using Smooth L1 on signed distance clipped to +/-8 and divided
by eight. Joint loss is **BCE + 10 * Smooth L1**. Both targets use the same hidden
cells. The factor ten is a fixed engineering heuristic informed by the order of
magnitude of LG1 training losses, not a tuned or validated optimum. Log both loss
components; inactive-arm outputs are not evidence of prediction quality.

Each arm receives 1,024 updates, batch eight, AdamW lr 0.001, weight decay 0.01.
No scheduler, early stopping, AMP, compilation, weighting search or gradient
balancing. Same seed-specific sample/mask stream (35400 + seed) across all arms.
This matches updates, samples and architecture, not exact FLOPs or wall time:
joint supervises two head outputs. Report actual runtime. All nine encoders finish
before the evaluation corpus is opened. Four-hour total cap; no incomplete run
can qualify. CUDA FP32, deterministic algorithms, TF32 disabled, four CPU threads.

## Fresh data and probes

- Study: `voxel-encoder-local-geometry-v1-lg2`.
- Dataset: `voxel-encoder-local-geometry-v1-dataset-2`.
- Queries: `voxel-encoder-local-geometry-v1-queries-2`.
- Run ID: study plus objective and `seed-0`, `seed-1` or `seed-2`.
- New write-once preregistration pins this exact spec commit, executable commit,
  resolved settings, all geometry IDs, and the development rank-fixture report.
- Report uses a new canonical payload identity and artifact hashes.

Use 96 pretraining, 48 probe-fitting, 48 evaluation geometries, disjoint by identity
and from LG1, balanced over the same 12 procedural family/density strata. Existing
`imported` means synthetic ellipsoids, not external real data; `topology` is a wall
generator name, not a topology target. Generate observation index one, radius eight,
in the local program with fresh LG2 geometry IDs. The existing occupancy-aware crop
selection is retained; do not claim unbiased natural-world sampling.

Independent Bernoulli(0.20) missingness, independent of truth, masks all hidden
input-channel values via the support path. Train masks resample each update.
Probe/evaluation banks are fixed, seeds 35401/35402. Occupancy and exact boundary
queries sample hidden cells; clearance samples observed-free cells; recovery
samples hidden ground-truth-free cells. Each task draws 256 uniform eligible
queries per geometry, without replacement unless fewer cells are eligible.
Fail invalid without redrawing if any eligible pool is empty, or either binary
task has fewer than 100 positive or negative query rows on either reporting split.

Discard pretraining heads. Freeze and hash encoders; fit fresh Linear(8,32)-SiLU-
Linear(32,1) probes, with train-only feature mean/std (std floor 1e-5). Probe fitting
uses only its own geometry pool. Use 512 updates, batch 1,024, AdamW lr 0.001,
weight decay 0.01, initialization seed 41000 + seed, sampling seed 42000 + seed.
Final checkpoint only; threshold 0.5; no selection on evaluation. Binary loss is
BCE; regression loss is Smooth L1 with outputs clipped to [0,1] for evaluation.

Targets and normalization are unchanged: occupied six-neighbor boundary, exact
queried-row F1 with zero spatial tolerance, and crop-local positive signed distance
clipped at eight voxels/divided by eight. Free-only regression is conditional on
ground-truth free queries, not a free-space classification claim. Missingness is
not physical line-of-sight occlusion.

## Rank-methodology deviation

This change is declared **before LG2 data**, not applied retrospectively to LG1.
Development-only synthetic fixtures (`lg2-rank-fixtures-1`, seed 354) contain 2,048
eight-dimensional Gaussian rows, half for linear fitting and half for testing.
The label is the row sum. Tests include independent features, invertible scaling
of seven channels by 0.01, eight copies of the label, and constant features.

The invertible transform drops covariance entropy rank fraction from 0.9983 to
0.1259 while held-out linear MSE stays below 1e-12. Correlation rank remains 0.9986.
The useful rank-one representation also predicts exactly, whereas the constant
representation has rank zero, all channels dead and MSE about 7.37. These fixtures
demonstrate that a covariance-rank floor alone does not establish information loss
or usefulness. They are not evidence that LG1's features are optimal.

For LG2, covariance rank and correlation rank are **diagnostics only**. Report
whether each run would satisfy LG1's 0.25 floor; do not whiten study features to
force a pass. Keep the <=5% near-dead-channel guard (std <1e-5), finite values,
unchanged encoder hashes and exactly zero mask-isolation difference as hard gates.
Actual task quality plus zero/shuffle and shuffled-label controls remain mandatory
tests of useful information. This does not prove broad representational diversity.

## Frozen decisions

All three seeds must independently satisfy all four absolute bars: occupied IoU
>=0.60, exact boundary F1 >=0.70, clearance NMAE <=0.15 and recovery NMAE <=0.20.
Each must improve over every paired random-encoder, zeroed-feature, shuffled-feature
and shuffled-label control by >=0.05 for classification or >=10% relative error
reduction and strictly positive gain for regression. Random encoders match initial
states; all fitting controls use the same probe budget. Shuffle evaluation rows
before normalization with seed 35430 + seed. Label shuffling is on fitting labels
only; evaluate against true held-out labels. No headroom normalization.

Each three-seed mean paired improvement must also have positive lower 95%
percentile bound from 2,000 stratified geometry-bootstrap draws, seed 354. Resample
four geometries with replacement within each of 12 strata, sharing draws across
arms, controls and seeds. Recompute pooled IoU/F1 from confusion counts, and NMAE
from error sums/counts; average scores across seeds. Intervals are conditional on
these seeds, not population seed uncertainty. All metrics are conjunctive; no
max-over-strata, best-seed selection, multiplicity-driven winner selection or
post-hoc gate change is permitted.

The primary **joint-preservation** hypothesis additionally requires joint to be
noninferior to occupancy-only on IoU and boundary F1 (margin 0.03 absolute), and
to ESDF-only on clearance/recovery (margin 0.02 NMAE). Every paired seed difference
and the lower paired 95% improvement bound must be >= negative margin. These are
engineering tolerances, not established deployment thresholds. Joint must also
pass all absolute, control and integrity gates. This tests preservation, not
superiority; passing neither certifies an encoder nor selects a large architecture.

Report per-recipe `qualifies_local_followup`/`not_qualified`; primary outcome is
`joint_preserves_specialists` or `joint_hypothesis_not_validated`.

Diagnostic only: visible 3x3x3 occupied/free/unknown neighborhood MLP (81 inputs,
32 hidden, same fitting budget), and exact full-information target oracle. The raw
probe has different capacity and receptive field; no capacity-matched superiority
claim follows. Report every arm regardless of outcome. Preserve all failures.

## Publication

Publish frozen registration, development fixture evidence, training curves,
per-geometry sufficient statistics, control and joint-preservation intervals,
integrity/rank diagnostics, artifact hashes, written assessment and state diagram.
Keep weights, generated volumes and tensor predictions outside Git. Specifications
and evidence must also be committed/pushed in the specs repository. PRs remain
unmerged for user review. No evaluation-guided retry, larger-radius run or changed
joint weighting is authorized under this frozen study identity.
