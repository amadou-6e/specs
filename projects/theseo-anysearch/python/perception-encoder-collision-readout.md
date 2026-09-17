# Frozen compact collision readout followup

Specs80 / implementation407, user-authorized stack on405/PR406, no merges or
promotion. Predecessor protocol191f883a24b67afe75a5ce9b0783f53351802423; completed
transfer report3c058b813540b08c7eb8f7499a13c2c6b08b44549689a2fc1d9f2a76ec7f8d67
and robustness report6f3036bd4f6a83443324ca44a7ac9c234b82748a31b89c71be4052349de09b7e
motivate this new study. They are not selection data for this experiment.

## Question and fixed boundary

Can a better small-field readout recover collision-relevant information from the
existing normalized729 code, and does explicit uncertain-path calibration expose
or reduce the pooled-threshold failure? Input33, central17, zero-radius discrete
six-connected paths; no field scaling, encoder adaptation, RLlib or global planning.
All three packaged seeds401/402/403, encoder normalization and native geometry
decoder weights stay fixed. Package manifest remains
2ddf188ecedff4699dba434fec05a851c5649119c07dcf30c9d9afd1292d4ed1.

## Fresh data and identities

Program `compact-collision-readout-v1`, run `compact-collision-readout-v1-run1`.
Freeze exact source/spec commits, all tensor/parent/query hashes and both preceding
report hashes before training. Reject parent overlap with all six earlier compact
studies and both405 datasets, and across new splits. No previous test corpus reuse.
Use the unchanged seven generators, central-density quantile mechanism, parent49,
input33/target17,20% independent unknown cells and no visible noise. Train1536,
calibration768, ID test768 use four seen generators; OOD576 uses the three unseen
generators from405. Within each family cycle density.08/.16/.28. This is synthetic
OOD with shared density control, not real-sensor validation.

Each geometry has32 seeded simple six-connected paths, lengths2/3/5/9 equally
represented, visibly known-free start, no subsequent hidden-truth filtering, endpoint
padding to9 nodes with a validity mask. Collision means any true occupied valid node.
Unknown-path/no-visible-hit is the uncertain stratum. Require at least100 uncertain
positives and100 uncertain negatives in calibration; reject inadequate support
rather than replacing the generator or threshold rule. Report all supports.

## Seven fitted controls per seed

All heads share the405 query readout: per-node8 features plus normalized xyz,
Linear11->32/SiLU, masked mean/max pooling, append path length/9, Linear65->32/SiLU,
Linear32->1. No occupancy or unknown query features bypass into compact heads.

| Kind | Spatial processing | Trainable parameters |
| --- | --- | ---: |
| original |405 compact head: Conv1->8->8/GN/SiLU, aligned trilinear9->17 |4521|
| resize_conv | original plus Conv3d8->8,k3,p1/SiLU after interpolation |6257|
| transpose | same compact trunk, ConvTranspose3d8->8,k3,stride2,p1/SiLU replaces interpolation |6257|
| native | frozen package decoder produces occupancy/boundary sigmoid and clamped distance3x17 cubed; Conv3->8->8/GN/SiLU |4953|
| raw | unchanged405 two-channel observed occupancy/unknown33 control |4737|
| spatial | unchanged405 frozen eight-channel backbone33 control |6033|
| null | resize_conv trained on zero normalized code, same initialization |6257|

Resize_conv versus transpose is exactly parameter-count matched. Other controls
are not: report their parameter counts and the additional frozen native-decoder
parameters. Native has geometry-pretraining supervision and a different input
representation; it is a diagnostic for information surviving the code, not a
capacity-matched claim. Its inputs must be generated solely from frozen729 codes.
Frozen native-head predictions use the packaged normalized-code convention,
unchanged sigmoid/clamp and batch8 evaluation path. Hash encoder and native decoder
states before/after extraction and replay; verify shared spatial-cache backbones.

Train all21 heads with the identical405 recipe:4096 updates,32 geometries x4
sampled paths, unweighted BCE, AdamW LR.001/weight decay.01, clip5,64 warmup steps,
cosine to .0001. Initialize seed+10000; sampling seed+40000, shared sequences across
heads within each seed. Checkpoint model/optimizer/RNG every512 updates, no early
stopping or test-driven selection. Float32 deterministic CUDA, TF32/autotuning off,
four CPU threads, cached inputs and one GPU-preloaded training representation.
Profile all readouts before freezing. This is a fixed recipe comparison, not HPO.

