# Compact aggregation reconstruction training

Issues specs#70 / implementation#397. Authorized unmerged successor to #395; no
integration merge or promotion. Input stays33 cubed, target stays central17 cubed.
The preceding frozen-code nonlinear heads were learnable but remained weak. This
study trains the aggregation itself and compares it with an uncompressed reference.

## Frozen protocol

Study compact-reconstruction-v1, run compact-reconstruction-v1-run1. Pin full clean
source/spec commits, the immutable seed0 spatial backbone and preceding report
39503c4fdbb641581a3d1d587827e6fe30e46126dae96e46f9a191d9092fd6e8.
Use fresh train1536/probe768/selection192/development192 parents from the #393
central-density-balanced generator: four families, fractions.08/.16/.28, parent49,
observation33, central17 labels, truncation8. Bank8 deterministic20% masks per
train/probe parent; one mask per other parent. IDs are
compact-reconstruction-v1-<split>-<index:04d>. Preserve box quantile ties. Freeze
array hashes/support checks and reject reuse against #389/#393/#395 and across
new splits. Development labels open only after the selection lock.

Cache the frozen backbone's full8x33x33x33 features as float32 memory-mapped files,
one split per file, bounded extraction batches16. Key by data identity and backbone
state hash; hash completed files before fitting. Read-only mappings, copied CPU
minibatches to CUDA; never load the whole cache onto GPU. Approximately21.4GB
feature storage plus20GiB free-disk headroom required. Partial unverified caches
are not silently reused. Model weights/caches/corpora stay outside Git.

## Factorial and controls

Eight candidates: aggregation grid/residual x dimension64/128 x training decoder
linear/conv. Grid: ordered adaptive-average bins to17 cubed, flatten, Linear39304
to256, SiLU, Linear256 toD. Residual: existing GroupNorm preactivation blocks
8->16->32->64, each kernel3/stride2, producing5 cubed; flatten8000, Linear8000
to256, SiLU, Linear256 toD. No global average bottleneck, variance penalty or
backbone update. Capacity is reported, not claimed matched. D128 has hidden256,
not a hidden layer smaller than its output dimension.

Linear training decoder: LinearD to3*4913 and gather queries. Conv decoder is
the #395 convolutional readout, with its initial Linear changed toD->2000 only.
Each candidate trains aggregation plus decoder for4096 updates. Then freeze and
hash aggregation, discard the training decoder for ranking, extract its probe/
selection vectors and fit a freshly initialized conv head for4096 updates on
probe only. Probe population mean/std floor1e-5 normalize vectors (float64
statistics, float32 model inputs). Never backpropagate independent-head loss
into aggregation. Fit a same-budget normalized-zero-code conv control atD64.

Contemporaneous spatial reference: each queried central17 coordinate receives its
frozen local8-vector from the corresponding33-cubed feature volume plus xyz in
[-1,1]. MLP11->64, SiLU, Linear64->3; no compact code. Train on probe bank with
the same updates/query exposure. No extra spatial-feature normalization. This is
an uncompressed reference, not a capacity-matched control or compact candidate.
Fit it first; its failure is evidence to investigate backbone/task adequacy, not
a reason to suppress the factorial. Report selection and locked development.

All fits: AdamW LR.001, weight decay.01, clip5;64-update warmup then cosine to
.1*base at4096. Batch32,256 uniformly sampled central17 coordinates each. Identical
sampling CPU generator39700 and initialization seed397 for every fit; query labels
and mask-bank mapping tested. Occupancy/boundary hidden-cell BCE with fit-split
positive-class prevalence weights; distance10*SmoothL1 on sampled free cells.
No model-dependent resampling. Save every1024 updates with optimizer/RNG; selection
only at4096. Log minibatch curves without calling them held-out learning curves.

## Selection and interpretation

Sigmoid binary predictions, distance clamped[0,1], all eligible central17 cells.
Choose pooled F1 thresholds.01..99 on selection only, lower ties. Rank eight
independent-head candidate results by #393 family-macro rule: targets met
(IoU.60/F1.70/errors.10), worst task/family directed ratio, capped mean macro
ratio, fewer aggregation parameters, fewer updates, lower ID. Select top two,
write immutable selection lock before development. Report per-family results,
trained-decoder metrics, independent-head metrics, fixed selection-scene shuffled
codes (seed397, same thresholds), covariance entropy rank, parameter counts,
exposure, times and memory. Null/spatial controls never enter candidate ranking.
Assess the two finalists and spatial reference on development, not every candidate.

If spatial succeeds and compact fails, next change is information retention or
explicitly preregistered larger code capacity, not more head-only search. If both
fail, investigate/adapt backbone and task before blaming compression. If compact
meets targets, proceed to fresh-seed independent confirmation and utility controls,
not immediate packaging. Single-seed directional evidence; no qualification claim.

## Budget and validity

Four-hour tranche inside authorized48 GPU-hours, including preparation and300s
overhead reserve. Per-fit cap1800s; cache preparation cap3600s. Save cumulative
fit time and charge the full uncertain phase cap on interruption before resuming
verified checkpoints. Exclusive campaign ledger lock and durable progress file.
Deterministic CUDA float32, TF32/autotuning off, CPU threads4. Do not mutate frozen
source/protocol in place. Validate shape/gradient/coordinate mapping, frozen state,
cache identity/hash/size, independent normalization, schedule, ranking and resume.
Replay artifact hashes and original-device predictions/metrics after completion.
Quality failures direct a bounded fresh follow-up; validity failures exclude the
affected evidence and require a recorded repair, never lower the acceptance bars.

## Completed evidence

Implementation#397 / PR398; source4723679, manifest24902ee, verifier531c5a8.
All18 fits completed. Report payload SHA256:
5ca3268a17847dde3bd30e6e019d48994f7140752d113bc1162ffeb594318474.
498 garden tests passed; all97 artifact hashes, eight backbone-batch replays,
eight candidates including vectors/heads/shuffles, two controls and three
development predictions verified on original CUDA.

The frozen ranking selected grid128/conv, not the best pooled-score residual model:
residual/conv improved pooled F1 to.404 but thin-sheet IoU remained.179/.167,
below grid/conv.205/.209. Selected grid128 development IoU.27136, F1.35488,
clearance.08829, recovery.08851; sphere/box distance errors still exceed.10.
The spatial reference achieved.75816/.79214/.04754/.04832 and passes every
development family. No compact candidate is usable or promotion-eligible.

Nonlinear reconstruction helps; neither code-size doubling nor variance-rank
improvement rescues the weak families. Next is a fresh spatial-layout/capacity
and learning-rate study, preserving local ordering inside a flattened vector,
with the actual selected grid/conv recipe retained as a control. Larger code sizes
require an explicit successor protocol; the field remains33 with central17 targets.
Increase independent geometry coverage within a bounded cache footprint; preserve
independent heads, family-aware ranking and unchanged quality targets.

Run3136.516s plus final settlement and an additional300s validation reserve in the
ledger; no change to the immutable report. All source/spec PRs remain unmerged.
