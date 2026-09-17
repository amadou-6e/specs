# Spatially structured compact-code search

Issues specs#72 / implementation#399. Authorized unmerged successor to #397.
This explicitly extends the compact-code capacity domain, not the field of view:
input33, central17 targets, no RLlib/navigation/topology or promotion claim.
Predecessor report5ca3268a17847dde3bd30e6e019d48994f7140752d113bc1162ffeb594318474
showed a passing spatial reference but no usable compact code. Residual pooled
gains concealed worse thin-sheet IoU; grid128/conv was the actual selected recipe.

## Fresh identities and compute footprint

Study compact-structured-v1; run compact-structured-v1-run1. Freeze full source/spec
SHAs and pretrained seed0 backbone hash. Reuse the central-density-balanced generator,
not any preceding data: train6144, probe1536, selection384, development384 independent
parents. IDs compact-structured-v1-<split>-<index:04d>. Train gets two deterministic
20% masks per parent; probe four; other splits one. Parent49, input33, target17,
fractions.08/.16/.28, four families, truncation8 and all query eligibility unchanged.
Freeze all array hashes/support checks; reject parent reuse against #389/#393/#395/
#397 and across new splits. Development prediction access follows selection lock.

This increases independent training geometries fourfold while retaining12288 training
and6144 probe cache entries. The mask-diversity/data-coverage tradeoff is explicit:
not a pure architecture comparison against the preceding dataset. All current
configurations share this new corpus. Cache frozen8x33-cubed float32 features with
the same hash/key/read-only/memory-map safeguards; approximately22.1GB plus20GiB
disk headroom. No corpus/weights/cache files in Git.

## Twelve configurations

Ten structured candidates: five forms below, each at LR.0003 and.001. Two grid128/
conv controls at the same learning rates reproduce #397's selected architecture
on the new data and budget, not its old weights. Controls remain ranking-eligible.

All structured aggregators use existing preactivation GroupNorm residual blocks:
8->16 stride2, then16->32. The second stride is2 for coarse codes,1 for fine codes.
Coarse output9-cubed is cropped to central5 (indices2:7); fine output17-cubed to
central9 (indices4:13). Kernel3/padding1 downsampling centers correspond to input
coordinates8..24 at spacing4/coarse or2/fine. Apply Conv1x1x1 from32 toC and flatten
channel-major to a single vector. No final MLP, global average or raw-feature bypass.

| Form | Latent side | Channels C | Vector dimension |
| --- | ---: | ---: | ---: |
| Coarse1 | 5 | 1 | 125 |
| Coarse2 | 5 | 2 | 250 |
| Coarse4 | 5 | 4 | 500 |
| Coarse8 | 5 | 8 | 1000 |
| Fine1 | 9 | 1 | 729 |

Structured native decoder: reshape only the vector toC x side cubed, Conv3dC->16
(kernel3,padding1), GroupNorm4, SiLU. For side5 only, ConvTranspose3d16->16
(kernel3,stride2,padding1) to9, GroupNorm4, SiLU. Both forms then ConvTranspose3d
16->8 with the same geometry to17, GroupNorm4, SiLU, Conv3d8->3(kernel3,padding1).
Gather the queried indices. Grid control uses the unchanged grid17->MLP256->128
aggregation and #397 conv decoder. No model accesses truth through a second channel.

Each aggregation/native decoder pair trains8192 updates. Freeze aggregation and
fit a freshly initialized native head8192 updates on probe only; never reuse the
training decoder for ranking. Structured probe normalization is per channel over
probe examples and latent positions, preserving shared spatial scaling; grid uses
per-dimension probe normalization. Float64 population statistics, std floor1e-5,
float32 inputs; persist expanded dimension-wise statistics in artifacts.

This records a methodology deviation from the preceding common-head-only screen:
primary utility is measured with a declared layout-aware independent head. Native
head capacities differ and are not called matched. Report all parameter counts;
do not attribute every improvement to the encoder alone. To diagnose dependence
on the native readout, fit the unchanged common conv head (LinearD->2000 then
5->9->17) for both selected finalists, with the same probe data/budget. These
common-head results cannot change selection and are diagnostics, not a substitute
for later multi-seed/task confirmation. Both head types receive only code and
query indices, never local features or raw input.

## Optimization, controls and selection

