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

Concrete v2r2 R0 registration:
[R0 execution protocol](perception-encoder-r0-execution.md).

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

#### Calibration amendment after the blocked v2 run

The first `voxel-encoder-pilot-v2` calibration run remains immutable under
specification commit `01eefc529016da48c4a1dd17b85391720542af14`. It returned
`blocked` and recorded report-payload SHA-256
`a7a149f9235b38f9ff1f1a230ce791367cf528fc6705e0f987674f1a48d4ea43`.
Three gates failed: PCA and fixed-random local projections exposed the queried input
channel and reached occupied IoU `1.0`; the reachability sampling/threshold contract
gave PCA AUPRC `0.934` while its absolute false-open veto was `0.05`; and frequency
prediction reached geodesic NMAE `0.0225`, leaving no useful small-radius denominator.
The supervised reference also collapsed to effective-rank fraction `0.011`. These are
probe and reference failures, not evidence against an encoder objective.

The amended program is `voxel-encoder-pilot-v2r1`. Freeze these new identities:

- dataset: `voxel-encoder-pilot-v2r1-dataset-1`;
- preregistration: `voxel-encoder-pilot-v2r1-preregistration-1`;
- calibration: `voxel-encoder-pilot-v2r1-p0c-1`;
- four-times-data sensitivity: `voxel-encoder-pilot-v2r1-p0d-1`; and
- replacement P1: `voxel-encoder-pilot-v2r1-p1-1`.

The amended calibration pool must contain 24 new parent-training geometry IDs that
are disjoint from every opened v1 and v2 pool. It covers all geometry-family and
occupancy strata. Revised query identities, masks, pair provenance, threshold folds,
and model-free ceiling inputs are content-addressed before the amended pool is opened.
The training and `pilot_dev_early` pools used by replacement P1 are also fresh and
disjoint from opened v1/v2 geometry because candidate selection has already occurred
under those earlier identities. No v2r1 result may be recomputed on v2 geometry.

The v1 P1 `no_viable_direction` verdict is formally superseded by
`voxel-encoder-pilot-v2r1-p1-1`. Preserve all v1 values and its raw collapse
observations, but do not treat its decision as active: the decision contract combined
those observations with a false-open veto later shown to be structurally unpassable
and with miscalibrated aggregate scores. Store a machine-readable supersede record
that cites the v2 P0C report-payload hash and names `false_open_rate_max` as the
invalidating fired veto.

For v2r1, apply the following probe and scoring overrides:

1. **Held-out occupancy:** select balanced known occupied/free query cells, change
   those cells to unknown before encoder execution, and predict their original labels.
   The default remains on-grid; off-grid and cross-channel variants are diagnostic
   flags and cannot replace the default after calibration opens. Assert that no query
   label remains in the encoder input.
2. **Reachability:** sample positives across fixed geodesic-distance bins, component
   negatives with the registered separation margin, and connectivity-flipping
   boundary perturbations. Calibrate the operating threshold on a geometry-disjoint
   selection fold, report overall and per-bin AUPRC plus false-open/false-closed rates,
   and require two-way agreement. Set the false-open veto before candidate results to
   the best calibrated non-neural baseline rate minus the registered `0.02` margin;
   do not restore an absolute threshold.
3. **Geodesic:** defer `geodesic_nmae` to Stage 2 wide-context evaluation. The v2
   frequency NMAE is below the registered `0.15` pilot noise floor and the supervised
   reference did not reduce it. Record the metric and deferral reason in reports, but
   exclude it from P0C/P0D/P1 gates and ordering.
4. **Ceilings:** use leave-one-out k-nearest-neighbour Bayes proxies for occupied IoU,
   boundary F1, and reachability AUPRC, and kNN-residual error for clearance NMAE.
   These estimates are model-free and collapse-free by construction. Do not train a
   supervised reference. If a future amendment restores one, its selected embedding
   must have effective-rank fraction greater than `0.30`.
5. **Triviality:** for every active component report pointwise V-information and
   online-MDL under its contextual input and registered null input. An active component
   requires contextual-minus-null PVI of at least `0.05` bits per example. Failure
   blocks the run; it does not authorize post-hoc metric removal.
