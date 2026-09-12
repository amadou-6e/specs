# Nonlinear independent compact readouts

Issues specs#68 / implementation#395. Authorized unmerged stack on #393. No encoder
training, field enlargement, integration merge or promotion. This fresh study asks
whether nonlinear heads can recover geometry from immutable64-number vectors.
Motivation: #393 increased variance entropy rank without fixing linear-head quality.

## Frozen sources and data

Pin full source/spec SHAs and report02701cbde1957a598460a86b0a4321f3ff39344a3a468c0f54dd3b943787fbe0.
Use exactly recipe-0-step-512.pt (task-selected source) and recipe-5-step-1024.pt
(high-diversity contrast, not relabeled as the prior winner). Verify both artifact
and aggregation-state hashes plus the shared pretrained spatial backbone hash.
No trainable head receives raw voxels or local features.

Study compact-readout-v1; run compact-readout-v1-run1. Fresh probe1536, selection192,
development192 and calibration12 geometry IDs: compact-readout-v1-<split>-<index:04d>.
Use #393's central17-quantile four-family generator, fractions.08/.16/.28 and same
parent49/observation33/target17 conventions. Reject duplicates across new splits
and against all registered parents in #389 and #393. Hash all arrays before fitting.
Probe gets eight20% masks per geometry; other splits one. Mask seeds are SHA ID
plus -mask-<bank-index>. Probe labels are the only labels for fitting ordinary heads.
Calibration is used exclusively for the learnability controls. Development opens
only after candidate head selection is locked. Family label/free support checked.

Cache immutable vectors for exact input/mask/source identities, not local-feature
inputs to the heads. Both sources share frozen backbone extraction, batches16.
Probe-only mean/std (population std floor1e-5, float64 statistics) normalize inputs;
neural heads receive float32 normalized vectors. Preserve normalization in artifacts.
Verify aggregation/backbone states before and after extraction. Cache hash before
fitting; no weights or corpora in Git.

## Heads and labels

Two head architectures, fixed64 input and three outputs per target coordinate:

- Conv: Linear(64,16*5^3), SiLU, reshape; ConvTranspose3d16->16 (kernel3,stride2,
  padding1) to9^3, GroupNorm4, SiLU; ConvTranspose3d16->8 with the same kernel/
  stride/padding to17^3, GroupNorm4, SiLU; Conv3d8->3 (kernel3,padding1).
- FiLM: query xyz in[-1,1], concatenated with sin/cos(pi*xyz*f), f=1,2,4,8
  (27 inputs); Linear27->128 and SiLU. Three residual blocks: Linear128->128 on
  SiLU(h), modulated by (1+gamma(z))*value+beta(z), SiLU and Linear128->128,
  then add to h. Each gamma/beta comes from Linear64->256. Final SiLU and
  Linear128->3. Use PyTorch default layer initialization, no special zero init.

