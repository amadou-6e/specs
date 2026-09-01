# Experiment Plan: Standalone Voxel Encoder Pretraining

Status: discovery
Owner: amadou-6e
Last reviewed: 2026-09-01
Tracking issue: [specs#7](https://github.com/amadou-6e/specs/issues/7)
Related research: [Scalable 3D Voxel Perception Encoders](perception-encoders.md)
Governing specification: [Model Garden](model-garden.md)

## Decision boundary

This plan answers one question: is a pretrained voxel encoder good enough to publish
in the model garden before it is connected to a policy, RLlib, a reward function, or
an end-to-end path-finding model?

No policy or navigation result is part of this certification. A disposable decoder or
probe may read a frozen encoder because an encoder has no observable correctness by
itself. The probe must be capacity-limited, trained with a fixed protocol, and unable
to update the encoder. This separates information present in the representation from
information learned by a later model.

Pretraining loss alone is not a certification metric. Different objectives have
different loss scales, and low reconstruction loss can be obtained by predicting the
dominant empty class. Every checkpoint must pass objective-independent frozen probes.

## Literature findings

### How pretrained representations are evaluated

- [SimCLR](https://arxiv.org/abs/2002.05709) established frozen linear evaluation and
  limited-label evaluation as practical tests of whether information is accessible in
  a representation. It also showed that augmentation composition, a projection head,
  batch size, and training duration materially affect contrastive learning.
- [Masked Autoencoders](https://arxiv.org/abs/2111.06377) use an asymmetric design in
  which the encoder processes visible tokens and a lightweight decoder reconstructs
  masked content. The decoder is discarded after pretraining. Compute savings from
  visible-token encoding do not automatically apply to a dense CNN that still
  processes every masked voxel.
- [VICReg](https://arxiv.org/abs/2105.04906) explicitly controls invariance, per-feature
  variance, and covariance to avoid collapsed or redundant embeddings without
  requiring negative pairs.
- [Alignment and uniformity](https://arxiv.org/abs/2005.10242) provide intrinsic
  diagnostics for contrastive representations, but they are not substitutes for
  task-relevant probes.
- [RankMe](https://proceedings.mlr.press/v202/garrido23a.html) proposes effective rank
  as a label-free signal for selecting self-supervised representations. It is useful
  for rejecting collapse and screening checkpoints, not as the sole acceptance gate.

### What 3D masked pretraining suggests

- [PointContrast](https://arxiv.org/abs/2007.10985) and
  [DepthContrast](https://arxiv.org/abs/2101.02691) show that contrastive 3D
  representations can transfer across datasets and tasks, but view construction is a
  major part of the method.
- [Point-MAE](https://arxiv.org/abs/2203.06604) and
  [MaskPoint](https://arxiv.org/abs/2203.11183) apply masked modeling to point clouds
  with coordinate reconstruction or masked point discrimination. Their point-patch
  assumptions are not identical to known-free voxel occupancy.
- [Occupancy-MAE](https://arxiv.org/abs/2206.09900) and
  [Voxel-MAE](https://openaccess.thecvf.com/content/WACV2023W/Pretrain/html/Hess_Masked_Autoencoder_for_Self-Supervised_Pre-Training_on_Lidar_Point_Clouds_WACVW_2023_paper.html)
  provide direct evidence for masked occupancy or voxel reconstruction followed by
  transfer of the encoder.
- [GeoMAE](https://openaccess.thecvf.com/content/CVPR2023/html/Tian_GeoMAE_Masked_Geometric_Target_Prediction_for_Self-Supervised_Point_Cloud_Pre-Training_CVPR_2023_paper.html)
  reports benefits from geometry-specific targets such as centroids, normals, and
  curvature rather than raw coordinate or occupancy reconstruction alone.
- [MM-3DScene](https://arxiv.org/abs/2212.09948) combines informative masking,
  progressive reconstruction, and self-distilled consistency for large 3D scenes.
- [NOMAE](https://arxiv.org/abs/2502.20316) reconstructs occupancy in neighborhoods of
  visible voxels and uses hierarchical multi-scale masking. This directly supports
  testing neighborhood and multi-scale objectives for the proposed voxel pyramid.
- [clDice](https://openaccess.thecvf.com/content/CVPR2021/html/Shit_clDice_-_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_CVPR_2021_paper.html)
  demonstrates that volumetric overlap can hide connectivity errors and provides a
  topology-aware 2D/3D measure. Theseo should likewise measure connectivity rather
  than accepting voxel IoU alone.

### Synthesis

The most defensible initial recipe is a multi-scale masked voxel encoder with a small
decoder, geometry-aware auxiliary targets, and an explicit representation-consistency
term. Contrastive learning and self-distillation are valuable comparisons, not
assumed defaults. Exact geometry can generate clearance, connectivity, and geodesic
targets automatically, so standalone certification can test path-relevant spatial
information without involving a policy or RL system.

## What counts as independent encoder validation

The encoder is loaded from its checkpoint, put in evaluation mode, and frozen. Every
parameter must have `requires_grad = false`, and encoder inference must run under
`no_grad`. Probe training must verify before and after SHA-256 hashes over sorted
tensor names, dtypes, shapes, and raw tensor bytes are identical.

Three readout classes are allowed:

1. **Linear probe**: one affine map from the global embedding.
2. **Coordinate probe**: an MLP with at most two hidden layers of width 128 reading
   `[embedding, query_coordinates, stride_metadata]`.
3. **Probe decoder**: a decoder no larger than 25% of encoder parameter count or one
   million parameters, whichever is smaller, used only for masked occupancy and
   topology reconstruction.

The same probe architecture, optimizer search space, update budget, and labeled
sample count must be used for every encoder in a comparison. A result from a larger
or separately tuned probe is invalid.

### Probe training protocol

Materialize immutable query sets from the geometry splits:

| Probe | Train queries | Validation queries | Test queries | Maximum updates |
|---|---:|---:|---:|---:|
| Global linear | 100,000 observations | 20,000 | 20,000 | 10,000 |
| Coordinate geometry | 1,000,000 coordinate queries | 100,000 | 100,000 | 50,000 |
| Topology pair | 500,000 balanced cell pairs | 50,000 | 50,000 | 50,000 |
| Probe decoder | 100,000 observations | 10,000 | 10,000 | 100,000 |

Probe optimization uses AdamW and selects learning rate from `1e-4, 3e-4, 1e-3`
and weight decay from `0, 1e-4, 1e-3` on validation data. Batch size is the largest
power of two that fits every compared encoder, capped at 512 queries or 64 decoded
observations. Early stopping patience is five validations. Once selected for a probe
task, its hyperparameters are reused for all encoders; they are not retuned per
checkpoint.

## Dataset and split protocol

### Split by geometry, never by observation

Nearby observations from the same geometry are strongly correlated. Randomly
splitting observation rows leaks obstacle layout into validation. Assign entire
geometries before sampling observations:

| Split | Share | Purpose |
|---|---:|---|
| Train | 70% | encoder pretraining and probe training subsets |
| Validation | 15% | checkpoint, recipe, and threshold selection |
| Test | 15% | one-time final certification |

The test split remains unopened until the recipe, checkpoint, and probe
hyperparameters are locked. Dataset hashes and geometry IDs must be artifacts.

### Geometry strata

Every split must cover the same declared strata, with separate reports for each:

- procedural boxes and open rooms;
- thin walls and isolated obstacles;
- narrow corridors, branches, loops, and dead ends;
- imported STL or reconstructed real geometry;
- low, medium, and high occupied fractions; and
- radii and voxel strides supported by the checkpoint.

At least one topology family and one imported-geometry family must be held out
entirely from pretraining. This out-of-family test is reported separately from the
ordinary test split.

### Sampling balance

Do not sample uniformly from free space. Build each training epoch from these strata:

| Sample type | Target share |
|---|---:|
| obstacle boundary or surface | 30% |
| corridor, junction, bottleneck, or dead end | 30% |
| ordinary traversable space | 25% |
| open or nearly empty space | 10% |
| unknown/boundary-of-observation cases | 5% |

Shares may move by at most 5 percentage points after the dataset audit. Empty samples
must not exceed 10%. Sample type, geometry family, radius, and occupied fraction must
be logged so a model cannot improve an aggregate by exploiting a changed mixture.

### Radius balance

For the multiresolution encoder, draw requested radii uniformly from
`2, 4, 8, 16, 32, 64, 128, 256, 512` at final training. A batch contains one radius
bucket so tensor shapes remain regular. Gradient accumulation makes the effective
number of observations comparable across radii.

## Baselines and controls

Every certification report includes:

- majority-class and occupancy-frequency predictors;
- a random frozen encoder with the same architecture;
- a fixed random projection or PCA baseline over the same voxel input;
- the current pretrained `VoxelEncoder3D` checkpoint at supported radii;
- the current tri-planar encoder at supported radii; and
- a fully supervised encoder trained on each probe target as an upper-reference
  model, clearly marked as non-comparable training.

The pretrained checkpoint must beat both its random-weight counterpart and the best
non-neural baseline on the critical frozen probes. The supervised reference estimates
whether a weak score reflects the representation or an impossible dataset/task.

## Metric suite

### 1. Pretext metrics

Use pretext metrics for early stopping and debugging only:

- class-balanced masked cross-entropy or BCE;
- occupied IoU and macro F1 on masked valid cells;
- precision-recall AUC for occupied cells;
- clearance normalized MAE; and
- each auxiliary loss separately, never only the weighted sum.

Report results by mask ratio, radius, and geometry stratum. Metrics on unmasked cells
do not count toward masked reconstruction quality.

### 2. Collapse and representation diagnostics

On at least 10,000 held-out observations, report:

- RankMe effective rank and effective-rank fraction `rank / embedding_dim`;
- count of near-dead dimensions with standard deviation below `1e-3` after each
  dimension is centered;
- largest principal-component explained-variance share;
- mean off-diagonal absolute correlation;
- embedding norm mean and standard deviation; and
- alignment/uniformity for methods trained with paired views.

These diagnostics are scale-sensitive. Compute them from the raw encoder output and
from L2-normalized output, record the exact formulas, and compare only like with like.

### 3. Frozen coordinate probes

Sample coordinates uniformly within the valid region, then rebalance the query set by
class or distance bin. The coordinate probe predicts:

- occupied, known-free, and unknown class;
- truncated signed distance or clearance;
- boundary membership and nearest-boundary direction; and
- local occupancy fraction at each represented stride.

Required measures are occupied IoU, macro F1, boundary F1 with one-voxel tolerance,
clearance normalized MAE, 95th-percentile absolute error, and direction cosine error.

### 4. Frozen topology probes

For balanced free-cell pairs, the coordinate-pair probe predicts:

- whether the cells are connected through known free space;
- normalized shortest-path or geodesic distance when connected; and
- the minimum clearance along that reference path.

Required measures are reachability AUROC, AUPRC, balanced accuracy, geodesic
normalized MAE, geodesic Spearman correlation, and bottleneck-clearance normalized
MAE. Also calculate false-open and false-closed rates on the dedicated thin-wall and
narrow-corridor suites. A false-open prediction is more severe because it claims a
blocked connection exists.

### 5. Reconstruction topology

Threshold the standardized probe decoder's occupancy prediction using a threshold
selected on validation data. Compare reconstructed and target volumes using:

- connected-component count error for known free space;
- fraction of sampled cell pairs whose connectivity changed;
- occupied boundary F1;
- skeleton or centerline overlap where a reference centerline exists; and
- clDice for corridor and tubular-geometry subsets.

This group detects a one-voxel hole or broken corridor that ordinary IoU can obscure.

### 6. Robustness and consistency

Evaluate without retraining under:

- all 24 proper cube rotations;
- translations that keep the queried physical region valid;
- 0.5% and 1.0% random cell corruption;
- removal of 5% and 10% of observed cells into the unknown class;
- voxel-scale and obstacle-density strata; and
- adjacent radius/stride representations of the same physical neighborhood.

Do not require rotation-invariant embeddings: orientation can be necessary to recover
spatial relationships. Require probe quality to be stable after applying the same
transform to the input and query coordinates. For adjacent scales, compare predictions
over their shared physical support rather than raw latent cosine unless the
architecture explicitly defines an equivariant latent transform.

### 7. Efficiency

Measure on declared reference CPU and accelerator hardware:

- unique observations and updates to each validation threshold;
- wall-clock time and accelerator-hours to the selected checkpoint;
- samples per second and valid voxels per second;
- peak allocated and reserved accelerator memory;
- checkpoint size and parameter count; and
- batch-1 p50 and p95 encoder latency at every radius.

Dataset generation, target generation, and training time are reported separately.
All runs must state precision mode, device, software versions, compilation settings,
and whether scale levels were processed sequentially or batched.

## Provisional certification thresholds

These thresholds are deliberately stricter than a successful training run and apply
to the locked, untouched test split. They are provisional until the dataset audit
confirms that the supervised upper-reference model can exceed each threshold by at
least 5 percentage points or reduce each error threshold by at least 20%. If it
cannot, fix the probe or dataset; do not lower a threshold after seeing model test
results.

In this plan, **critical metrics** means occupied IoU, three-class macro F1,
clearance normalized MAE, reachability AUPRC, geodesic normalized MAE, false-open
rate, and false-closed rate. A composite or average score cannot hide failure of one
of these metrics.

### Hard gates

| Group | Minimum passing result |
|---|---|
| Reproducibility | Same checkpoint and input produce `max_abs_error <= 1e-5` on the same device in evaluation mode. |
| State integrity | Encoder state hashes are identical before and after every frozen-probe run. |
| Effective rank | At least `max(32, 0.25 * embedding_dim)` and no more than 5% near-dead dimensions. |
| Dominant component | Largest principal component explains no more than 35% of embedding variance. |
| Occupancy | Occupied IoU >= 0.75 and three-class macro F1 >= 0.85. |
| Boundary | One-voxel-tolerance boundary F1 >= 0.85. |
| Clearance | Normalized MAE <= 0.10 and 95th-percentile error <= 0.25 of truncation distance. |
| Reachability | AUROC >= 0.95, AUPRC >= 0.90, and balanced accuracy >= 0.90. |
| Geodesic distance | Normalized MAE <= 0.15 and Spearman correlation >= 0.90 on reachable pairs. |
| Bottleneck clearance | Normalized MAE <= 0.15. |
| False-open topology | <= 1.0% on thin-wall and narrow-corridor suites. |
| False-closed topology | <= 5.0% on thin-wall and narrow-corridor suites. |
| Pairwise topology reconstruction | <= 3.0% of sampled free-cell pairs change connectivity. |
| Out-of-family generalization | No critical metric loses more than 10% relative to the ordinary held-out test result. |
| Rotation robustness | No critical metric loses more than 3 percentage points over proper cube rotations. |
| Corruption robustness | No critical metric loses more than 5 percentage points at 1% cell corruption or 10% observed-cell removal. |
| Radius retention | Adding a coarser level reduces no already-supported-radius critical metric by more than 2 percentage points. |
| Radius 512 execution | Batch-1 inference completes without OOM and without constructing a dense volume larger than 33 per level. |
| Radius resource scaling | Radius-512 peak memory <= 1.5x radius-16 peak memory and p95 latency <= 6.5x radius-16 latency when six levels run sequentially. |
| Training budget | The selected checkpoint passes validation gates by 200,000 encoder updates. |

### Baseline-relative gates

In addition to the hard gates, pretraining must demonstrate that it created useful
features. Against the same architecture with random frozen weights, it must achieve:

- at least +0.10 absolute occupied IoU;
- at least +0.10 absolute reachability AUPRC;
- at least 20% lower clearance normalized MAE;
- at least 20% lower geodesic normalized MAE; and
- at least 25% fewer labeled examples to reach 90% of its full-data probe score.

It must beat the best PCA/random-projection baseline on every critical metric. A
checkpoint that passes absolute thresholds but fails these comparisons is not evidence
that pretraining helped and must not be published as pretrained.

### Few-label probe gate

Train each probe with 1%, 10%, and 100% of its labeled training queries. At 10%, the
encoder must retain at least 90% of its 100%-data score after converting lower-is-
better errors to `1 - normalized_error`. This tests accessibility of geometry without
allowing a large probe dataset to compensate for weak features.

### Statistical gate

Final certification uses five encoder seeds. Each probe uses three probe seeds per
encoder seed. Report mean, standard deviation, and a 95% bootstrap confidence
interval over geometry IDs. Every hard gate must be passed by the mean, and the lower
confidence bound for higher-is-better critical metrics must be no more than 2
percentage points below its gate. No single encoder seed may miss a critical gate by
more than 5 percentage points.

## Candidate pretraining recipes

Change one recipe component at a time. The following sequence is intentionally not a
full factorial search.

| ID | Recipe | Purpose |
|---|---|---|
| R0 | Full autoencoder with class-balanced occupancy reconstruction | Existing baseline and empty-space shortcut check. |
| R1 | Random-cell masked occupancy modeling | Existing MVM baseline. |
| R2 | Contiguous patch masking at one scale | Test whether spatial completion is more useful than isolated-cell prediction. |
| R3 | Hierarchical neighborhood masking and occupancy targets at every active scale | NOMAE-inspired primary candidate. |
| R4 | R3 + clearance, boundary, and nearest-boundary-direction targets | Geometry-aware candidate inspired by GeoMAE. |
| R5 | R4 + reachability, geodesic, and bottleneck-clearance targets | Topology-aware procedural supervision. |
| R6 | R4 + VICReg consistency across topology-preserving views | Negative-free consistency candidate. |
| R7 | R4 + contrastive projection head | PointContrast/DepthContrast-style comparison. |
| R8 | R4 + EMA self-distillation across mask ratios and scales | MM-3DScene-style consistency comparison. |
| R9 | Best of R5-R8 with only additions that passed ablation | Final combined candidate. |

R5 labels come from exact voxel geometry algorithms, not a policy, reward, rollout, or
RL model. R7's projection head and every decoder or auxiliary head are discarded.

## Training method search

### Masking

For R2 and later, screen mask ratios `0.40, 0.60, 0.75, 0.85` and patch sides
`2, 4, 8`. Sample occupied-boundary, free-space, and unknown patches separately so a
batch has declared class coverage. Reject a masking scheme if coordinates, validity
metadata, or decoder inputs directly reveal the masked occupancy label.

Use `0.60` as the first trial rather than assuming the 2D MAE value of `0.75` transfers
to sparse 3D. Extensive masking can disconnect sparse evidence. Promote a mask ratio
by frozen-probe score, not by reconstruction loss.

### Losses

- Occupancy: class-balanced cross-entropy for occupied/free/unknown; compare focal
  gamma `0, 1, 2` only if occupied precision-recall remains poor.
- Clearance and geodesic: Smooth L1 over values normalized by the declared maximum.
- Boundary direction: cosine loss plus a valid-boundary mask.
- Reachability: balanced BCE; sample equal reachable and unreachable pairs.
- Consistency: VICReg variance/invariance/covariance terms or an EMA-teacher loss.

Normalize every component by its initial moving standard deviation before applying
static weights. Start with equal normalized weights. Compare uncertainty or
gradient-norm weighting only after R5 shows conflicting gradients. Log each raw and
weighted loss and the cosine similarity between objective gradients on a fixed batch.

### Optimizer

Use AdamW with cosine decay, 5% linear warmup, gradient clipping at global norm 1.0,
and mixed precision. Tune this bounded space on Tiny and freeze it before architecture
comparison:

| Parameter | Values |
|---|---|
| Peak learning rate | `1e-4`, `3e-4`, `1e-3` |
| Weight decay | `0.01`, `0.05`, `0.10` |
| Effective batch | `128`, `256`, `512` observations |
| Decoder/encoder width ratio | `0.125`, `0.25`, `0.50` |

Use gradient accumulation when a radius does not fit the effective batch. Contrastive
runs use the same number of encoded views, not merely the same sample count. Report
both updates and encoded valid voxels so methods receive comparable compute.

### Augmentation

The safe initial set is proper cube rotations, translations that retain query support,
masking, and conversion of observed cells to unknown. Do not flip occupied to free,
apply elastic deformations, or cut a corridor without regenerating topology targets.

Compare four policies: none, rotation only, rotation plus translation, and the safe
full set. Select by held-out robustness and topology probes. Augmentation parameters
become part of checkpoint metadata.

### Checkpoint selection and stopping

Evaluate pretext metrics every epoch or 1,000 updates, collapse diagnostics every
5,000 updates, and the fixed validation probe suite every 10,000 updates. Select
lexicographically:

1. reject any checkpoint failing collapse or numerical-integrity gates;
2. reject any checkpoint regressing false-open rate;
3. maximize the mean normalized validation score across occupancy, clearance,
   reachability, and geodesic probes; then
4. break ties within 1% by lower training compute and lower inference memory.

Early stopping requires no improvement greater than 0.5 percentage points in the
normalized validation score for three consecutive probe evaluations. Never select a
checkpoint on test metrics.

## Experiment stages

### Stage 0: Harness and target validation

No encoder training.

- implement geometry-level splits and dataset hashes;
- verify occupancy, clearance, boundary, connectivity, geodesic, and bottleneck
  targets against hand-checked micro-scenes;
- implement majority, random encoder, PCA, and supervised upper references;
- lock probe capacities and search spaces; and
- verify every metric on perfect, empty, random, one-voxel-hole, and broken-corridor
  predictions.

Exit: perfect predictions pass every hard gate, known failures trigger the expected
gate, and no geometry ID crosses splits.

### Stage 1: Cheap recipe pilot

Use Tiny, radii through 32, 100,000 unique observations, 10,000 updates, and one seed.
Run R0-R4 plus the random-weight control. Use ASHA with a 2,000-update grace period to
screen optimizer, mask, and augmentation choices.

Exit: retain at most two configurations per recipe. They must beat the random encoder
on at least three of occupancy, clearance, reachability, and effective rank. Results
do not certify a model.

### Stage 2: Objective selection

Use Tiny, radii through 32, 1 million unique observations, 50,000 updates, and three
encoder seeds. Compare R1-R8 with the Stage 1 optimizer fixed. For additive recipes,
initialize from the same parent checkpoint and count all parent compute.

Exit: an objective is retained only if it improves at least one critical frozen-probe
metric by 2 percentage points or lowers a critical normalized error by 10%, while no
other critical metric regresses more than 2 percentage points. Retain at most three
recipes.

### Stage 3: Architecture selection

Use the best retained recipe, radii through 32, 1 million observations, 100,000
updates, and three seeds. Compare:

- current dense `VoxelEncoder3D`;
- pre-activation dense 3D ResNet;
- tri-planar 2D encoder;
- Tiny shared-backbone voxel pyramid;
- voxel pyramid with per-scale adapters; and
- sparse residual encoder if its runtime dependency is available.

The two-branch dilation/Inception variant is tested only against the winning residual
architecture at matched parameters within 10%.

Exit: select one primary and one fallback architecture using frozen-probe score,
false-open rate, peak memory, and latency. The primary must improve the mean normalized
probe score by at least 3 percentage points over the current encoder or match it while
reducing peak memory or latency by at least 25%.

### Stage 4: Radius scaling

Keep architecture, capacity, optimizer, data count per radius, and objective fixed.
Train/evaluate maximum-radius checkpoints at `16, 32, 64, 128, 256, 512`. For the
shared pyramid, warm-start each checkpoint from the previous radius and retain 50% of
batches from earlier radii. Train one radius-128 checkpoint from scratch to measure
whether warm-starting changes the conclusion.

Budget: 100,000 updates and three seeds per maximum radius, stopping earlier only by
the locked rule.

Exit per radius: pass radius retention, improve at least one wide-context topology or
geodesic metric by 2 percentage points/10% error, and add no more than one scale
level's declared compute. Stop increasing radius if two consecutive levels add no
probe benefit.

### Stage 5: Data scaling

Hold Base architecture and maximum useful radius fixed. Train on `0.1M, 0.3M, 1M,
3M, 10M` unique observations for a fixed 100,000 updates and three seeds. Then repeat
the two largest datasets with equal-epoch rather than equal-update budgets to separate
data diversity from optimization time.

Fit learning curves against unique observations and encoded valid voxels. Exit when
tripling data improves no critical metric by 1 percentage point and lowers no critical
error by 5%. The smallest dataset on that plateau becomes the reference corpus.

### Stage 6: Capacity scaling

Train Tiny, Base, and Large on the reference corpus and maximum useful radius with the
same recipe. Use 200,000 updates, three seeds, and identical probe budgets. Train from
scratch for the scientific comparison; weight inflation or partial loading may be
measured as a separate efficiency experiment.

Promote Tiny to Base only for at least +2 percentage points in mean normalized probe
score or a 10% reduction in a critical error. Promote Base to Large only for at least
+1 percentage point or a 5% critical-error reduction, with no hard-gate regression.
Report quality per million parameters, accelerator-hour, and millisecond.

### Stage 7: Final standalone certification

Lock recipe, architecture, capacity, radius, corpus, and checkpoint selection. Train
five fresh encoder seeds for the full 200,000-update budget. Train the three probe
seeds per encoder seed, open the test split once, and run the complete metric suite.

Exit: every hard, baseline-relative, few-label, statistical, and hardware gate passes.
Only then may the checkpoint be labeled `validated` and published in the model garden.
Failure leaves it as `experimental`; do not choose a new recipe using test results.

## Run matrix and cost control

The maximum planned run count before early stopping is:

| Stage | Full runs | Seeds | Maximum encoder trainings |
|---|---:|---:|---:|
| 1 recipe pilot | up to 24 ASHA trials | 1 | 24 partial |
| 2 objective selection | 8 recipes | 3 | 24 |
| 3 architecture selection | up to 7 variants | 3 | 21 |
| 4 radius scaling | 6 maxima + 1 scratch control | 3 | 21 |
| 5 data scaling | 7 budgets | 3 | 21 |
| 6 capacity scaling | 3 families | 3 | 9 |
| 7 certification | 1 locked candidate | 5 | 5 |

Do not execute this as one Cartesian sweep. Complete each exit decision and discard
losers before the next stage. Reuse immutable datasets and cached algorithmic targets,
but never reuse validation/test observations as pretraining input.

## Required artifacts and metric names

Each run must store resolved configuration, Git commit, dataset/split hashes, encoder
checkpoint, optimizer state, objective histories, collapse diagnostics, frozen-probe
configurations, per-geometry predictions, and an environment manifest.

Use stable metric prefixes:

```text
pretext/{objective}/{metric}
representation/rankme_effective_rank
representation/dead_dimension_fraction
representation/largest_pc_share
probe/occupancy/{metric}
probe/clearance/{metric}
probe/reachability/{metric}
probe/geodesic/{metric}
probe/topology/{metric}
robustness/{corruption}/{metric}
efficiency/{device}/{metric}
```

The certification command must emit `certification.json` containing every gate,
observed value, threshold, confidence interval, pass/fail result, and links to raw
artifacts. A single failed hard gate makes the top-level result `failed`.

## Recommended first execution

Implement Stage 0 before changing the encoder. Then run Stage 1 with R0, R1, R3, and
R4 only. This determines whether the existing reconstruction objective has an
empty-space shortcut and whether multi-scale neighborhood masking plus geometric
targets improves frozen features. Do not train Base or Large until a Tiny recipe
passes Stage 2 promotion rules.