6. **Aggregation:** retire the unweighted `pilot_score` for v2r1. Report raw mean,
   raw IQM, normalized IQM, and the performance profile at thresholds
   `[-0.5, 0, 0.25, 0.5, 0.75, 1.0]` for every active component. A component remains
   active only when its higher-is-better ceiling exceeds its floor by `0.10`, or its
   error ceiling reduces floor error by `20%`. Retain at most two nondominated
   candidates on the per-metric IQMs; if more than two are nondominated, prefer the
   highest worst-component IQM and then the lexical frozen candidate ID. A composite
   score cannot override or conceal any component gate.

`boundary_f1` and `clearance_nmae` keep their v2 target definitions and probe
templates. Their calibration bars remain, respectively, at least `0.10` absolute
headroom and at least `20%` error reduction. The model-free ceilings and fresh v2r1
queries are nevertheless remeasured; the v2 numerical values are evidence, not copied
anchors.

After amended P0C passes, run P0D with four times the observation density from the
same v2r1 training geometry IDs, identical active metrics, fixed query identities,
and matched probe budgets. P0D passes when every active denominator remains valid,
the empirically calibrated false-open veto changes by no more than `0.02` absolute,
and no active metric reverses floor/ceiling ordering. Report geometry-clustered
uncertainty. P0D does not select a recipe and cannot tune the amended probes.

Replacement P1 retains T0-T3, learning rates `1e-4` and `3e-4`, seeds 0 and 1,
2,000 updates, FP32, and the original optimizer schedule. It uses the v2r1 probes,
empirical false-open veto, per-metric gates, and Pareto retention above. Precompute
immutable geometry targets and pipeline CPU batch preparation when those operations
preserve the ordered observations, effective batch size, and exact numerical targets;
record throughput and cache identities with the run.

#### Termination after the blocked v2r1 run

State diagram and review evidence: [perception-encoder-state-review.md](perception-encoder-state-review.md).

The amended `voxel-encoder-pilot-v2r1` calibration is terminal. Its P0C returned
`blocked` (report-payload SHA-256
`2564db175a1880cf81da40bd5a32e472f9b3db81bce111283fe48c74d409697b`) on the single
active gate `reachability_auprc`: even with the redesigned pair sampler and the
model-free k-nearest-neighbour ceiling, the revised anchor could not clear a
`0.10` higher-is-better denominator. The selected floor was coordinates-only
AUPRC `0.9309221452`, and the kNN reference was `0.9971262631`: a gap of
approximately `0.066204`. This shows inadequate headroom on the sampled task, not that
raw occupancy makes connectivity linearly decodable. R0 must test coordinate
and pair-sampling shortcuts before attributing this result to observability.
P0D returned `blocked`
(`4af619e2e3c2256c0e8f6655f65534580fbcabc4178257a4b100348699461775`) with no
retained bundle, and replacement P1 was recorded `not_started`
(`f499d7ede0049ab568297bc3aa6ad810d0400071214648ef940b05781bcdb542`) with zero
trials, updates, and accelerator-hours. That line does not reopen; no
configuration change revives it.

#### Frozen v2r2 topology rule

> At least one topology component must be active and pass its denominator,
> identifiability, triviality, and control-ladder gates. If both reachability
> and geodesic are deferred or invalid, v2r2 terminates with
> `no_topology_identifiable`. The direction-finding pilot does not begin. A
> separately preregistered local-geometry study may be proposed, but is outside
> this pilot's decision chain.

Reachability and geodesic performance are essential to the claim that the encoder
supports pathfinding and benefits from wider context. Continuing P1-P8 on
`occupied_iou`, `boundary_f1`, and `clearance_nmae` alone would silently measure
local-geometry reconstruction while preserving an unjustified topology-perception
claim. `geodesic_nmae` is already deferred (v2r1 override 3), so v2r2 begins only
if it establishes an identifiable, calibratable connectivity gate.

The v2r2 topology gate is the neutral component **`reachability`**: a gate family
whose one frozen primary metric is chosen by R4 (either the normalized
conditional log-loss gain or occlusion-stratified AUPRC). The **selected** R4
metric drives the `reachability` gate; the unselected alternative, pointwise
V-information, selectivity, and the R3 structural scores are diagnostics of the
family. Reports and `active_gate_components` name `reachability`, not a specific
metric, so the gate identity does not contradict the chosen metric.

Enforcement is structural: the comparative P1-P8 preregistration cannot be frozen
unless `active_gate_components` contains a topology-family component - one whose
name begins with `reachability` or `geodesic` (`contracts.TOPOLOGY_COMPONENT_FAMILIES`,
`_require_active_topology_component`). Because P1-P8 can only begin from a frozen
preregistration, a run that defers both topology families stops at P0C with
`decision: no_topology_identifiable` and writes no preregistration.

