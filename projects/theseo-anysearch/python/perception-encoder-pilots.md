# Preregistration: Voxel Encoder Direction-Finding Pilots

Status: discovery
Owner: amadou-6e
Last reviewed: 2026-09-02
Tracking issue: [specs#13](https://github.com/amadou-6e/specs/issues/13)
Methodology revision: [specs#15](https://github.com/amadou-6e/specs/issues/15)
Calibration recovery: [specs#19](https://github.com/amadou-6e/specs/issues/19)
Governing validation plan:
[Standalone Voxel Encoder Pretraining](perception-encoder-pretraining.md)
Architecture research:
[Scalable 3D Voxel Perception Encoders](perception-encoders.md)

## Decision boundary

This document is a preregistration: hypotheses, data partitions, budgets, metrics,
decision rules, and validity limits are committed before results are opened. This
separates planned comparisons from later exploratory analysis, following the
[preregistration practice](https://doi.org/10.1073/pnas.1708274114) and the reporting
principles in the
[NeurIPS reproducibility program](https://jmlr.org/papers/v22/20-303.html).

These pilots answer which architecture and pretraining directions deserve the larger
Stage 1-3 budgets. They do not certify an encoder, set final hyperparameters, or use a
policy, reward, planner head, rollout, or RLlib. Pilot results may order or prune the
full experiments, but they cannot weaken a gate in the governing validation plan.

The sequence must produce:

- a primary and fallback pretraining bundle;
- a primary and fallback architecture/field-of-view bundle;
- evidence about whether recipe ranking changes with architecture;
- resource measurements that rule out infeasible candidates early; and
- an explicit `winner`, `tie`, or `no viable direction` outcome.

The final certification validation and test splits remain sealed throughout. All pilot
selection occurs on geometry IDs drawn from the parent training partition.

## Questions

| ID | Question | Decision informed |
|---|---|---|
| Q0 | Are targets, masks, probes, gradients, and encoder outputs trustworthy? | Whether any comparative run may begin. |
| Q1 | Which broad target family creates useful frozen features fastest? | Full reconstruction, masked occupancy, ESDF, or latent teacher prediction. |
| Q2 | Which native training choices materially affect the top target families? | Masking, target sampling, and teacher-update defaults. |
| Q3 | Which architecture families are feasible and learn useful features at Tiny scale? | Dense residual, tri-planar, shared pyramid, or sparse residual direction. |
| Q4 | How much multiscale context is useful before radius scaling? | Per-level side and number of active scales. |
| Q5 | Does the objective ranking survive a change of architecture? | Whether recipe and architecture can be selected mostly independently. |
| Q6 | Is the observed direction stable across fresh seeds and unseen pilot geometries? | Which configurations enter the larger experiment plan. |
| Q7 | Can the winner execute at radius 128 without losing shared-radius quality? | Whether its architecture may be queued as a wide-context direction. |

## Methodology basis

- [Hyperband](https://www.jmlr.org/papers/v18/16-558.html) and
  [ASHA](https://arxiv.org/abs/1810.05934) motivate escalating resources across a
  shrinking candidate set. Their guarantees do not establish that a short-budget
  ranking is the full-budget ranking, so this plan measures that proxy explicitly.
- [Domhan et al.](https://www.ijcai.org/Proceedings/15/Papers/487.pdf) and
  [LC-PFN](https://arxiv.org/abs/2310.20447) motivate probabilistic learning-curve
  extrapolation. Extrapolation is used only when its interval calibration passes on
  completed local curves; it may rescue an uncertain slow starter but never name a
  winner by itself.
- [Accounting for Variance in Machine Learning Benchmarks](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf)
  motivates varying initialization and reporting uncertainty over data and seed
  sources. P1 and P4 therefore use two seeds, and all direction decisions use paired
  geometry-cluster bootstrap intervals.
- [Generalization in Adaptive Data Analysis](https://arxiv.org/abs/1506.02629) shows
  the risk of repeatedly adapting to one holdout. Independent development pools are
  opened at the objective, architecture, and interaction phases. A competition
  [meta-analysis](https://proceedings.neurips.cc/paper_files/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html)
  found limited aggregate overfitting in its setting, so repeated reuse is treated as
  a risk to measure, not proof that this pilot must fail.
- [Deep-learning data-scaling evidence](https://arxiv.org/abs/1712.00409) motivates a
  targeted four-times-data sensitivity check. A low-data ranking is not assumed to
  estimate the representation ceiling.
- [A Metric Learning Reality Check](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123700681.pdf)
  motivates identical evaluation protocols, strong baselines, and component-level
  reporting when comparing representation-learning methods.

## Pilot corpus

Create `voxel-encoder-pilot-v1` only from geometry IDs assigned to the parent training
split. Assign geometry IDs before sampling observations and store the assignment hash.

| Nested split | Geometry IDs | Base observations | Use |
|---|---:|---:|---|
| `pilot_train` | 96 | 24,000 | Encoder and probe training; P4D alone expands this to 96,000 observations from the same IDs. |
| `pilot_dev_early` | 24 | 6,000 | P1-P2 objective and training-mechanics decisions. |
| `pilot_dev_arch` | 24 | 6,000 | Open after P3 for P4-P5 architecture/context decisions. |
| `pilot_dev_interaction` | 24 | 6,000 | Open after P6 pairings are locked. |
| `pilot_confirm` | 32 | 12,000 | Open once for P7 after the top two pairings are locked. |

### Calibration-repair corpus

The first execution of `voxel-encoder-pilot-v1` remains governed by specification
commit `f64ea0b1b30ce07c28dfe2dc688a56d48a931c0d`. Its analytic micro-fixture
normalization anchors are not measured corpus baselines, so its aggregate
`pilot_score` values are diagnostic only. Preserve its raw metrics and reports; do
not recalculate them under replacement anchors. The v1 effective-rank and false-open
vetoes remain valid observations for its trained embeddings because they do not use
the normalization anchors.

The calibration-repair execution is `voxel-encoder-pilot-v2`. Draw every v2 geometry
ID afresh from the parent training partition; no v2 geometry or observation may occur
in an opened v1 pool. Preserve the v1 decision-pool sizes and add two non-decision
pools before any v2 candidate result is opened:

| V2-only split | Geometry IDs | Base observations | Use |
|---|---:|---:|---|
| `pilot_calibration` | 24 | 6,000 | Fit and validate fixed score floors and supervised references only. |
| `pilot_diagnostic` | 24 | 6,000 | Run the frozen T3 implementation-health replay only. |

Both added pools cover all four geometry families and low, medium, and high occupied
fractions. They are geometry-disjoint from `pilot_train`, every decision pool, and
each other. Neither pool may rank candidates, select P1 checkpoints, or contribute
rows to a P1-P8 decision. Freeze the following identities before generating any v2
candidate metric:

- corpus: `voxel-encoder-pilot-v2`;
- dataset snapshot: `voxel-encoder-pilot-v2-dataset-1`;
- preregistration: `voxel-encoder-pilot-v2-preregistration-1`;
- calibration run: `voxel-encoder-pilot-v2-p0-calibration-1`;
- T3 diagnostic run: `voxel-encoder-pilot-v2-t3-diagnostic-1`; and
- replacement P1 run: `voxel-encoder-pilot-v2-p1-1`.

The v2 preregistration must pin the merge commit containing this recovery revision,
the superseded v1 run and specification commit, every pool and query hash, generator
version and seed, reference checkpoint and prediction hashes, numerical anchors, and
separate calibration/diagnostic accelerator-hour caps. P0 calibration and T3
diagnostics do not consume the unchanged 16-trial P1 cap, but their compute is
reported separately. A cap exhaustion or failed shared gate blocks v2 P1 rather than
borrowing comparative budget.

`pilot_train` and every development pool cover open rooms/boxes, thin walls/isolated
obstacles, corridor/topology scenes, and imported geometry. In `pilot_confirm`, 16
geometries come from the same families with new seeds, eight use a held-out procedural
topology template, and eight come from an imported-geometry source absent from encoder
pretraining. Report these three confirmation groups separately; do not tune their
weights after P7 begins. The two eight-geometry out-of-family groups are stress smokes,
not estimates of generalization to their source populations.

Sample radii 8 and 16 equally for P0-P4. Generate radius-32 observations from the same
IDs only when P5 starts and radius-128 observations only after P7 is locked for P8.
Balance boundary, topology, ordinary free-space, open-space, and unknown cases using
the governing sampling shares. Within every nested split, balance low, medium, and
high occupied fractions. No observation may move between nested splits, and no
augmented view may cross a split.

The frozen pilot probe set is smaller than certification:

| Probe | Training examples | Per-dev examples | Confirm examples | Maximum updates |
|---|---:|---:|---:|---:|
| Global linear | 12,000 observations | 3,000 | 6,000 | 2,000 |
| Occupancy/clearance coordinate | 100,000 queries | 20,000 | 40,000 | 5,000 |
| Reachability/geodesic pair | 50,000 balanced pairs | 10,000 | 20,000 | 5,000 |
| Topology decoder | 8,000 observations | 2,000 | 4,000 | 5,000 |

Probe architecture and optimizer are fixed after P0. Every coordinate and pair probe
still runs the control-target, zero-embedding, and shuffled-embedding controls. Pilot
queries and their stratum weights are immutable after their hashes are recorded.

Partition each development pool into three geometry blocks of eight IDs. For each
encoder checkpoint, select probe hyperparameters and checkpoint preference on two
blocks and report on the third, rotating so every geometry has one out-of-fold
prediction. Pool only those out-of-fold predictions for pilot decisions. This removes
same-row checkpoint reporting bias but does not erase adaptive reuse of
`pilot_dev_early` by P1-P2 or `pilot_dev_arch` by P4-P5; that residual risk is declared
below.

## Common comparison contract

Unless a pilot says otherwise:

- use the Tiny capacity family and a 192-dimensional global embedding;
- initialize from scratch; no candidate receives a pretrained parent;
- use seeds 0 and 1 for P1 and the base P4 architecture screen, seed 0 for P2,
  P5, and P6, fresh seeds 2 and 3 for P7, and seed 4 for P8;
- use the same ordered observation batches, augmentation draws, probe examples, and
  checkpoint steps within a paired comparison;
- count encoder updates, observations, encoded valid voxels, accelerator-hours, peak
  memory, and wall time;
- run on one declared reference accelerator, disable compilation, and use BF16 only
  when every candidate supports it reliably; otherwise use FP32 for the comparison;
- compare trainable encoder parameters within 10%; report decoder, projector, and
  predictor parameters separately; and
- evaluate frozen probes at 10%, 25%, 50%, 75%, and 100% of each run's update budget.

Do not stop a valid run merely because its early score is low. Early termination is
allowed only for non-finite values, failed state integrity, failed mask isolation,
greater than 95% dead dimensions at two evaluations, OOM, or exhaustion of the
preregistered stage compute cap.

Whenever a later pilot asks for the top two but only one new candidate survives, use
the non-veto reference control in the second slot: T0 for a training bundle and the
current dense encoder for an architecture. If that control also vetoes, run the later
pilot with one slot and declare that no fallback was established. If no new candidate
survives, return `no viable direction` and stop.

### Pilot score

In P0, lock one floor per metric as the best of the majority/frequency, PCA, and fixed
random-projection baselines. The floor is shared by every recipe and architecture; do
not use an architecture's own random initialization as the normalization floor. For
each metric, normalize the candidate between that fixed floor and the over-capacity
supervised reference. For a higher-is-better metric:

```text
(candidate - fixed_floor) / (supervised_reference - fixed_floor)
```

For a lower-is-better error, use:

```text
(fixed_floor_error - candidate_error) /
    (fixed_floor_error - supervised_reference_error)
```

Do not clip values outside `[0, 1]`. The `pilot_score` is the unweighted mean of
normalized occupied IoU, boundary F1, clearance normalized MAE, reachability AUPRC,
and geodesic normalized MAE. Always report the components and strata; the aggregate
cannot override a veto.
Before using a component, the supervised reference must beat the fixed floor by at
least 0.10 absolute score or reduce its normalized error by at least 20%. The candidate
must still beat its paired random encoder independently; this proves that pretraining,
not only architectural inductive bias, added value. If the ceiling check fails,
the normalization is ill-conditioned: block the comparison and repair the target,
probe, or corpus rather than dropping the component after seeing candidate results.

For `voxel-encoder-pilot-v2`, fit and measure these anchors as follows before opening
`pilot_dev_early`:

1. Derive majority/frequency statistics only from `pilot_train`. Fit PCA only on
   `pilot_train`, and freeze the random-projection distribution and seed. Train each
   baseline's capacity-matched probe with the same target definitions, training-query
   budget, architecture, optimizer, update budget, and cross-fitting code used for a
   candidate probe.
2. Train the deliberately over-capacity supervised references from `pilot_train`.
   Each reference has at least four times the Tiny candidate's parameters and uses
   fixed geometry-disjoint train/selection folds within `pilot_train`. Select its
   checkpoint without reading `pilot_calibration`; record its convergence curve,
   capacity, seed, and residual training and selection error.
3. Evaluate every floor candidate and supervised reference once on the immutable
   `pilot_calibration` queries. For each component, set the floor to the best measured
   majority/frequency, PCA, or fixed-random-projection result and the ceiling to the
   measured supervised-reference result. Store per-geometry values and strata as
   well as the aggregate.
4. Apply the existing denominator check to each measured floor/ceiling pair. A
   higher-is-better ceiling must exceed its floor by at least 0.10 absolute; an error
   ceiling must reduce the floor error by at least 20%. Any failed component blocks
   the entire v2 comparison. Do not drop, replace, or reweight a failed component
   after opening candidate results.
5. Content-address the fitted models, predictions, queries, per-geometry metrics, and
   numerical anchors in `voxel-encoder-pilot-v2-preregistration-1`. Only then may P1
   open the separately hashed `pilot_dev_early` decision pool.

Candidates continue to require improvement over their paired random encoder. The
measured fixed floors normalize scores across architectures; they do not replace the
paired random control or any raw veto.

The following vetoes apply to every comparative pilot:

- state-integrity, numerical-reproducibility, or applicable mask-isolation failure;
- effective-rank fraction below 0.25 or more than 5% near-dead dimensions at the final
  checkpoint;
- control-target selectivity below 0.05 pilot-score units;
- zeroed or shuffled embeddings within 0.05 of the real-embedding pilot score;
- active pilot evaluation-pool false-open rate above 5% or more than 2 percentage
  points worse than the current encoder; or
- unsupported output shapes, invalid masks, OOM, or missing resource accounting.

For every score difference, run a paired stratified cluster bootstrap with 10,000
resamples of complete geometry IDs. Preserve geometry-family and occupancy strata. In
P1 and P4, compute intervals separately per seed and on per-geometry scores averaged
over the two observed seeds. Do not bootstrap two seeds as if they estimated the
initialization population. A direction is decisive only when the pooled paired 95%
geometry interval excludes zero, the absolute mean difference is at least 0.03 pilot-
score units, and both seeds agree where two exist. Otherwise it is a tie. Never use
lower pretext loss to break a frozen-probe tie. Carry tied candidates forward when the
next pilot has capacity; otherwise prefer the lower-memory candidate while recording
the tie.

### Learning-curve extrapolation

Different objectives may have different early learning speed. Fit a probabilistic
learning-curve model to the five frozen-probe checkpoints following
[Domhan et al.](https://www.ijcai.org/Proceedings/15/Papers/487.pdf) or the Bayesian
[LC-PFN](https://arxiv.org/abs/2310.20447). P0 locks one implementation, its priors,
and its target horizon before candidate results exist. Predict no farther than four
times the current pilot budget or the next governing-stage budget, whichever is
smaller.

Before extrapolation affects retention, backtest it by hiding the final two points of
completed local encoder curves. Its nominal 95% posterior interval must cover at least
90% of hidden points and median absolute pilot-score error must be at most 0.05. Store
the calibration sample, coverage, error, posterior draws, and implementation version.
If local curves are insufficient or calibration fails, extrapolation remains a plotted
diagnostic and every observed-score tie advances.

A calibrated extrapolation can rescue a candidate: do not eliminate it when its
predicted 95% upper bound at the target horizon overlaps the leader's predicted 95%
lower bound. It cannot name a winner or eliminate a candidate by itself. When observed
and extrapolated rankings disagree, record `short_horizon_unresolved` and advance both.

## Pilot sequence

### P0: Contract and overfit smoke tests

**Hypothesis:** the harness exposes known failures and every candidate can propagate a
valid learning signal before comparative compute is spent.

Use 32 hand-checkable micro-scenes containing empty/open space, a plane, a one-voxel
wall, a one-voxel hole, a corridor, a branch, a loop, disconnected components, and
unknown boundaries. Run each objective and architecture through 20 forward/backward
batches, then overfit 64 fixed observations for at most 500 updates.

Required outcomes:

- exact geometry targets agree with hand-computed values on every micro-scene;
- perfect, empty, random, broken-wall, and filled-corridor predictions trigger the
  expected metric and topology behavior;
- the fixed per-metric normalization floors and supervised ceilings satisfy the
  pilot-score denominator checks;
- the paired geometry-bootstrap implementation recovers known differences and covers
  zero for identical synthetic candidates;
- the learning-curve implementation, priors, target horizons, and calibration fixture
  are locked; it is marked diagnostic until its local backtest passes;
- encoder state hashes change during encoder training and never during frozen probes;
- each trainable objective reduces its micro-set loss by at least 90% without NaN or
  Inf values;
- sparse/mask-aware recipes pass hidden-value intervention, hidden Jacobian, and
  mask-only shortcut tests; and
- all architectures return their declared outputs with correct validity masks at radii
  8, 16, and 32; every new garden candidate returns the global, scale, and local
  outputs, while the current encoder is checked against its legacy contract.

Exit: all required outcomes pass. P0 selects nothing. A failure blocks only the
affected recipe or architecture unless it invalidates shared targets, probes, or
metrics, in which case all later pilots stop.

#### V2 T3 implementation-health replay

Before replacement P1, run T3 at both P1 learning rates with diagnostic seed 5 for
2,000 updates on v2 `pilot_train` and evaluate only on `pilot_diagnostic`. Use the
unchanged P1 T3 baseline: mask ratio 0.60, EMA decay 0.996, AdamW weight decay 0.05,
5% linear warmup, cosine decay, and global-norm clipping at 1.0. This two-cell replay
is diagnostic, not a recipe comparison; it cannot select a learning rate or weaken a
P1 gate.

At update 0 and every 100 updates, store:

- pretext loss, learning rate, unclipped gradient norm, clipping occurrence, and
  encoder parameter-update norm;
- online-encoder, predictor, and EMA-teacher local/global per-channel standard
  deviation, effective-rank fraction, largest-component fraction, and near-dead
  dimension fraction;
- EMA parameter drift, online/teacher feature cosine similarity, target norm, and
  target variance; and
- at the five ordinary frozen-probe checkpoints, the real, zeroed, shuffled, and
  control-target results on `pilot_diagnostic`.

Interpret the replay using rules frozen in the v2 preregistration. Non-finite values,
unchanged encoder state, or a broken EMA update are implementation failures. Label
`target_collapse` when the teacher target has effective-rank fraction below 0.25 or
more than 5% near-dead dimensions at two consecutive stored checkpoints. Label
`representation_collapse` by the same rule on the online global embedding. Label
`late_optimization_instability` when the update-2,000 loss exceeds the lowest loss at
or after update 1,000 by more than 25% at both learning rates. These labels are
diagnostic classifications, not new comparative vetoes.

Declare `mechanism_health_failure` when the same collapse label occurs at both
learning rates or when `late_optimization_instability` fires. T3 enters replacement
P1 unchanged only if the replay has neither an implementation failure nor a mechanism
health failure. A label at only one learning rate does not select the other rate: both
rates still enter P1 and the label remains a declared validity limit. Any failure
blocks T3 and requires a focused fix with a new diagnostic run identity; it does not
authorize tuning against `pilot_diagnostic` or substituting an unregistered T3
variant. A healthy replay means only that the mechanism executes as specified, not
that latent targets are useful.

### P1: Broad pretraining signal screen

**Hypothesis:** useful target families separate from random features within 2,000 Tiny
updates on a fixed reference encoder.

Use one pre-activation Tiny residual encoder with identical widths and outputs for:

| Bundle | Governing recipe | Direction represented |
|---|---|---|
| T0 | R0 | Full class-balanced occupancy autoencoding. |
| T1 | R1 | Sparse visible-cell masked occupancy at mask ratio 0.60. |
| T2 | R2 | Truncated ESDF with boundary-balanced coordinate sampling. |
| T3 | R9 | Masked contextual EMA-teacher local-feature prediction. |

Run each bundle at peak learning rates `1e-4` and `3e-4`, with AdamW weight decay
`0.05`, 5% linear warmup, cosine decay, and global-norm clipping at 1.0, for 2,000
updates and seeds 0 and 1: 16 trained trials. Use `pilot_dev_early`. Masked and
unmasked paths retain the same residual stage widths, output dimensions, and probe
contracts; report their different executed-voxel counts rather than claiming identical
kernels.

Exit: retain at most two bundles. A bundle must pass all vetoes on both seeds and
improve at least three of the five pilot-score components over random weights. Apply
the paired-bootstrap and learning-curve rescue rules before eliminating it. Carry both
learning rates for each retained bundle into P2; P1 does not lock a bundle-wide
learning rate. When T1/T3 and T0/T2 are tied, retain one masked or latent bundle and
one direct-geometry bundle so a short-horizon tie does not erase a meaningfully
different direction.

### P2: Native training-mechanics screen

**Hypothesis:** a useful native recipe choice remains directionally beneficial across
both plausible P1 learning rates.

For each of the two retained bundles, cross the baseline plus its two applicable
variants below with both P1 learning rates. Train from scratch for 3,000 updates and
seed 0: at most 12 trained trials total. Use `pilot_dev_early`. This small factorial
estimates whether the native recipe choice reverses across the two learning rates;
P2 does not assume the P1 point winner transfers to every variant.

| Bundle | Baseline | Variant 1 | Variant 2 |
|---|---|---|---|
| T0 | class-balanced full-volume occupancy | focal loss, gamma 2 | surface/frontier-only target sampling |
| T1 | mask ratio 0.60 | mask ratio 0.40 | mask ratio 0.75 |
| T2 | ESDF truncation `0.25 * radius` | `0.125 * radius` | `0.50 * radius` |
| T3 | mask 0.60, EMA 0.996 | mask 0.40 | EMA 0.99 |

All variants use proper cube rotations and no other augmentation. Promote a variant
only when its paired-bootstrap interval and mean pass the common decisive-direction
rule at one learning rate and its effect has the same sign at the other, or when its
mean component gain is at least 0.05 at both rates without another component regressing
more than 0.02. Otherwise retain the simpler baseline and carry an unresolved learning-
rate interaction into the full Stage 1 search. The result is a locked target/mechanics
bundle, not a permanently locked optimizer.

### P3: Architecture feasibility screen

**Hypothesis:** profiling can eliminate architectures that violate the output or
resource contract without using training quality as a proxy.

Parameter-match these candidates within 10% where their structure permits:

- current dense `VoxelEncoder3D`;
- Tiny pre-activation dense 3D ResNet;
- Tiny tri-planar 2D encoder;
- Tiny shared-backbone multiscale voxel pyramid; and
- Tiny sparse residual encoder when the dependency is available.

With random weights, run 100 warmup and 500 measured batch-1 inferences at radii 8,
16, and 32. Measure p50/p95 latency, peak allocated memory, checkpoint bytes,
parameters, FLOPs or executed sparse operations, and output/validity shapes. Then run
20 training steps to measure peak training memory and examples/second.

Exit: remove candidates that fail an output contract, OOM at radius 32, or exceed both
the current encoder's peak memory and p95 latency by more than 50% without providing a
new required capability. Retain all other candidates for P4, capped at five. P3 makes
no quality claim.

### P4: Short architecture signal screen

**Hypothesis:** useful architecture families separate under one fixed training bundle
before the full Stage 3 budget.

Train every P3 survivor with the best P2 bundle for 4,000 updates, seeds 0 and 1,
radius 16, and identical pilot batches. Lock the candidate set before opening
`pilot_dev_arch`. Every candidate sees the full radius-16 physical extent. The dense
and residual candidates use a `33^3` input; the pyramid uses side 17 at strides 1, 2,
4, and 8; the tri-planar model uses the three orthogonal `33^2` planes.

Retain the decisive best candidate and every tied candidate that reduces peak memory
or p95 latency by at least 25%. Keep no more than two base families after applying the
bootstrap and learning-curve rescue rules. If the shared pyramid is retained, test
FiLM and residual-adapter conditioning with seed 0. If a dense residual family is
retained, test one matched-parameter two-branch dilation/Inception block with seed 0.
Confirm only the best conditional variant with seed 1 when it would replace a base
family. Do not test independent per-scale weights, norm variants, or equivariance yet.
P4 is capped at ten two-seed base trials plus four conditional/confirmation trials.

Exit: name a provisional primary architecture by quality and a fallback by the Pareto
frontier of quality, memory, and latency. If no learned architecture beats the random
encoder on three pilot-score components, return `no viable direction` and stop.

### P4D: Four-times-data sensitivity

**Hypothesis:** the P4 primary/fallback ordering is not caused only by the 24,000-
observation low-data regime.

After locking the P4 primary and fallback, train each once from scratch with seed 0,
the same 4,000 updates, and 96,000 unique observations sampled from the same 96
`pilot_train` geometry IDs. Preserve strata, batch size, optimizer, and encoded-voxel
accounting. Compare each expanded-data result with its paired 24,000-observation P4
seed-0 run on `pilot_dev_arch`.

Flag `data_sensitive` and retain both architectures when their point ordering reverses,
the paired difference changes by at least 0.05 pilot-score units, or either expanded-
data learning-curve interval makes the earlier elimination inconclusive. P4D is a
ranking sensitivity check, not a fitted scaling law; two data sizes cannot establish
an asymptotic trend. Because both sizes use the same 96 geometry IDs, it tests
observation density rather than geometry-family diversity.

### P5: Field-of-view micro-ablation

**Hypothesis:** the provisional primary benefits from multiscale context without
requiring a large per-level dense volume.

Use the P4 primary and its fixed P2 training bundle for four seed-0 trials of 4,000
updates on `pilot_dev_arch`:

| Trial | Maximum radius | Per-level side | Active strides |
|---|---:|---:|---|
| F0 | 16 | 17 | `1, 2, 4, 8` |
| F1 | 16 | 33 | `1, 2, 4, 8` |
| F2 | 16 | winning side | one stride whose half-width covers radius 16 |
| F3 | 32 | winning side | all strides needed to cover radius 32 |

For a non-pyramid primary, implement equivalent nested inputs or receptive-field
changes without changing parameter count by more than 10%. F2 uses stride 2 when the
winning side is 17 and stride 1 when it is 33, preserving the radius-16 physical extent
with one level. It tests whether a fine-to-coarse hierarchy adds value beyond a single
resolution; report the expected loss of fine detail separately.

Exit: among candidates tied with the best radius-16 result under the common bootstrap
rule, choose the smallest side and fewest scales with no component regression above
0.02. Radius 32 advances only if the paired 95% geometry interval for reachability or
geodesic improvement excludes zero, its mean gain is at least 0.03, no veto fires, and
it adds no more than one declared scale level. Otherwise keep radius 16 for the next
pilot and leave wider context to the full radius study.

### P6: Objective-by-architecture interaction check

**Hypothesis:** the selected recipe and architecture directions are not artifacts of
being evaluated with only one counterpart.

Cross the top two P2 training bundles with the P4 primary and fallback architecture/
field-of-view bundles. Lock all four pairings before opening `pilot_dev_interaction`.
Train them from scratch for 8,000 updates with seed 0. Use the same batches and cap each
pairing at the smaller of the fixed update budget or the preregistered accelerator-hour
budget.

Report recipe effects within each architecture, architecture effects within each
recipe, and the paired-bootstrap distribution of the difference-in-differences. With
one encoder seed this is an exploratory interaction screen, not a precise estimate.
Flag a possible material interaction when either condition holds:

- the preferred recipe reverses by at least 0.03 pilot-score units; or
- the mean architecture effect changes by at least 0.05 between recipes, or its 95%
  interval includes changes of that magnitude in either direction.

Exit: without a possible material interaction, retain the decisive best pairing and
the most efficient tied pairing. With a possible interaction, retain the best pairing
from each architecture and prohibit independent recipe/architecture conclusions in
later reports. Only the later multi-seed experiments may turn the flag into a claim.

### P7: Fresh-seed confirmation

**Hypothesis:** the two retained pairings preserve their direction on fresh seeds and
previously unopened pilot geometries.

Lock all choices, then train both pairings from scratch for 10,000 updates with seeds 2
and 3: four trained trials. Open `pilot_confirm` only after the run manifests and
checkpoint-selection rule are committed. Report mean and per-seed metrics for the
ordinary, held-out-topology, and held-out-imported groups. Two seeds are not enough for
a significance claim; they are a guard against a single lucky exploratory seed. The
eight-geometry topology and imported results are stress smokes and may expose a
failure, but they cannot support a population-level generalization claim.

Declare `winner` only when one pairing:

- passes every pilot veto on both seeds;
- leads by at least 0.03 mean pilot-score units;
- has a paired geometry-cluster-bootstrap 95% interval excluding zero on the ordinary
  confirmation group;
- has the same score direction on both seeds; and
- has no component regression greater than 0.02.

Otherwise declare `tie` and carry both pairings into the existing Stage 1/2 program.
Declare `no viable direction` if neither pairing passes the vetoes. Never reopen P1-P6
or tune a configuration after reading `pilot_confirm`.

### P8: Wide-context viability smoke

**Hypothesis:** the P7 winner can execute and retain useful features at a radius large
enough to exercise the multiscale design before it is queued as the wide-context
direction.

After P7 is immutable, train the winner from scratch twice with seed 4, 10,000 updates,
and the expanded 96,000-observation corpus: one checkpoint with maximum radius 32 and
one with maximum radius 128. Use the same observation positions, optimizer, and update
budget. Both mixtures allocate 25% each to radii 8, 16, and 32; the remaining 25% is
radius 32 for the control and radius 128 for the wide model. Count cumulative
observations, valid voxels, wall time, and accelerator-hours. Evaluate both on matching
radius-32 queries and on the same preregistered wide-context reachability, geodesic,
loop, and dead-end labels from `pilot_confirm`; the control receives only its declared
radius-32 observation.

Exit: radius 128 must execute without OOM or a dense per-level volume above the
declared side, pass state/mask vetoes, and regress no shared-radius component by more
than 0.05. Report whether any wide-context component improves by at least 0.03, but do
not require improvement from this one-seed smoke. Failure prevents describing the P7
architecture as the queued wide-context direction: retain its training bundle, mark
architecture scaling unresolved, and reopen the relevant full Stage 3/4 comparison.

## Validity limits

The pilot outcome is directional evidence under these known limits:

- **Short horizons:** 2,000-10,000 updates can favor fast-starting objectives and may
  miss a delayed representation gain. Calibrated curve intervals rescue uncertain
  candidates; only the full Stage 2 budget resolves their ceiling.
- **Small base corpus:** 24,000 observations can rank optimization speed more than data
  efficiency. P4D detects one observation-density reversal at 96,000 observations but
  holds geometry count fixed, does not fit a scaling law, and does not substitute for
  the full data-diversity study.
- **Limited context:** P1-P4 see radii no larger than 16 and P5/P6 no larger than 32.
  P8 establishes radius-128 viability for one winner, not architecture superiority at
  128 or transfer to radius 512.
- **Incomplete seed variance:** P2, P5, P6, and P8 use one encoder seed. Geometry
  bootstrap intervals condition on that seed and cannot estimate initialization
  variance. Their numerical thresholds are retention heuristics, not significance
  claims.
- **Adaptive development reuse:** P1-P2 share `pilot_dev_early` and P4-P5 share
  `pilot_dev_arch`. Cross-fitted scores reduce checkpoint bias but cannot make adaptive
  reuse independent. Fresh pools at P4, P6, and P7 test for major ranking failures.
- **Small out-of-family groups:** eight held-out topology and eight imported geometries
  can veto an obvious failure only. Generalization claims require the full stratified
  certification corpus.
- **Proxy task:** frozen probes and the small geometry-only adaptation check measure
  accessible geometry, not eventual policy or planner value. Pilot ordering may still
  invert in the governing experiments.

Every decision record lists which limits could plausibly invert that decision. Reports
must say `pilot direction`, never `best architecture`, `scales to 512`, or `validated`.

## Budget and stop rules

| Pilot | Maximum trained trials | Updates per trial | Maximum updates |
|---|---:|---:|---:|
| P0 | diagnostic only | 500 | not comparative |
| P0C (v2 calibration) | fixed controls/references | preregistered convergence cap | not comparative |
| P0D (v2 T3 replay) | 2 | 2,000 | 4,000 diagnostic |
| P1 | 16 | 2,000 | 32,000 |
| P2 | 12 | 3,000 | 36,000 |
| P3 | profiling only | 20 steps | not comparative |
| P4 | 14 | 4,000 | 56,000 |
| P4D | 2 | 4,000 | 8,000 |
| P5 | 4 | 4,000 | 16,000 |
| P6 | 4 | 8,000 | 32,000 |
| P7 | 4 | 10,000 | 40,000 |
| P8 | 2 | 10,000 | 20,000 |
| **Total** | **58 comparative trainings** | | **240,000** |

Before P1, record a per-pilot and total accelerator-hour cap. The total program stops
at the first of 240,000 comparative encoder updates or that accelerator-hour cap.
P0/P0C/P0D/P3 diagnostic work is reported separately so calibration, diagnosis, and
profiling cannot silently consume the training budget. A pilot may spend unused trials
from its own cap only; budget cannot be moved into a later pilot after results are
visible.

The 240,000-update cap is 17.8% of the 1.35 million maximum encoder updates in the
governing Stage 2 matrix. This ratio is descriptive, not a claim of equal compute:
executed valid voxels and accelerator-hours remain the primary accounting.

## Decision record

Commit one `pilot-decision.json` after every pilot with:

```json
{
  "pilot": "P4",
  "dataset_hash": "...",
  "query_hash": "...",
  "code_commit": "...",
  "development_pool": "pilot_dev_arch",
  "locked_inputs": {},
  "candidates": [],
  "vetoes": {},
  "pilot_scores": {},
  "bootstrap": {"resamples": 10000, "paired_geometry_ids": true},
  "learning_curve": {"implementation": "...", "calibrated": false},
  "resource_metrics": {},
  "validity_flags": [],
  "decision": "winner | tie | no_viable_direction | blocked",
  "retained": [],
  "rejected": [],
  "reason": "...",
  "next_pilot": "P5"
}
```

Every rejection names the preregistered rule that fired. Store resolved configs,
checkpoints, per-geometry out-of-fold predictions, probe ablations, metric components,
bootstrap indices, learning-curve observations/posteriors/calibration, resource traces,
and failed-run logs. Failed/OOM trials count against the trial cap.

## Handoff to the full experiment plan

After it passes P8, the pilot winner becomes the first queued wide-context direction in
Stage 1, not a certified model. Before P8 passes, only its training bundle may be
prioritized; its architecture remains a small-context result. The fallback remains
queued until Stage 2 establishes a multi-seed result. R0, the random encoder, the raw-
grid control, and the current encoder remain mandatory even if they lose in the pilots.

P0 evidence may satisfy a governing Stage 0 item only when it used the identical
implementation, fixtures, tolerances, and artifact contract. The remaining Stage 0
checks still run before full Stage 1; a successful pilot is not a blanket Stage 0 pass.

If P7 returns a tie, Stage 1/2 must retain both pairings and spend its additional data,
updates, and seeds on resolving the tie. If P7 finds a material recipe/architecture
interaction, Stage 2 compares complete pairings rather than swapping independently
selected parts. Architecture normalization, equivariance, independent scale weights,
Base/Large capacity, radii above 32, and final certification remain in the governing
later stages.
