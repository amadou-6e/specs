# Proposed certification protocol: standalone voxel encoder pretraining

This page preserves the proposed qualification protocol associated with the model
registry. It is not the implemented registry contract: current publication does not
run these gates, emit `certification.json`, or enforce `experimental` versus
`validated` status. Executed protocols and results belong under the experiments
category; this page states the intended promotion criteria they would need to
satisfy.

Status: discovery
Owner: amadou-6e
Last reviewed: 2026-09-01
Tracking issue: [specs#7](https://github.com/amadou-6e/specs/issues/7)
Literature revision: [specs#9](https://github.com/amadou-6e/specs/issues/9)
Methodology revision: [specs#11](https://github.com/amadou-6e/specs/issues/11)
Related research: [Scalable 3D Voxel Perception Encoders](../../../research/perception-encoders.md)
Direction pilots: [Voxel Encoder Direction-Finding Pilots](../../../experiments/perception-encoder-r0/preregistration.md)
Governing specification: [Model Garden architecture](../../../architecture/README.md)

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
- [Scaling and Benchmarking Self-Supervised Visual Representation Learning](https://arxiv.org/abs/1905.01235)
  and [Ericsson et al.](https://arxiv.org/abs/2011.13377) show that transfer rankings
  depend on the target task and evaluation protocol. Frozen probes are standardized
  accessibility tests, not guaranteed predictors of fine-tuned ranking.
- [Masked Autoencoders](https://arxiv.org/abs/2111.06377) use an asymmetric design in
  which the encoder processes visible tokens and a lightweight decoder reconstructs
  masked content. The decoder is discarded after pretraining. Compute savings from
  visible-token encoding do not automatically apply to a dense CNN that still
  processes every masked voxel.
- [VICReg](https://arxiv.org/abs/2105.04906) explicitly controls invariance, per-feature
  variance, and covariance to avoid collapsed or redundant embeddings without
  requiring negative pairs.
- [BYOL](https://arxiv.org/abs/2006.07733) provides the online/EMA-target precedent
  for negative-free prediction, while DINO below provides a related self-distillation
  design. Predictor and projector capacity remain comparison confounds.
- [Alignment and uniformity](https://arxiv.org/abs/2005.10242) provide intrinsic
  diagnostics for contrastive representations, but they are not substitutes for
  task-relevant probes.
- [RankMe](https://proceedings.mlr.press/v202/garrido23a.html) proposes effective rank
  as a label-free signal for selecting self-supervised representations. It is useful
  for rejecting collapse and screening checkpoints, not as the sole acceptance gate.
- [SwAV](https://arxiv.org/abs/2006.09882) and
  [DINO](https://arxiv.org/abs/2104.14294) establish multi-view assignment and
  self-distillation objectives. [DenseCL](https://arxiv.org/abs/2011.09157),
  [PixPro](https://arxiv.org/abs/2011.10043), and
  [VADeR](https://arxiv.org/abs/2011.05499) show why dense, corresponding locations
  matter when transfer requires spatial predictions. Cross-scale voxel consistency
  should therefore use known physical correspondences, not only global embeddings.
- [Hewitt and Liang](https://aclanthology.org/D19-1275/) show that a capable probe can
  learn a task instead of exposing information in a representation. Certification
  therefore requires control-target selectivity plus zeroed and shuffled embedding
  ablations, not only random-encoder and PCA floors.
- [Fine-Tuning can Distort Pretrained Features](https://arxiv.org/abs/2202.10054)
  establishes that frozen and adapted evaluations can rank or generalize differently.
  A small geometry-only adaptation check accompanies recipe and architecture ranking,
  but it does not become a policy or standalone certification metric.

### What frozen embodied encoders establish

- [R3M](https://arxiv.org/abs/2203.12601),
  [MVP](https://arxiv.org/abs/2203.06173),
  [PVR](https://arxiv.org/abs/2203.03580),
  [VIP](https://arxiv.org/abs/2210.00030), and
  [VC-1](https://arxiv.org/abs/2303.18240) demonstrate reusable frozen visual
  encoders across embodied tasks. MVP is especially relevant because it discards a
  masked-pretraining decoder and reuses one large frozen encoder.
- This evidence is contested rather than uniform. VC-1 finds no universal winner,
  while [Hansen et al.](https://arxiv.org/abs/2212.05749) report that in-domain
  from-scratch training can be competitive and that fine-tuning can overcome domain
  mismatch. Theseo must prove frozen value against raw-input, random-feature, adapted,
  and from-scratch controls; it cannot inherit the conclusion from 2D robotics.

### What 3D masked pretraining suggests

- [PointContrast](https://arxiv.org/abs/2007.10985) and
  [DepthContrast](https://arxiv.org/abs/2101.02691) show that contrastive 3D
  representations can transfer across datasets and tasks, but view construction is a
  major part of the method.
- [Point-MAE](https://arxiv.org/abs/2203.06604) and
  [MaskPoint](https://arxiv.org/abs/2203.11183) apply masked modeling to point clouds
  with coordinate reconstruction or masked point discrimination. Their point-patch
  assumptions are not identical to known-free voxel occupancy.
- [Point-M2AE](https://arxiv.org/abs/2205.14401) uses consistent visible regions
  across a hierarchical point pyramid and reports strong frozen linear evaluation.
  It supports multi-scale masking but does not establish Theseo's fixed-grid design.
- [Occupancy-MAE](https://arxiv.org/abs/2206.09900) and
  [Voxel-MAE](https://arxiv.org/abs/2207.00531)
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
- [SparK](https://arxiv.org/abs/2301.03580) and
  [ConvNeXt V2/FCMAE](https://arxiv.org/abs/2301.00808) show that masked ConvNet
  pretraining needs a sparse visible-cell encoder path and hierarchical decoder;
  feeding a zero-masked dense volume through ordinary convolutions does not inherit
  MAE's information isolation or compute savings.
- [iBOT](https://arxiv.org/abs/2111.07832) combines masked prediction with an online
  teacher, while [data2vec](https://arxiv.org/abs/2202.03555) predicts contextualized
  latent teacher features from a masked view. Both motivate first-class latent-target
  recipes that avoid occupancy class imbalance, though geometry probes must still
  prove that the learned targets preserve obstacle and topology information.
- [clDice](https://openaccess.thecvf.com/content/CVPR2021/html/Shit_clDice_-_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_CVPR_2021_paper.html)
  demonstrates that volumetric overlap can hide connectivity errors and provides a
  topology-aware 2D/3D measure. Theseo should likewise measure connectivity rather
  than accepting voxel IoU alone.
- [Voxblox](https://arxiv.org/abs/1611.03631) and
  [FIESTA](https://arxiv.org/abs/1903.02144) establish truncated Euclidean signed-
  distance fields as useful mapping products for planning. They motivate a truncated
  ESDF as the primary dense geometric target, while exact collision checks remain
  outside the learned representation.
- [Semi-parametric Topological Memory](https://arxiv.org/abs/1803.00653),
  [Search on the Replay Buffer](https://arxiv.org/abs/1906.05253), and
  [Sparse Graphical Memory](https://arxiv.org/abs/2003.06417) show that learned
  reachability or distance relations can support graph search. They are precedents for
  topology probes, not evidence that a policy-conditioned value belongs in this
  goal-independent encoder.

### Synthesis

The most defensible initial recipe uses truncated ESDF prediction as its primary dense
target, frontier-biased multi-scale masked occupancy as a complementary target, and
physically aligned local consistency over overlapping scales. Contrastive learning
and self-distillation are comparisons, not assumed defaults. Exact geometry can
generate clearance, connectivity, and geodesic targets automatically, so standalone
certification can test path-relevant spatial information without a policy or RL
system.

## What counts as independent encoder validation

The encoder is loaded from its checkpoint, put in evaluation mode, and frozen. Every
parameter must have `requires_grad = false`, and encoder inference must run under
`no_grad`. Probe training must verify before and after SHA-256 hashes over sorted
tensor names, dtypes, shapes, and raw tensor bytes are identical.

Three readout classes are allowed:

1. **Linear probe**: one affine map from the global embedding.
2. **Coordinate probe**: an MLP with two hidden layers of width 64 by default reading
   `[global_embedding, sampled_local_feature, query_coordinates, stride_metadata]`.
   Report global-only, local-only, and combined variants with the same capacity cap.
   A width-128 variant is the absolute ceiling and is allowed only when preregistered
   for every comparison and its selectivity controls pass.
3. **Probe decoder**: a decoder no larger than 25% of encoder parameter count or one
   million parameters, whichever is smaller, used only for masked occupancy and
   topology reconstruction.

The same probe architecture, optimizer search space, update budget, and labeled
sample count must be used for every learned encoder in a comparison. The raw-grid
control's minimal input adapter is preregistered, counts against the same parameter and
update cap, and may not be retuned per recipe. A result from a larger or separately
tuned probe is invalid.

The coordinate decoder follows the conditioning pattern used by
[Occupancy Networks](https://arxiv.org/abs/1812.03828),
[DeepSDF](https://arxiv.org/abs/1901.05103), and
[Learning Implicit Fields for Generative Shape Modeling](https://arxiv.org/abs/1812.02822):
combine a spatial query with a scene code, but restrict capacity so the decoder cannot
become the representation. Coordinates are agent-centered, normalized by requested
radius, and accompanied by physical voxel size and stride; no absolute geometry ID or
world coordinate is allowed.

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

### Probe selectivity and embedding ablations

Every coordinate and topology probe run includes three paired controls with the same
initialization, optimizer, batches, and update budget:

1. **Control target**: replace real labels with a fixed random assignment that
   preserves the label or regression-bin marginal within geometry-family, radius, and
   occupancy-density strata. Hash `(split, geometry_id, query_id, control_seed)` so
   the assignment is deterministic and cannot cross splits.
2. **Zero embedding**: replace global and local encoder features with zeros while
   retaining coordinates and metadata.
3. **Shuffled embedding**: permute complete observation embeddings across different
   geometry IDs in the batch while retaining each query's coordinates and labels.

Following [control-task selectivity](https://aclanthology.org/D19-1275/), convert each
metric to a preregistered `[0, 1]` higher-is-better score and report
`selectivity = real_target_score - control_target_score`. Also report the gap from the
real-embedding score to the better of zeroed and shuffled embeddings. The same control
seed is reused for all encoders. A probe that performs well without the matching
embedding is invalid even when the encoder beats random weights.

## Dataset and split protocol

### Split by geometry, never by observation

Nearby observations from the same geometry are strongly correlated. Randomly
splitting observation rows leaks obstacle layout into validation. This is a blocked
cross-validation requirement consistent with
[Roberts et al.](https://doi.org/10.1111/ecog.02881). Assign entire geometries before
sampling observations:

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

### Locked evaluation mixture

Stage 0 freezes validation and test query IDs, exact per-stratum counts, and aggregate
weights independently of the training sampler. The training shares above may move by
their declared 5 percentage points, but validation/test composition never follows
those changes. Every report includes fixed-weight aggregates and unweighted results
for every geometry family, radius, occupancy-density, and topology stratum. Changing
an evaluation weight or query requires a new dataset version and invalidates prior
comparisons; test weights cannot change after any test result is opened.

### Radius balance

For the multiresolution encoder, draw requested radii uniformly from
`2, 4, 8, 16, 32, 64, 128, 256, 512` at final training. A batch contains one radius
bucket so tensor shapes remain regular. Gradient accumulation makes the effective
number of observations comparable across radii.

## Baselines and controls

Every certification report includes:

- majority-class and occupancy-frequency predictors;
- raw conservative multiscale grids consumed by capacity-matched coordinate and
  decoder probes, with no pretrained encoder. The minimal trainable input adapter
  needed to consume grid channels counts against the same probe parameter and update
  budget, so this control measures learning perception in the head from raw geometry;
- a random frozen encoder with the same architecture;
- a fixed random projection or PCA baseline over the same voxel input;
- the current pretrained `VoxelEncoder3D` checkpoint at supported radii;
- the current tri-planar encoder at supported radii; and
- a deliberately over-capacity fully supervised encoder or three-model ensemble for
  each probe target, clearly marked as non-comparable training. It uses at least four
  times the candidate's parameters, trains to validation convergence, and is selected
  for ceiling quality rather than deployment efficiency.

The pretrained checkpoint must beat its random-weight counterpart, raw-grid control,
and best other non-neural baseline on the declared baseline-relative gates. The raw
control answers whether learning compression adds accessible geometry beyond the
conservative pyramid itself. The supervised reference estimates whether a weak score
reflects the representation or an impossible dataset/task. It is not architecture-
matched: an under-powered reference would make certification thresholds artificially
easy. Record ensemble size, capacity, convergence curve, and residual label errors.

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
- eigenspectrum power-law decay exponent and fit quality following
  [alpha-ReQ](https://papers.neurips.cc/paper_files/paper/2022/hash/70596d70542c51c8d9b4e423f4bf2736-Abstract-Conference.html);
- [LiDAR](https://arxiv.org/abs/2312.04000) linear-discriminant rank for joint-
  embedding recipes whose view identities define a valid surrogate task;
- mean off-diagonal absolute correlation;
- embedding norm mean and standard deviation; and
- alignment/uniformity for methods trained with paired views.

These diagnostics are scale-sensitive. Compute them from the raw encoder output and
from L2-normalized output, record the exact formulas, and compare only like with like.
[Dimensional-collapse analysis](https://arxiv.org/abs/2110.09348) motivates tracking
the complete singular-value spectrum rather than only constant embeddings. Keep
`0.25 * embedding_dim` as the rejection floor, but target at least
`0.50 * embedding_dim` during validation selection.

Alpha-ReQ and LiDAR are tracked diagnostics, not universal gates. Alpha-ReQ is valid
only when the log-log spectral fit has `R^2 >= 0.90`,
and LiDAR does not apply to reconstruction-only recipes. Before either metric can
select checkpoints, Stage 2 must establish its rank correlation with the fixed frozen
probe aggregate on this voxel corpus. RankMe remains in the report even when another
spectral diagnostic correlates better.

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
- foreground-restricted Variation of Information normalized by `log(valid_cells)` and
  adapted Rand error over connected-component labels, following the evaluation in
  [Arganda-Carreras et al.](https://doi.org/10.3389/fnana.2015.00142);
- absolute Betti-number error for `beta_0` components and `beta_1` loops, following
  [topology-preserving segmentation](https://arxiv.org/abs/1906.05404);
- occupied boundary F1;
- skeleton or centerline overlap where a reference centerline exists; and
- clDice for corridor and tubular-geometry subsets.

This group detects a one-voxel hole or broken corridor that ordinary IoU can obscure.
Variation of Information and adapted Rand error are required on all volumes. Betti
errors are required when the exact cubical-complex implementation fits the Stage 0
resource budget; otherwise record them as a deferred diagnostic with the measured
cost, never silently omit them.

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

For every critical metric, report the canonical-orientation value, mean over the 24
rotations, standard deviation over rotations, worst-rotation value, and worst-case
degradation from canonical. `robustness/rotation/worst_degradation` is a first-class
gate, not a supplemental chart. Reflections are excluded unless the data contract
explicitly proves handedness and channel semantics are reflection symmetric.

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
| Mask isolation | For masked recipes, changing only hidden voxel values changes no visible encoder feature by more than `1e-6`, and the gradient of any encoder output with respect to hidden input values is zero or has `max_abs <= 1e-8`. |
| Mask shortcut | With encoder features zeroed, a decoder receiving only mask geometry scores no more than 2 percentage points above the frequency baseline conditioned on mask-sampling stratum for any masked target. |
| Effective rank | At least `max(32, 0.25 * embedding_dim)` and no more than 5% near-dead dimensions. |
| Dominant component | Largest principal component explains no more than 35% of embedding variance. |
| Probe selectivity | Mean normalized control-task selectivity is >= 0.10 for coordinate and topology probes, with no critical metric below 0.05. |
| Embedding necessity | Mean normalized score exceeds the better of zeroed and shuffled embeddings by >= 0.10, with no critical metric favoring an ablation. |
| Occupancy | Occupied IoU >= 0.75 and three-class macro F1 >= 0.85. |
| Boundary | One-voxel-tolerance boundary F1 >= 0.85. |
| Clearance | Normalized MAE <= 0.10 and 95th-percentile error <= 0.25 of truncation distance. |
| Reachability | AUROC >= 0.95, AUPRC >= 0.90, and balanced accuracy >= 0.90. |
| Geodesic distance | Normalized MAE <= 0.15 and Spearman correlation >= 0.90 on reachable pairs. |
| Bottleneck clearance | Normalized MAE <= 0.15. |
| False-open topology | <= 1.0% on thin-wall and narrow-corridor suites. |
| False-closed topology | <= 5.0% on thin-wall and narrow-corridor suites. |
| Pairwise topology reconstruction | <= 3.0% of sampled free-cell pairs change connectivity. |
| Component partition | Normalized foreground-restricted Variation of Information <= 0.05 and adapted Rand error <= 0.05. |
| Out-of-family generalization | No critical metric loses more than 10% relative to the ordinary held-out test result. |
| Rotation robustness | Worst-rotation degradation is <= 3 percentage points for every higher-is-better critical metric and <= 0.03 normalized error for every lower-is-better critical metric over the 24 proper cube rotations. |
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

It must beat the best PCA/random-projection baseline on every critical metric. Against
the raw conservative-grid control, it must improve the preregistered mean normalized
probe score by at least 3 percentage points or reduce labeled examples to 90% of the
full-data score by at least 25%, while losing no higher-is-better critical metric by
more than 2 percentage points and increasing no normalized critical error by more than
10%. A checkpoint that passes absolute thresholds but fails these comparisons is not
evidence that learned compression helped and must not be published as pretrained.

### Few-label probe gate

Train each probe with 1%, 10%, and 100% of its labeled training queries. At 10%, the
encoder must retain at least 90% of its 100%-data score after converting lower-is-
better errors to `1 - normalized_error`. This tests accessibility of geometry without
allowing a large probe dataset to compensate for weak features.

### Statistical gate

Final certification uses five encoder seeds. Each probe uses three probe seeds per
encoder seed. Following the robust reporting principles in
[rliable](https://arxiv.org/abs/2108.13264), report the mean, median, interquartile mean
(IQM), and 95% stratified cluster-bootstrap intervals. Geometry ID is the cluster:
resample complete geometry IDs within geometry
family, radius, and occupancy-density strata, and preserve the nesting of encoder and
probe seeds; do not treat voxel queries as independent samples.

For each critical metric, both the mean and IQM must pass its hard threshold. The
conservative confidence bound may miss a higher-is-better threshold by at most 2
percentage points or a lower-is-better threshold by at most 0.02 normalized error.
Report paired probability of improvement against the random encoder and raw-grid
control, using identical geometry/seed units; it must exceed 0.95 for the
preregistered normalized aggregate. Include performance profiles showing the fraction
of critical metric/stratum pairs above every normalized threshold. No single encoder
seed may miss a critical gate by more than 5 percentage points or 0.05 normalized
error. Mean plus standard deviation alone is insufficient for certification.

## Candidate pretraining recipes

Change one recipe component at a time. The following sequence is intentionally not a
full factorial search.

| ID | Recipe | Purpose |
|---|---|---|
| R0 | Full autoencoder with class-balanced occupancy reconstruction | Existing baseline and empty-space shortcut check. |
| R1 | Random-cell masked occupancy modeling through a sparse visible-cell encoder | SparK/FCMAE-style MVM baseline. |
| R2 | Truncated ESDF prediction with boundary-balanced coordinate sampling | Primary dense-geometry baseline. |
| R3 | R2 + contiguous frontier-biased masked occupancy at one scale | Test whether spatial completion adds information beyond distance fields. |
| R4 | R3 + hierarchical neighborhood masks and targets at every active scale | Point-M2AE/NOMAE-inspired primary candidate. |
| R5 | R4 + reachability, geodesic, and bottleneck-clearance targets | Topology-aware procedural supervision. |
| R6 | R4 + physically aligned local VICReg consistency across overlapping scales/views | Negative-free dense-consistency candidate. |
| R7 | R4 + aligned local contrastive projection head | PointContrast/DepthContrast-style comparison. |
| R8 | R4 + EMA online-tokenizer self-distillation across masks and aligned scales | iBOT/MM-3DScene-style masked self-distillation. |
| R9 | Masked sparse encoder predicts contextualized EMA-teacher local features | data2vec-style latent-target candidate without occupancy class imbalance. |
| R10 | Best of R5-R9 with only additions that passed ablation | Final combined candidate. |

R5 labels come from exact voxel geometry algorithms, not a policy, reward, rollout, or
RL model. Every decoder, projector, predictor, and auxiliary head used by R0-R10 is
discarded; only the encoder is eligible for publication.

## Training method search

### Masking

For masked recipes, screen mask ratios `0.40, 0.60, 0.75, 0.85` and patch sides
`2, 4, 8`. Every observation must contain at least one nonempty masked patch. Draw
50% of patch centers from occupied boundaries or observed/unknown frontiers, 30% from
corridors or ordinary free space, and 20% from unknown regions; audit these shares by
radius. Compare full-patch loss with a surface/frontier-only target mask. Reject a
masking scheme if coordinates, validity metadata, or decoder inputs directly reveal
the masked occupancy label.

For every convolutional masked recipe, the default encoder path follows
[SparK](https://arxiv.org/abs/2301.03580) or
[FCMAE](https://arxiv.org/abs/2301.00808): remove hidden coordinates before the
encoder, apply sparse/submanifold convolutions only to visible coordinates, retain
multi-stage sparse features, and densify only inside the disposable decoder. Ordinary
dense convolution over zero, constant-token, or noise-filled hidden cells is not a
valid masked-ConvNet implementation.

If the selected deployment backend cannot support sparse training, a dense fallback
may advance only after implementing partial/mask-aware convolution and normalization
whose statistics use visible cells only. It must pass two Stage 0 intervention tests:

1. create paired tensors with identical visible cells and masks but adversarially
   different hidden values; every visible encoder feature and global embedding must
   satisfy the mask-isolation gate; and
2. differentiate every sampled encoder output with respect to hidden input values;
   the hidden-region Jacobian must satisfy the mask-isolation gradient gate.

Also train a decoder with encoder features zeroed and only the mask geometry exposed.
Its masked-target score must remain within 2 percentage points of the corresponding
frequency baseline conditioned on the mask-sampling stratum. This detects mask-shape
shortcuts even when hidden values are numerically isolated.

Use `0.60` as the first trial rather than assuming the 2D MAE value of `0.75` transfers
to sparse 3D. Extensive masking can disconnect sparse evidence. Promote a mask ratio
by frozen-probe score, not by reconstruction loss.

### Losses

- Occupancy: class-balanced cross-entropy for occupied/free/unknown; compare focal
  gamma `0, 1, 2` and full-patch versus surface/frontier-only supervision.
- ESDF and geodesic: Smooth L1 over values normalized by the declared physical
  truncation or maximum. Clip ESDF targets symmetrically and report boundary, free,
  occupied, and saturation-region errors separately.
- Boundary direction: cosine loss plus a valid-boundary mask.
- Reachability: balanced BCE; sample equal reachable and unreachable pairs.
- Consistency: map both views to a common physical frame, intersect validity masks,
  conservatively pool fine features to the coarse grid, and compare only corresponding
  local features. Use VICReg variance/invariance/covariance terms or an EMA-teacher
  stop-gradient loss. Do not minimize unaligned global cosine similarity as a proxy.

R6-R9 use one locked two-layer projection architecture, output dimension, hidden
width, normalization, and activation. Methods that require an extra predictor match
total projector-plus-predictor parameters within 5% by adjusting hidden width. Record
all head shapes and parameter counts in checkpoint metadata, and compare the same
number of encoded views and valid voxels.

Normalize every component by its initial moving standard deviation before applying
static weights. Start with equal normalized weights. Log each raw and weighted loss
and the cosine similarity between objective gradients on a fixed batch, following the
conflict diagnostic used by [PCGrad](https://arxiv.org/abs/2001.06782). If R5 has
persistent negative gradient cosine and a critical probe regression, compare PCGrad,
[GradNorm](https://arxiv.org/abs/1711.02257), and
[uncertainty weighting](https://arxiv.org/abs/1705.07115) under the same update and
compute budget. Promote a mitigation only if it resolves the regression; do not add
adaptive weighting to the default recipe preemptively.

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

### Training efficiency controls

- Generate occupancy, truncated ESDF, boundary, connectivity, and geodesic targets
  once from exact geometry code; content-address and reuse them across recipes.
- Process scale levels sequentially for the memory baseline and accumulate gradients
  before the optimizer step. A batched-scales variant must report its throughput and
  peak-memory tradeoff.
- Use BF16 where supported and FP16 only with dynamic loss scaling. Keep ESDF target
  generation and certification metrics in FP32 or higher precision.
- A masked transformer or sparse candidate may skip hidden tokens. A dense CNN must
  count every processed voxel even when its input value is masked; do not claim MAE-
  style compute savings unless profiling shows that masked locations were skipped.
- Enable activation checkpointing only when needed to fit the locked effective batch,
  and report recomputation time. Compilation and fused kernels are deployment
  measurements, not changes to the scientific architecture comparison.

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
2. reject any masked checkpoint failing isolation or mask-only shortcut tests;
3. reject any checkpoint failing selectivity or embedding-necessity gates, or
   regressing false-open rate;
4. maximize the mean normalized validation score across occupancy, clearance,
   reachability, and geodesic probes; then
5. among checkpoints within 1%, prefer effective-rank fraction >= 0.50, then lower
   training compute and lower inference memory.

Early stopping requires no improvement greater than 0.5 percentage points in the
normalized validation score for three consecutive probe evaluations. Never select a
checkpoint on test metrics.

### Geometry-only adaptation ranking check

Frozen-probe rank is not assumed to predict adaptation rank. For the top two Stage 2
recipes and top two Stage 3 architectures, run one validation-only geodesic regression
check with one fixed seed and no policy, reward, rollout, planner head, or RLlib:

1. attach the same two-layer width-64 geodesic head;
2. train only the head for 2,000 updates, then unfreeze the encoder and train both for
   8,000 updates with an encoder learning rate one tenth of the head rate;
3. use the same labeled geometry queries, augmentation, batch order, and total compute;
   and
4. report validation geodesic normalized MAE before and after adaptation plus the
   encoder's out-of-family result.

This LP-then-fine-tune order is motivated by
[Kumar et al.](https://arxiv.org/abs/2202.10054). The check is diagnostic and cannot
make a checkpoint pass standalone frozen certification. If adaptation inverts the top
two frozen rankings by more than 2 percentage points or 10% normalized error, advance
both candidates and record that frozen ranking was non-predictive.

## Experiment stages

Before spending the Stage 1-3 budgets below, run the bounded
[direction-finding pilot sequence](../../../experiments/perception-encoder-r0/preregistration.md). Pilot results order
and prune the candidate queue but do not certify a model or weaken any exit rule here.

### Stage 0: Harness and target validation

No encoder training.

- implement geometry-level splits and dataset hashes;
- verify occupancy, clearance, boundary, connectivity, geodesic, and bottleneck
  targets against hand-checked micro-scenes;
- implement majority, raw conservative-grid, random encoder, PCA, and supervised
  upper references;
- implement control-target, zero-embedding, and shuffled-embedding probe runs;
- lock validation/test query IDs, stratum counts, and aggregate weights;
- implement sparse-mask isolation, hidden-region Jacobian, and mask-only shortcut
  tests;
- lock probe capacities and search spaces; and
- verify every metric on perfect, empty, random, one-voxel-hole, and broken-corridor
  predictions.

Exit: perfect predictions pass every hard gate, known failures trigger the expected
gate, and no geometry ID crosses splits.

### Stage 1: Cheap recipe pilot

Use Tiny, radii through 32, 100,000 unique observations, 10,000 updates, and one seed.
Run R0-R4 and R9 plus the raw-grid and random-weight controls. Use ASHA with a
2,000-update grace period to screen optimizer, mask, and augmentation choices.

Exit: retain at most two configurations per recipe. They must beat the random encoder
on at least three of occupancy, clearance, reachability, and effective rank. Results
do not certify a model.

### Stage 2: Objective selection

Use Tiny, radii through 32, 1 million unique observations, 50,000 updates, and three
encoder seeds. Compare R1-R9 with the Stage 1 optimizer fixed. For additive recipes,
initialize from the same parent checkpoint and count all parent compute.

Exit: an objective is retained only if it improves at least one critical frozen-probe
metric by 2 percentage points or lowers a critical normalized error by 10%, while no
other critical metric regresses more than 2 percentage points. Retain at most three
recipes. Run the geometry-only adaptation ranking check on the top two before the
stage decision; an inversion advances both.

### Stage 3: Field-of-view and architecture selection

Use the best retained recipe, radii through 32, 1 million observations, 100,000
updates, and three seeds. First use the Tiny shared pyramid to isolate field-of-view
construction without a Cartesian sweep:

1. hold four active scales fixed and compare per-level sides `17`, `33`, and `65`;
2. hold the winning side fixed and compare one, two, four, and all scales available
   through radius 32; and
3. keep the smallest side/scale combination within 2 percentage points of the best
   normalized probe score and within 0.02 normalized error on every critical error.

With that field-of-view contract fixed, compare:

- raw conservative grids with the capacity-matched probe and no learned encoder;
- current dense `VoxelEncoder3D`;
- pre-activation dense 3D ResNet;
- tri-planar 2D encoder;
- Tiny shared-backbone voxel pyramid;
- pyramid with per-stage FiLM conditioning;
- pyramid with residual adapters;
- pyramid with independent per-scale weights;
- sparse residual encoder if its runtime dependency is available.

The two-branch dilation/Inception variant is tested only against the winning residual
architecture at matched parameters within 10%. Compare GroupNorm and LayerNorm only
on that winner. If its worst-rotation degradation exceeds 3 percentage points or 0.03
normalized error, add the 24-rotation octahedral-equivariant variant at matched
parameters and report the activation-memory multiplier. Do not include reflections.

Exit: select one primary and one fallback architecture using frozen-probe score,
false-open rate, peak memory, and latency. The primary must improve the mean normalized
probe score by at least 3 percentage points over the current encoder or match it while
reducing peak memory or latency by at least 25%. It must also satisfy the raw-grid
comparison rule; otherwise no learned architecture advances.
Run the geometry-only adaptation ranking check on the top two architectures before
locking the primary/fallback pair; an inversion advances both into radius screening.

### Stage 4: Radius scaling

This stage has two separate studies. Only Stage 4A may support a claim that wider
context improves the representation.

**Stage 4A, matched context ablation:** keep architecture, capacity, optimizer,
objective, unique-observation count, update count, and seed set fixed. Train every
maximum-radius checkpoint at `16, 32, 64, 128, 256, 512` from scratch for 100,000
updates and three seeds. Sample requested radii uniformly from those supported by that
checkpoint and report both observations and encoded valid voxels. No checkpoint loads
weights or optimizer state from a smaller radius.

Exit per radius: pass radius retention, improve at least one wide-context topology or
geodesic metric by 2 percentage points or 10% normalized error, and add no more than
one scale level's declared compute. Stop increasing radius if two consecutive levels
add no probe benefit.

**Stage 4B, optional curriculum efficiency:** warm-start the sequence from the prior
radius and retain 50% of batches from earlier radii. This is explicitly a curriculum
study and reports cumulative observations, valid voxels, updates, wall time, and
accelerator-hours from the first radius. Pilot it with one seed. At radii 128 and 512,
train scratch controls for the same cumulative accelerator-hour budget within 5% and
report their resulting updates, observations, and encoded valid voxels. Promote the
curriculum conclusion to three seeds only if it reaches the same frozen-probe quality
with at least 25% less wall time or compute.
Never compare a cumulative warm-start checkpoint with a 100,000-update scratch model
to claim a context benefit.

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

### Interim experimental publication

Full certification is intentionally expensive, but discovery must still produce
usable artifacts. After Stage 2, a checkpoint may enter the model garden with status
`experimental` when it:

- passes reproducibility, state-integrity, supported-radius execution/resource gates,
  and mask-isolation/shortcut gates when applicable, on validation data;
- beats random weights and the zeroed/shuffled embedding controls on the normalized
  validation aggregate;
- has validation false-open <= 2% and false-closed <= 10% on the dedicated topology
  suites;
- includes complete configuration, corpus, split, limitation, and hardware metadata;
  and
- has never been selected using test data.

An experimental checkpoint is not a default, cannot be described as validated, and
must expose its failed or unrun certification gates. This interim path does not lower
the Stage 7 thresholds.

## Run matrix and cost control

The maximum planned run count before early stopping is:

| Stage | Full runs | Seeds | Maximum encoder trainings |
|---|---:|---:|---:|
| 1 recipe pilot | up to 28 ASHA trials | 1 | 28 partial |
| 2 objective selection | 9 recipes | 3 | 27 |
| 3 field-of-view and architecture selection | up to 17 staged variants | 3 | 48 |
| 4A matched radius context | 6 scratch maxima | 3 | 18 |
| 4B optional curriculum pilot | 6 warm starts + 2 matched scratch controls | 1 | 8 |
| 5 data scaling | 7 budgets | 3 | 21 |
| 6 capacity scaling | 3 families | 3 | 9 |
| 7 certification | 1 locked candidate | 5 | 5 |

Do not execute this as one Cartesian sweep. Complete each exit decision and discard
losers before the next stage. Reuse immutable datasets and cached algorithmic targets,
but never reuse validation/test observations as pretraining input.

Before Stage 1 begins, preregister an accelerator-hour and wall-clock cap for Stages 1
and 2 in addition to their update limits. Stop each stage at the first reached cap;
do not extend it after inspecting rankings. Publish the best eligible checkpoint as
`experimental` when the cap is exhausted, then schedule later stages separately. This
keeps the validation program executable without weakening final certification.

## Required artifacts and metric names

Each run must store resolved configuration, Git commit, dataset/split hashes, encoder
checkpoint, optimizer state, objective histories, collapse diagnostics, frozen-probe
configurations, per-geometry predictions, per-rotation predictions, stratified-
bootstrap samples or reproducible indices, IQM and performance-profile inputs,
evaluation-mixture weights, selectivity/embedding-ablation results, mask-isolation
and Jacobian results, projector/predictor shapes, spectral diagnostics, topology
partitions, geometry-only adaptation rankings, and an environment manifest.

Use stable metric prefixes:

```text
pretext/{objective}/{metric}
representation/rankme_effective_rank
representation/dead_dimension_fraction
representation/largest_pc_share
representation/alpha_req_exponent
representation/alpha_req_fit
representation/lidar_rank
probe/occupancy/{metric}
probe/clearance/{metric}
probe/reachability/{metric}
probe/geodesic/{metric}
probe/topology/{metric}
probe/selectivity/{probe}/{metric}
probe/embedding_ablation/{ablation}/{metric}
pretext/mask_isolation/{metric}
adaptation/geodesic/{metric}
robustness/{corruption}/{metric}
robustness/rotation/{metric}/worst_degradation
statistics/{metric}/iqm
statistics/{metric}/probability_of_improvement/{baseline}
efficiency/{device}/{metric}
```

The certification command must emit `certification.json` containing every gate,
observed value, threshold, confidence interval, pass/fail result, and links to raw
artifacts. A single failed hard gate makes the top-level result `failed`.

## Recommended first execution

Implement Stage 0, including sparse-mask isolation and probe-ablation controls, before
changing the encoder. Then run Stage 1 with R0, R1, R2, R3, R4, and R9. This determines
whether the existing reconstruction objective has an empty-space shortcut, whether
truncated ESDF is a stronger standalone target, and whether sparse masked occupancy
or contextual latent prediction adds useful frozen features. Publish an eligible Tiny
checkpoint as `experimental` at the time-box, but do not train Base or Large until a
Tiny recipe passes Stage 2 promotion rules.