#### Successor study: `voxel-encoder-pilot-v2r2`

v2r2 is a partially-observed-topology study, not a metric adjustment on v2r1.
The terminal `voxel-encoder-pilot-v2r1` runs are governed by specification commit
`0c9e3c633799f5d42b7a603e0845cac0bd494cda`; v2r2 records that as its predecessor
commit. Draw every v2r2 geometry ID afresh from the parent training partition; no
v2r2 geometry or observation may occur in an opened v1, v2, or v2r1 pool. Freeze
these identities before generating any v2r2 candidate metric:

- dataset: `voxel-encoder-pilot-v2r2-dataset-1`;
- audit protocol: `voxel-encoder-pilot-v2r2-audit-protocol-1`;
- comparative preregistration: `voxel-encoder-pilot-v2r2-preregistration-1`;
- identifiability audit run: `voxel-encoder-pilot-v2r2-r0-1`;
- calibration: `voxel-encoder-pilot-v2r2-p0c-1`;
- four-times-data sensitivity: `voxel-encoder-pilot-v2r2-p0d-1`; and
- replacement P1: `voxel-encoder-pilot-v2r2-p1-1`.

**Two immutable contracts.** R0 runs before R1-R4 and P0C informs the R4 metric
choice, so a single preregistration cannot pin both the R0 report and the chosen
metric. Freeze two:

