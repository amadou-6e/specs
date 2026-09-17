# Frozen compact-code robustness and collision transfer

Specs #78 / implementation #405. User-authorized unmerged successor to package
#403/PR404; no merges or promotion. Package spec
1eedc6ca419b4f62f9bb320d1e983d65cb8999ca and manifest
2ddf188ecedff4699dba434fec05a851c5649119c07dcf30c9d9afd1292d4ed1.
Freeze both protocols below, exact source/spec commits and fresh array identities
before either study executes. No design changes driven by the robustness results
are silently introduced into transfer. Fixed input33/central17; no RLlib/planner.

## Shared generation and validity

Retain the four original continuous-field generators and add three unseen ones:
unions of solid ellipsoids, a forest of finite solid capsules, and gyroid walls.
Generate fields on parent49, threshold at a declared central17 occupancy quantile,
then crop input33. Unseen means these three algorithms were absent from encoder
training; shared quantile density control is not a wholly unrelated data domain.
Use SHA-derived per-geometry seeds and record actual density. Compute geometry
targets on the full parent with the unchanged truncation8 and boundary definition.
Record parent, input, mask, target and query hashes. Reject parent overlap with
all previous compact studies and across transfer splits. Robustness deliberately
pairs the same scene field across conditions; those repeated parents are declared
paired observations, not independent geometries.

All three exported encoders remain frozen, including normalization. Check their
state hashes before and after each study. Weights, corpora, caches and prediction
tensors stay runtime-only; source, tests, resolved manifests and compact reports
are committed. Use deterministic float32 CUDA, TF32/autotuning off, four CPU
threads, existing campaign budget ledger and no concurrent GPU trials.

## R: robustness without retraining

Identity `compact-robustness-v1`, run `compact-robustness-v1-run1`.
Seven generators,24 paired geometry IDs per generator,12 conditions:

- Baseline: central density .16, independent unknown probability .20, no noise.
- Density .03/.08/.28/.45, otherwise baseline.
- Unknown probability0/.10/.40/.60, otherwise baseline.
- Independent visible occupancy bit flips .01/.05, otherwise baseline.
- Contiguous axis-aligned unknown slab of7/33 input slices, otherwise baseline.

Same latent field/geometry ID across all conditions; same uniform random arrays
for nested missing rates/noise levels. Slab axis/location are seeded by geometry.
Only visible occupancy is corrupted; truth and unknown-channel semantics are not.
Density conditions necessarily change the thresholded parent, while noise/mask
conditions share the same parent. All seed401/402/403 package geometry heads and
thresholds remain fixed. No recalibration, head fitting or normalization updates.

Report per seed/generator/condition occupied IoU, boundary F1, and normalized
distance error on all central cells/free cells, plus original hidden-cell binary,
visible-free clearance and hidden-free recovery metrics. Record supports; empty
subsets (especially zero missing rate) are explicitly unavailable, never zeros or
silently dropped from an aggregate. Original hidden-task targets remain .60/.70/
.10/.10, reported as a stress-test outcome, not grounds to alter acceptance bars.
All-cell scores are separate diagnostics, not substituted into original gates.

For mask/noise shifts report paired changes from baseline; for density shifts
call them paired-field comparisons because truth also changes. Include per-geometry
scores and paired mean distance-error differences with1000 geometry-cluster bootstrap
resamples, seed405. Report worst conditions and unsupported regimes, never only
the best subset. This bounded screen has24 scenes per cell and only synthetic
generators; confidence intervals do not establish broad deployment robustness.

Reserve7200s within the existing48 GPU-hours, including timed freeze preparation
and600s validation overhead. No partial failure converted into a pass.

## T: new short-path collision head

Identity `compact-collision-transfer-v1`, run `compact-collision-transfer-v1-run1`.
Fresh shared geometry splits: train1536, calibration384, ID test384 (four original
families equally represented), OOD test288 (three unseen families equally).
Within each family cycle densities .08/.16/.28. Independent20% unknown masks,
no occupancy noise. These data are disjoint from robustness and prior studies.

For every geometry sample32 paths, cycling lengths2/3/5/9. Paths are simple
six-connected random walks inside central17, no repeated nodes, seeded by ID.
Starts must be visibly known free, using only observed input; subsequent steps
are not filtered by hidden truth or occupancy. Deterministic bounded rejection
raises on insufficient paths, never switches label semantics. Pad to9 nodes with
the final node and supply a valid-node mask. Target collision is any true occupied
path voxel. Agent radius is zero; this is discrete path occupancy, not dynamics,
continuous swept-volume collision, global reachability or navigation success.

