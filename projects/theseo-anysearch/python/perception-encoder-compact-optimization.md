# Small-field compact encoder optimization campaign

Status: proposed execution plan; not a frozen run preregistration
Owner: amadou-6e
Last reviewed: 2026-09-11
Tracking issue: [specs#54](https://github.com/amadou-6e/specs/issues/54)
Related: [Model Garden](model-garden.md),
[Standalone Pretraining](perception-encoder-pretraining.md),
[Direction-Finding Pilots](perception-encoder-pilots.md)

## Objective and scope

Deliver a frozen encoder mapping one 33 x 33 x 33 voxel observation to one compact
vector, with independently trained small heads demonstrating retained geometry.
Compare 64, 128 and 192 dimensions; none is assumed sufficient. A dimension may
be extended only through an explicit follow-up protocol, not mid-search.

Existing pilots trained spatial features, not the unused global projection. Their
results provide an initialization and spatial reference, not evidence of a useful
compact vector. Context and tiling evidence is recorded in implementation reports
at commits 081f007 (#374) and d710794 (#376). Preserve their original conclusions.
Pause the #378 halo/scaling direction in favor of this small-field campaign; this
document records direction, not that the remote issue has already been updated.

Primary queries lie in central17 cubed, with eight voxels of context per side.
Evaluate the remaining input region separately before claiming whole-field
usability. A central-query success must be labeled as such, even though the vector
is computed from the whole observation. No RLlib, policy, navigation, topology,
larger-radius or general model-garden certification claim follows automatically.

## Work packages and dependencies

| ID | Scope and owned deliverable | Depends on | Acceptance |
| --- | --- | --- | --- |
| C0 | Interface, claims, split and evaluation contracts | None | Shapes, masks, eligibility, metrics and unresolved decisions explicit |
| C1 | Dataset manifests, target cache and controls | C0 | Group isolation, reproducible labels, mask isolation and control fixtures pass |
| C2 | Compact aggregation and training/probe harness | C0 | No vector bypass; fresh probes; serialization and gradient tests pass |
| C3 | Throughput and numerical profiling | C1, C2 | Cost model, batch/precision choice and measured bottlenecks recorded |
| C4 | Calibration and frozen search preregistration | C1-C3 | Numeric floors, ranking rule, budgets and all run identities frozen |
| C5 | Structural screen and hyperparameter search | C4 | Complete trial ledger, pruning reasons and protected long runs |
| C6 | Multi-seed confirmation and locked assessment | C5 | Winner fixed before test access; per-task uncertainty and limits reported |
| C7 | Frozen model package and review | C6 | Reproducible API, artifacts, metadata and disposition; no automatic promotion |

C1 and C2 can proceed independently after C0 with separate module ownership.
Profiling, search and assessment are dependent stages, not concurrent agent tasks.
Each implementation package needs an issue and exp/<issue> branch. Target
exp/perception-encoder; no integration merges without review. Unmerged dependency
execution must record the user's stacking authorization and exact dependency SHAs.

## Interface and data contract

- Input distinguishes occupied, free, unknown and invalid cells, with voxel spacing
  and coordinate convention explicitly recorded. Unknown truth must not leak through
  another channel, normalization statistics or cached features.
- Output is a finite fixed-length vector. Evaluation heads receive only that vector
  and a query coordinate; no feature maps, raw local occupancy or skip connections.
- Targets are occupancy, boundaries, visible-free clearance and hidden-free distance
  recovery. Freeze boundary definition, distance truncation/normalization and query
  eligibility. Do not silently change these between controls or candidates.
- Use separate geometry-group sets for representation training, probe training,
  tuning, calibration and final assessment. Related scenes, completions and
  augmentations remain in the same group. Maintain a separate final OOD suite.
- Include thin walls, narrow gaps, clutter, cavities, density variation and partial
  observations. Define family/density weights and missingness distributions before
  search. Never select a maximum-performing stratum as the reported result.
- Cache deterministic targets with hashes; generate training masks/augmentations
  reproducibly. Prevent duplicate scenes across all new and reused data manifests.
- Freeze dataset sizes after pipeline profiling and calibration, before tuning.
  Final assessment must not be used for early stopping or search-space changes.

## Candidate models and training

Screen three position-preserving aggregation families: ordered spatial-grid pooling
plus MLP, learned strided convolution, and position-aware attention pooling.
Freeze their exact shapes, positional encoding, parameter counts and compute before
the structural screen. A pooling design must not erase obstacle position through
unqualified global averaging.

Start from the validated spatial backbone. Compare aggregation-only training with
the backbone frozen against joint backbone/aggregation training. Train query
decoders through the vector using occupancy, boundary and distance objectives.
Spatial auxiliary losses may support backbone learning, but cannot supply inputs
to compact-vector evaluation heads. Record gradient paths and trainable parameters.

Discard training decoders when evaluating a checkpoint. Freeze the entire encoder
and aggregation module; fit fresh small probes with identical capacity, examples,
optimizer budgets and selection rules. Use train-only normalization and a fixed
coordinate encoding. Pretraining reconstruction loss alone never ranks usability.

Controls include the existing spatial representation, random encoder, coordinates
only, null input, and a nonlinear raw-input predictor. Report actual parameter and
compute counts; a raw-input baseline with a much larger first layer is not silently
called capacity-matched. Freeze control architectures and matching tolerances in C4.
Test zeroed/shuffled vectors with fixed heads for embedding necessity; independently
fit null/shuffled controls for selectivity. These answer different questions.

## Compute profiling

Measure preprocessing, transfer, training, probe fitting and validation separately.
Record examples/second, optimizer updates, geometry exposures, GPU allocated peak,
wall time and GPU-hours. Utilization alone is not a success metric.

Benchmark batch sizes, CPU workers, caching and mixed precision against a float32
reference. Numerical compatibility tests must include losses, finite gradients and
validation agreement with preregistered tolerances. Reserve memory headroom; do not
launch overlapping GPU trials merely to fill memory. Use concurrency only when it
improves measured aggregate throughput without changing trial budgets or semantics.
Cache frozen-backbone features only when keyed by the exact input, mask, model and
augmentation state; do not accidentally remove masking diversity to accelerate fits.

## Search design

First screen aggregation family, vector dimension and frozen versus joint training.
The nominal balanced structural grid has 3 x 3 x 2 = 18 cells. Reserve representation
for every cell before allocating additional trials. Tune the strongest two structural
choices with randomized hyperparameters; target 36 configurations in total, including
the structural screen. Actual counts are frozen in C4 after cost measurement.

| Parameter | Proposed initial domain |
| --- | --- |
| Vector size | 64, 128, 192 |
| Aggregation | Ordered grid pooling, strided convolution, position-aware attention |
| Backbone mode | Frozen; joint |
| Learning rate | Log-uniform 1e-5 to 3e-3 |
| Weight decay | Explicit zero branch; log-uniform 1e-5 to 1e-2 |
| Joint backbone LR multiplier | 0.1, 0.3, 1.0; not applicable when frozen |
| Objectives | Occupancy/boundary/distance balance and spatial auxiliary weight |
| Masking and queries | Missingness level; balanced versus boundary-focused sampling |

Objective coefficients, missingness ranges, sampling proportions, schedules and
initialization seeds are unresolved numeric choices for C4, not executable defaults.
Keep evaluation query weights fixed regardless of training sampling. Do not tune
probe capacity per candidate. Log resolved configurations, including conditional
parameters, so the search is reproducible.

Use successive resource allocation at fixed training-exposure milestones, with probe
evaluation included in the budget. Specify how batch sizes affect example exposure
and optimization updates. Record FLOPs/time alongside exposure; equal steps alone
do not mean equal data or compute. Randomized search and multi-fidelity allocation
are grounded in [Bergstra and Bengio](https://www.jmlr.org/beta/papers/v13/bergstra12a.html)
and [Hyperband](https://www.jmlr.org/beta/papers/v18/16-558.html).

Reserve full-budget runs for randomly selected configurations, chosen before early
scores are known, to detect slow learners discarded by pruning. If those controls
contradict early rankings, revise allocation prospectively with new run identities.
Publish unstable, pruned, failed and successful trials, not only the winner.

## Budget and selection

Proposed initial ceiling: 48 GPU-hours across the campaign. This is a planning
estimate, not authorization to consume it. Obtain execution-budget approval before
launch; define the GPU-hour accounting convention and track CPU/wall costs as well.

| Stage | Share | Nominal GPU-hours |
| --- | ---: | ---: |
| Correctness, controls, calibration and profiling | 10% | 4.8 |
| Structural and hyperparameter search | 50% | 24.0 |
| Multi-seed confirmation | 25% | 12.0 |
| Final assessment and packaging validation | 15% | 7.2 |

Freeze an executable schedule within this cap after profiling: trial counts, rung
exposures, protected long runs, probe fits and timeout behavior. If projected cost
does not fit, reduce scope before search; never silently extend the cap or remove
confirmation to spend more on screening. Cached work and resumed trials remain in
the accounting ledger.

Confirm the top three configurations across three training seeds. Shared initial
screen seed(s) support paired screening but do not establish robustness. Select the
winner from tuning/confirmation only, then lock its weights, head-fitting procedure
and selection thresholds before one final assessment. Repeated final-test-driven
changes require a new independent assessment set and recorded deviation.

## Acceptance and failure-directed decisions

C4 must freeze absolute per-task floors based on intended utility and calibration,
not on the eventual winner. Also freeze compression noninferiority margins relative
to the spatial reference, minimum improvement over controls, necessity/selectivity
criteria, uncertainty method and deployment resource limits. Previous local spatial
pilot margins are evidence to consider, not automatically appropriate here.

Report geometry-cluster confidence intervals, each seed, every task, family, density,
missingness and spatial region. Include probability calibration for classifiers.
Specify multiplicity treatment and the ranking/tie-break rule before tuning. A single
aggregate cannot hide a failed core task. Among qualifying candidates, choose the
smallest vector, with frozen secondary latency/quality tie-breaks. Any certification
claim must separately satisfy the governing pretraining specification.

| Observation | Next action |
| --- | --- |
| Leakage, corrupted artifacts, nonfinite output | Repair validity; invalidate affected runs |
| Training loss improves but fresh probes do not | Investigate decoder reliance, probe capacity and representation transfer |
| Spatial reference succeeds but all compact sizes fail | Test bottleneck capacity/aggregation under a new protocol |
| Training succeeds but unseen geometry fails | Refine diversity and augmentation, not test-set thresholds |
| Random/raw/null controls match the encoder | Diagnose shortcut or missing pretraining benefit; no usefulness claim |
| Quality passes but resource budget fails | Optimize execution or choose a smaller qualifying candidate |
| No candidate meets absolute floors | Publish experimental result and diagnosis; do not lower floors retroactively |

Quality failures direct bounded follow-ups; they do not terminate all research.
Validity failures prevent using affected evidence. Packaging an experimental artifact
is allowed with explicit limitations; it is not the same as certifying it usable.

## Deliverables and first increment

Publish the frozen encoder and preprocessing contract, batch API, example inputs,
checkpoint metadata, model card, reproducibility tests and compact evaluation report.
Include tensor shape/dtype, mask semantics, spatial coverage, source/data hashes,
training budget, search ledger and failed configurations. Store weights and corpora
outside Git, with artifact hashes/locations in the manifest. Promotion remains a
separate reviewed issue and selective cherry-pick workflow.

First implementation increment: C0-C3, establishing the bottleneck-only harness and
measured cost model. C4 is the transition from this plan to an executable frozen
campaign. Open choices include utility floors, dataset counts, detailed loss/masking
ranges, ranking rule, resource limits and authorized budget. No training has been
launched by creating or committing this document.