1. **Audit and calibration protocol** (`voxel-encoder-pilot-v2r2-audit-protocol-1`),
   frozen before R0. It pins: the `theseo-anysearch` integration commit
   `f03509f926d217cf8a0c8c34cd0da38020a5034c` - the squash of PR #342 on
   `exp/perception-encoder`, which carries the `Decision.no_topology_identifiable`
   literal, `contracts.TOPOLOGY_COMPONENT_FAMILIES`, and
   `_require_active_topology_component` (the v2r2 audit/comparative contracts in
   #340 call it; the completed v1/v2/v2r1 contracts are not amended); the
   predecessor v2r1 specification commit
   `0c9e3c633799f5d42b7a603e0845cac0bd494cda`; the audit pool and every
   pool/query hash; generator version and seed; the R2 control ladder identities
   and their capacities; the model-free ceiling inputs; the menu of admissible
   R4 primary-metric forms and a deterministic selection rule; and separate
   R0/P0C/P0D accelerator-hour caps. It also pins the actual implementation SHA
   executing the audit; the foundation SHA above is not a substitute for it.
2. **Comparative P1-P8 preregistration**
   (`voxel-encoder-pilot-v2r2-preregistration-1`), frozen after R0 and P0C and
   before any candidate result. It pins: the R0 audit report payload hash; the
   single chosen R4 primary metric and its aggregation; the calibrated
   per-component denominators and floor sources; the R3 false-merge veto
   threshold; and `active_gate_components`.

`boundary_f1`, `clearance_nmae`, and `occupied_iou` keep their v2r1 target
definitions and probe templates and are remeasured on fresh v2r2 queries; the
v2r1 numerical values are evidence, not copied anchors.

**R0 - identifiability audit (gates everything).** Before R1-R4, on a
geometry-disjoint audit pool, generate controlled counterfactual pairs that hold
the visible voxels fixed and vary the hidden completion, then estimate the
conditional uncertainty of the completed-reachability label given the visible
input. Report:

- unknown-channel prevalence and per-stratum class balance;
- the conditional label entropy `H(reachable | visible input)` per occlusion-span
  stratum. If, for any stratum R4 requires, the hidden geometry is effectively
  random given the visible input under the frozen entropy and uncertainty rule,
  the `reachability` gate defers for insufficient usable signal. A visible-context predictor that *beats*
  the geometric prior is the wanted signal - learnable completion - not a
  failure;
- a **leakage** check with two parts. First, an ablation: a predictor given only
  forbidden generator identity or configuration features (seed, template index,
  band placement rule) that a deployed encoder would not see must not exceed the
  geometric-prior baseline by more than the registered margin. Second, transfer:
  the visible-context completion predictor trained on one generator configuration
  must retain its skill on a held-out generator configuration; an excessive drop
  fails the transfer requirement. Both must pass for a `feasible` finding.

R0 emits a machine-readable `feasible` or `defer` decision from audit data only;
`defer` triggers the frozen topology rule.

Before R0 data are opened, the audit contract must resolve numeric values for
geometry and counterfactual counts per stratum, class support, entropy bounds,
predictor skill margins, transfer-drop tolerances, and uncertainty coverage.
It must define the geometric-prior predictor, coordinate-only control, forbidden
features, generator folds, training budgets, and entropy estimator. All completions
sharing a visible observation stay in the same geometry group. Empty strata,
insufficient support, or intervals crossing a decision boundary produce `defer`
with a reason such as `insufficient_evidence`; this is not proof of impossibility.
Missing values prevent protocol freeze, rather than receiving runtime defaults.
Only the audit contract freezes before R0; the comparative contract is conditional
on the subsequent measured gates. R0 deferral preserves the audit record and does
not require running P0C to emit the terminal decision.

The forbidden-feature control measures generator predictability, not by itself
leakage into the encoder. Record whether those features actually reach encoder
inputs; report held-out-generator failure as a transfer failure rather than proof
of leakage. Both may still fail the preregistered robustness requirements.

**R1 - occlusion-aware sampler.** Reachability labels come from the completed
geometry. Occlusion-span strata `1-2`, `3-5`, and `6+` and their aggregation
weights are frozen before any candidate result; the weights are balanced or
task-motivated and are never set to observed stratum prevalence. Selecting the
best-performing stratum after results (`max`-over-strata) is prohibited.
For reachable pairs, span counts unknown cells on one shortest six-connected
path, including endpoints, with lexicographic (D, H, W) next-cell tie-breaking.
It never counts the union of shortest paths. Unreachable pairs have no such path:
freeze their bin-assignment rule separately before sampling; do not duplicate
every negative into every stratum. Record the support and prevalence of each bin.

**R2 - control ladder.** Freeze the candidate probe capacity, optimization
budget, and checkpoint-selection procedure before building any control. Compare
against three distinct controls: an identical probe over raw input; a
capacity-matched nonlinear raw-input model; and an over-capacity or model-free
reference ceiling. The gated `reachability` denominator is
`reference - nonlinear_raw`, never `reference - linear_raw`; a weak linear
raw-grid probe is not a general raw-input floor because connectivity is
nonlinear.

Every empirical reference uses geometry-disjoint fitting and evaluation, including
preprocessing. Row-wise leave-one-out neighbours from the same geometry cannot
establish the reference used by a v2r2 gate. Counterfactual siblings share folds.
Report kNN results as empirical references, not certified Bayes bounds. The
gating reference and nonlinear-raw control receive the same visible information;
completed geometry, component labels, and target-derived features are permitted
only in separately named oracle diagnostics. Otherwise the denominator would
measure privileged information rather than learnable representation quality.

**R3 - structural evaluation.** Evaluate connectivity with dense reachability
fields from `K` preregistered anchor cells per observation (fixed selection rule;
target is reachable-from-anchor-`k`), scored with Variation of Information,
Adapted Rand index, and Betti-0 error, plus explicit false-merge and false-split
rates. While the `reachability` gate is active, the false-merge rate is a veto
(a false merge is a false-open); its threshold is calibrated from the R2 control
and reference behaviour, not an absolute value. Per-cell component identifiers
are not used as targets.

**R4 - one primary metric, chosen from calibration only.** Before P1 opens,
freeze exactly one primary metric and aggregation for the `reachability` family.
The preferred form is the normalized conditional log-loss gain against the R2
nonlinear-raw floor:

```text
(nonlinear_raw_log_loss - candidate_log_loss) /
(nonlinear_raw_log_loss - reference_log_loss)
```

structurally uniform with the other revised anchors and not clipped (the pilot
never clips normalized scores). Occlusion-stratified AUPRC with the R1 frozen
weighted aggregate, normalized between the R2 nonlinear-raw floor and the
reference ceiling, is the alternative. Exactly one of the two is selected in the
comparative preregistration and becomes the `reachability` gate; the unselected
form, the null-input log loss, pointwise V-information, and selectivity are then
diagnostics only. The `reachability` gate is active only when R0 returned
`feasible`, the selected R4 metric's denominator clears `0.10` headroom between
the R2 nonlinear-raw floor and the reference ceiling, and its triviality gate
passes.

For log loss, use mean binary cross-entropy in bits per query (log base 2),
with probabilities clipped to `[1e-6, 1 - 1e-6]` before taking logarithms.
The headroom is `nonlinear_raw_log_loss - reference_log_loss >= 0.10` bits;
for AUPRC it is `reference_auprc - nonlinear_raw_auprc >= 0.10` absolute.
Normalized scores remain unclipped. Compute both losses on identical queries
and aggregate using the frozen stratum weights. Freeze the primary-metric
selection rule before P0C; do not select a diagnostic merely because it passes.

For v2r2, this amendment supersedes the inherited absolute 5% false-open veto
and the v1 aggregate-score-unit selectivity and embedding-necessity vetoes.
The calibrated R3 false-merge veto is the topology error veto. Its formula,
threshold-selection folds, minimum support, and uncertainty rule must be in the
audit contract before calibration. Component-wise selectivity and embedding
necessity thresholds and the active-component retention rule must also be
explicitly frozen; a v1 five-component rule must not be silently reused.
State integrity, numerical checks, collapse, masks, and resource vetoes remain.
P0D rechecks all active denominators and the calibrated topology veto using its
frozen sensitivity tolerances before P1 may start.

**R5 - fresh run.** New v2r2 dataset, query, audit-protocol, preregistration, and
run identities; no reuse of any v1, v2, or v2r1 identity; new specification
commit. Run R0, then the frozen CUDA P0C, P0D, and P1 chain. If R0 or the R2
ladder shows the preregistered `reachability` denominator stays below `0.10`
headroom, defer the `reachability` gate; do not adopt whichever diagnostic
happened to pass.

#### Local-geometry carve-out

A narrower study may proceed only as its own program, never as part of this
decision chain. It uses a new corpus `voxel-encoder-local-geometry-v1` with its
own dataset, queries, preregistration, runs, score, and reports. Its claims are
limited to occupancy, boundary, clearance, and clearance recovery. It makes no
claim about connectivity or pathfinding, topology perception, wide-context value,
or architecture selection for planning. Its results cannot advance the
direction-finding P1-P8 sequence chain. A later topology-capable study must
independently qualify before its conclusions may be combined with local-geometry
results.

The separately registered [LG1 local-feature study](perception-encoder-local-geometry.md)
implements this carve-out under the user's recorded independent-execution exception.
Its outcomes do not alter this pilot's topology stop rule or advance P1-P8.

The following vetoes apply to every comparative pilot:

- state-integrity, numerical-reproducibility, or applicable mask-isolation failure;
- effective-rank fraction below 0.25 or more than 5% near-dead dimensions at the final
  checkpoint;
- control-target selectivity below 0.05 pilot-score units;
- zeroed or shuffled embeddings within 0.05 of the real-embedding pilot score;
- active pilot evaluation-pool false-open rate above 5% or more than 2 percentage
  points worse than the current encoder; or
- unsupported output shapes, invalid masks, OOM, or missing resource accounting.

For v2r1 only, replace the two `pilot_score`-unit vetoes with their corresponding
per-metric PVI/MDL, embedding-necessity, and revised-anchor checks, and replace the
absolute false-open veto with the empirical reachability veto above.

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
- **Topology identifiability:** v2r2 begins only if its R0 audit finds an identifiable,
  non-leaky, calibratable `reachability` gate. If R0 or the R2 control ladder cannot
  establish a `0.10` denominator between the nonlinear raw-input floor and the
  reference ceiling, both topology families are deferred and the pilot terminates
  `no_topology_identifiable`. A local-geometry study is then a separate program with
  no topology, wide-context, or planning-architecture claims.

Every decision record lists which limits could plausibly invert that decision. Reports
must say `pilot direction`, never `best architecture`, `scales to 512`, or `validated`.

## Budget and stop rules

| Pilot | Maximum trained trials | Updates per trial | Maximum updates |
|---|---:|---:|---:|
| P0 | diagnostic only | 500 | not comparative |
| P0C (v2 calibration) | fixed controls/references | preregistered convergence cap | not comparative |
| P0D (v2 T3 replay) | 2 | 2,000 | 4,000 diagnostic |
| P0C (v2r1 amended calibration) | fixed controls/model-free ceilings | fixed query budget | not comparative |
| P0D (v2r1 four-times-data sensitivity) | fixed controls/model-free ceilings | matched P0C query budget | not comparative |
| R0 (v2r2 identifiability audit) | counterfactual audit pool | preregistered audit cap | not comparative |
| P0C (v2r2 amended calibration) | fixed controls/model-free ceilings + R2 ladder | fixed query budget | not comparative |
| P0D (v2r2 four-times-data sensitivity) | fixed controls/model-free ceilings | matched P0C query budget | not comparative |
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