Compare four fitted heads for each seed401/402/403:

1. Compact: normalized frozen729 code reshaped to1x9x9x9.
2. Raw grid: observed occupied and unknown channels over input33.
3. Spatial: frozen backbone8-channel full input33 feature volume.
4. Null compact: zero normalized code, with the same head initialization/budget.

Common head family: two Conv3d layers to8 channels, kernel3/padding1, each with
GroupNorm2 and SiLU. Compact maps are trilinearly expanded to17 with aligned
corners; raw/spatial maps are cropped to central17 after convolution. Gather at
path nodes, concatenate normalized node coordinates, apply shared Linear11->32
and SiLU; masked mean/max pool over valid nodes, append normalized path length,
then Linear65->32,SiLU,Linear32->1 collision logit. Same widths and training
budget; first-layer parameter counts differ and must be reported, not called
exactly capacity-matched. Raw and spatial controls see the full33 input before
cropping; learned receptive-field differences remain an architectural limitation.

All encoder parameters and statistics stay fixed. Heads initialize with seed+10000,
sampling generator seed+40000. Fit4096 updates,32 geometries and4 sampled paths
per geometry per update, unweighted BCEWithLogits, AdamW LR.001, weight decay.01,
clip5,64-step warmup/cosine to .0001. One frozen recipe, no HPO in this comparison.
Checkpoint model/optimizer/RNG every512 updates. Cache inputs/features and preload
one training representation on CUDA when memory permits. Profile before freezing.

Calibrate one decision threshold per fitted head on calibration only: highest
threshold retaining at least95% empirical collision recall (inclusive >=).
Lock all twelve thresholds before ID/OOD prediction access. No seed/repr selection
on either test split. Also evaluate each compact head with shuffled geometry codes
(permutation seed+30000) and zeroed codes, without refitting or changing thresholds.

Report collision-positive AUPRC, AUROC, log loss (probability clip1e-6), Brier,
false-safe rate FN/positive, false-alarm FP/negative, and predicted-safe fraction;
record class supports and mark rank metrics unavailable for one-class strata.
Disaggregate by generator, path length, fully observed paths, and uncertain paths
with at least one unknown node but no visible occupied node. Report visible-hit
and hidden-only-collision supports/false-safe rates separately. A visible-grid
rule declares collision on a visible occupied node, free only if every node is
known free, otherwise abstains; report coverage and error on its definite subset.
Do not use hidden truth as an input or imply all hidden completions are identifiable.

Primary comparisons are paired per-geometry negative log-loss differences with
1000 family/density-stratified geometry bootstrap resamples, seed405, separately
for each training seed and test split. No pooling paths as independent samples.
Per-seed differences from raw/spatial/null and fixed-head shuffled code are reported.

An engineering screen may label the ID result competitive only if every seed has
compact AUPRC within .03 of both raw/spatial heads, at least .10 above fitted null,
false-safe <= .10 and false-alarm <= .25. These are preregistered practical margins,
not literature-derived universal guarantees. Otherwise report limited/no transfer
with the actual failed comparisons. OOD results are independently reported, never
used to reselect. Failed quality directs a separately frozen followup, not blocking
the remainder of this valid comparison or relaxing criteria.

Reserve14400s within existing authorization, timed freeze preparation plus900s
validation overhead, per-fit1800s. Hash-keyed resume and cumulative charges; no
duplicated fits. After completion verify artifacts and original-device head
predictions, calibration lock, sampled-query exposure, and encoder-state invariance.
Keep confidence/partial-observation/control-capacity limits in the assessment.

## Executed evidence

Both studies completed and passed original-device replay under frozen protocol
191f883a24b67afe75a5ce9b0783f53351802423 and implementatione16fbc6 (issue405/PR406).
See the [full assessment](perception-encoder-compact-validation-assessment.md).
Robustness report6f3036bd4f6a83443324ca44a7ac9c234b82748a31b89c71be4052349de09b7e;
transfer report3c058b813540b08c7eb8f7499a13c2c6b08b44549689a2fc1d9f2a76ec7f8d67.
All416 artifacts verified, all12 collision heads and82944 queries replayed;
encoder states unchanged. 559 garden tests pass. The compact code transfers useful
signal but misses the declared raw/spatial competitiveness margins in every seed.
Noise, sparse density and contiguous occlusion expose robustness limits. The
uncertain-path diagnostics also expose limits of pooled-recall threshold calibration.
No thresholds, heads or criteria were changed after test access. Total accounted
3706.844s for these two studies within the existing48-hour authorization; no merge
or promotion. Subsequent directions require fresh protocols/data, not test-set tuning.