## Calibration and held-out evaluation

For each fitted head, lock two thresholds using calibration only: highest inclusive
threshold retaining at least95% empirical collision recall (a) over all calibration
paths and (b) over uncertain calibration paths. Lock all42 thresholds before any
test predictions. Keep pooled operating-point results as the direct405 diagnostic.
At the uncertain threshold, report uncertain-stratum false-safe and false-alarm
rates, AUPRC/AUROC/log loss/Brier and supports. It is not a population95% guarantee.

Also report a clearly named observability-assisted system diagnostic: use the
visible-grid rule on definite paths, and the learned probability/uncertain threshold
only on unresolved paths. This rule requires the raw unknown/observed state; it
is not a pure729-code interface or evidence that the encoder encodes certainty.
Report rule coverage separately, no silent raw-grid bypass into learned-head scores.

Report per family, path length, fully observed, visible-hit, uncertain and hidden-only
collision strata, retaining undefined metrics for empty/one-class support. Evaluate
original/resize_conv/transpose/native with shuffled and zeroed normalized codes,
without refitting/recalibrating. Permutations seed+30000. For native, shuffle codes
before the independent frozen decoder (equivalently shuffle its outputs); decode
zero codes rather than zeroing the three predicted geometry channels.

Primary contrasts: paired per-geometry uncertain-path negative log-loss, averaging
eligible paths within each geometry, then1000 family/density-stratified geometry
bootstrap resamples, seed405. Exclude only geometries with zero eligible paths and
report their count. Compare each new readout to original/raw/spatial/null, separately
for each seed and ID/OOD; use natural log, probability clip1e-6. AUPRC and operating
points are supporting diagnostics; no reselecting a winner from OOD.

A readout is an ID improvement candidate only if all three seeds have a positive
lower95% bound versus original for the primary contrast, uncertain AUPRC gain>=.03,
uncertain missed-collision<=.10 and false-alarm<=.25 at uncertain-calibrated threshold.
Record a separate stronger competitive screen requiring overall and uncertain AUPRC
within.03 of both raw/spatial in every seed. These are frozen engineering margins,
not universal acceptance criteria. Report every candidate and failed condition;
never average failing seeds into a pass, silently relax criteria, or use this screen
to certify deployment. Comparisons form a bounded exploratory study; intervals are
per contrast, not a simultaneous family-wise guarantee. Do not select/test a fourth
recipe after looking at these tests.

## Budget, verification and disposition

Reserve14400s from the existing48 GPU-hour campaign (36.616429h remains before
this study), including timed freeze preparation and1200s validation overhead;
per-fit1800s cumulative cap. One GPU run at a time, no duplicated fits; hash-keyed
resume retains optimizer/RNG and conservatively charges interrupted phases.
Quality failures direct the next recorded comparison, not a protocol stop or a
lowered threshold. A source/identity/mask validity failure excludes affected evidence
and needs an explicit revision before execution resumes.

Replay all artifacts, encoder/native caches, queries/labels,21 final head states,
calibration locks and all calibration/test/perturbed predictions on the original
device. Recompute metrics, bootstrap comparisons and screening decisions. Commit
source, tests, frozen manifest, compact reports and assessment in the issue PRs;
weights, corpora and prediction stores stay runtime-only. No merges or promotion.
Finish by assessing whether readout changes help, whether the code still loses
detail, and whether explicit uncertain calibration trades false alarms for misses.

## Executed evidence

The frozen protocol at `4961f46d4023d9780a9ffd0db18db2bf5e29e09c` was executed
as `compact-collision-readout-v1-run1`, source `958b541`, manifest `84436a7`.
See [the assessment](perception-encoder-collision-readout-assessment.md), including
the pipeline diagram and links to full replayed implementation evidence in PR408.
All three revised heads pass the three-seed ID improvement screen; none passes
the raw/spatial competitiveness screen. Retain, without promotion. This evidence
appendix does not modify the frozen training, calibration or decision rules.