[FiLM](https://arxiv.org/abs/1709.07871) motivates feature-wise affine conditioning;
[Occupancy Networks](https://arxiv.org/abs/1812.03828) motivates geometry queried
through a learned continuous function. These heads are local experimental designs,
not replications or evidence that either paper guarantees this voxel performance.

For each source/head, compare learning rates.0003/.001/.003:12 candidates. Train
4096 updates, evaluate/save1024/4096. AdamW weight decay.01, clip global gradient
norm5;64-update linear warmup then cosine to.1*base at4096. Batch32 bank entries,
256 uniform target indices each. Fixed head initialization seed395 and sample
CUDA generator39500 for every fit. Same sampled label exposure across neural heads;
conv computes dense outputs but gathers exactly the same supervised query indices.
Occupancy/boundary BCE uses probe-prevalence positive weights on hidden selected
cells; distance10*SmoothL1 uses selected free cells. No model-dependent resampling.
Record head parameters, runtime, memory, updates and query exposure.

Predict sigmoid for binary logits and clamp distance[0,1]. Evaluation uses all
eligible central17 cells, in batches8 for bounded memory. Select pooled F1
thresholds.01..99 (lower ties) on selection, never development.

## Controls and selection

Fit two ridge controls (one per source), alpha1, unpenalized bias, same probe bank.
Identical per-geometry labels may be summed in the normal-equation sufficient
statistics instead of materializing eight copies; test algebraic equivalence.
These closed-form controls see all targets, unlike the finite sampled neural fits;
report that exposure difference rather than imply an identical optimization budget.

Fit one no-input head per architecture at LR.001 with normalized zero vectors,
same4096 updates/labels. These are controls, excluded from candidate ranking.
Also evaluate each trained candidate after fixed-seed selection-scene permutation,
keeping its thresholds. The no-input fit and fixed-head shuffle answer different
questions; neither is a substitute for future matched raw/spatial controls.

Learnability controls: four calibration scenes at indices1/4/7/10, corresponding
to four families at density.16. Input64 code has a one-hot scene identity in its
first four coordinates; no real-encoder claim. For each head and three LRs, train
2048 updates with batch32 and256 uniform queries, all queried cells eligible for
binary loss, free cells for distance. Same optimizer, warmup64/cosine horizon2048.
Score all same-scene cells with F1-calibrated thresholds: IoU.95 and boundary F1.97
are overfit targets, not generalization. Record free-cell NMAE. An underfit control
limits negative readout conclusions; it does not invalidate the real fits or imply
an encoder impossibility theorem. Retain both successes and failures.

Rank only the12 real candidate fits/checkpoints by the #393 family-macro rule:
number of task-macro targets met (IoU.60/F1.70/errors.10), worst directed ratio
over all task/family cells, capped mean macro ratio, fewer head parameters, fewer
updates, lower configuration ID. Select the top two distinct candidate fits, with
each fit's best checkpoint fixed from selection. Lock before development; do not
reselect from development. Report all families, controls and learnability limits.
Single-seed directional evidence only; no automatic utility/certification claim.

## Budget and execution

Cap4h within the existing approved48 GPU-hours, including preparation and300s
overhead reserve. Each fit cap900s; track cumulative saved-fit time across resumes.
Exclusive ledger lock, deterministic float32/float64 as specified, CPU threads4,
TF32/cuDNN autotuning off. Save optimizer/RNG/checkpoints and compact reports with
artifact hashes; cached vectors remain outside Git. On interruption charge900s
for the uncertain fit/preparation phase before resuming a verified checkpoint.
Completed phases are not repeated silently; preserve all accounting and failures.

Before fitting: head shape/gradient/query-order tests; input-only conditioning;
immutable encoder/cache checks; old-data default identity preserved; grouped ridge
equivalence; learning-rate schedule, mask/label selection, ranking and resume tests.
Verify report hashes and original-device prediction replay after completion.
If nonlinear heads help, confirm the promising head/encoder before packaging; if
not, test encoder training with a nonlinear decoder and stronger spatial detail
under fresh identities. Continue within scope/budget, not another routine pause.

## Completed evidence

Implementation#395 / PR396, sourced02d086, manifest11811c9. All20 fits and34
checkpoint evaluations completed. Report payload
39503c4fdbb641581a3d1d587827e6fe30e46126dae96e46f9a191d9092fd6e8.
484 garden tests passed. All39 artifact hashes,34 original-CUDA head replays,
24 shuffle replays, two ridge controls and both development assessments verified.

Conv passed all three learnability controls (IoU1.0, boundary F1.989/1.0/1.0).
FiLM passed at LR.003 (both1.0), underfit at lower rates. Real frozen-code heads
remained around.34-.35 boundary F1, above null~.259 but far below target. Selected
source0/conv/LR.001/4096 development: IoU.25684, boundary F1.33722,
clearance.09771, recovery.09790. Neither finalist is usable or promotion-eligible.

Charge1180.906s plus final report-write settlement, including preparation and300s
overhead reserve. Next: train the encoder aggregation with nonlinear reconstruction
and stronger spatial-detail preservation, with a contemporaneous spatial reference.
Keep the field fixed, preserve failed results and freeze fresh identities before
training. No additional head search on these immutable codes is justified now.