Every fit: batch64,256 uniform central17 queries per example,8192 updates, AdamW
weight decay.01, clip5,64-update warmup then cosine to.1*base. Aggregation LR is
the configured.0003/.001; all independent/common/control heads use.001. PyTorch
initialization seed399; CPU sampling generator39900 reset for each fit. Compared
with #397, fourfold total sampled query exposure is a recorded budget change.
Prevalence-weighted occupancy/boundary BCE on hidden queried cells, distance
10*SmoothL1 on queried free cells. Same losses, not model-dependent sampling.
Checkpoint every1024 with optimizer/RNG; evaluate only at8192. No mid-run HPO edits.

Fit the contemporaneous spatial MLP reference from #397 on probe, same budget.
Fit normalized-zero-code native controls for coarse1, fine1 and grid128; these
represent readout families, not exact initialization-matched controls for everyC.
Also evaluate every candidate with zeroed and shuffled selection codes (seed399)
using its fixed head and original thresholds. These ablations do not refit heads.

Primary ranking stays the #393 family-aware rule on independent native-head results:
number of macro targets met (IoU.60/F1.70/errors.10), worst task/family directed
ratio, capped mean macro ratio, fewer aggregation parameters, fewer updates, lowerID.
Pooled scores are diagnostic, never a replacement ranking. Calibrate binary F1
thresholds.01..99 on selection only, lower ties. Lock two finalist IDs before common
head fits and development. Assess both native/common heads and spatial reference
on development; do not reselect. Report variance entropy rank, all family scores,
trained-head scores, ablations, samples, timings and memory. No success claim from
training reconstruction alone or from a passing pooled score with failed families.

## Execution and next decisions

Eight-hour tranche within the already approved48 GPU-hours, no new total budget.
Preparation cap5400s, each fit cap3600s,900s overhead reserve. Cumulative phase
times/resume charges, exclusive ledger lock, deterministic CUDA float32, TF32/
autotuning off, CPU threads4. Charge the uncertain phase cap after interruption;
reuse only verified checkpoints/caches. Profile batch64 CUDA shapes before freeze.

Validate central-latent mapping, flatten/reshape query order, finite gradients,
normalization/no bypass, mask-bank mapping, legacy defaults, schedule, resume and
artifact integrity. Verify original-device cached features and predictions after
completion. Fresh native-head success directs multi-seed confirmation and control
checks before packaging. Native/common disagreement limits readout generality,
not data validity. Failure directs a new bounded information-retention/optimization
study; never lower targets, enlarge the field silently or stop merely at a weak score.

## Executed evidence

The frozen protocol above was executed at spec commit
`02ab2379655e8a76ae4a6a6f3dc4ff483a74145a`, implementation source
`07b24adce7a3faf15ab39bf81cd0a8e77822ed5e`, issue #399 / PR #400.
Report payload `f4c46fe17c0c767e7e43e374ee940f70d83d760f472c18c1fd84a5ee02711b94`:
30 completed fits, 12 configurations, 279 hashed artifacts; 18,684.031 seconds
including the preregistered preparation/overhead accounting (5.190 hours).

Fine729 at LR .0003 is the frozen selection winner (ID8); fine729 at .001 is
runner-up (ID9). Both pass all family point targets on selection. The selected
native head reaches development IoU .75263 / F1 .77775 / errors .04506/.04519,
but thin-sheet IoU .589664 misses .60. The runner-up passes all development
family point targets, but is not substituted using development evidence.
No qualification or promotion. The contemporaneous spatial reference passes
development family targets (pooled IoU .75479 / F1 .79716) despite failing
selection thin-sheet IoU .57844; narrow point margins require replication.

The selected code's common-head development IoU/F1 falls to .56767/.62079.
Thus the supported direction is a layout-aware spatial code with an independent
native head, not a generic interchangeable global embedding. Native readout
capacities, data coverage and cross-study budget differences remain confounds
as declared above. The same-data grid128 controls remain weak (F1 .27424/.27523).

Next evidence-directed action: fresh-data and fresh-seed replication of the
selected recipe, preserving its settings and all thresholds, with spatial/null
controls. Do not retune or reselect on this development set. Repeatable deficits
direct a separate fresh refinement protocol. Implementation assessment and
Mermaid decision diagram: `docs/perception-compact-structured-assessment.md`.
Validation: 514 garden tests; original-CUDA replay verified all 279 artifact hashes,
eight backbone batches, 12 candidates, four controls, two common heads and five
development predictions under unchanged strict tolerances. Specs validator has
zero errors; the unrelated existing large Draw.io warning remains.
