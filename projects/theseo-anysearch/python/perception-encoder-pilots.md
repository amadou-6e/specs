# Pilot Plan: Voxel Encoder Direction Finding

Status: discovery
Owner: amadou-6e
Last reviewed: 2026-09-01
Tracking issue: [specs#13](https://github.com/amadou-6e/specs/issues/13)
Governing validation plan:
[Standalone Voxel Encoder Pretraining](perception-encoder-pretraining.md)
Architecture research:
[Scalable 3D Voxel Perception Encoders](perception-encoders.md)

## Decision boundary

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

## Pilot corpus

Create `voxel-encoder-pilot-v1` only from geometry IDs assigned to the parent training
split. Assign geometry IDs before sampling observations and store the assignment hash.

| Nested split | Geometry IDs | Observations | Use |
|---|---:|---:|---|
| `pilot_train` | 64 | 24,000 | Encoder and probe training. |
| `pilot_dev` | 16 | 6,000 | P1-P6 checkpoint and direction selection. |
| `pilot_confirm` | 16 | 6,000 | Open once for P7 after the top two pairings are locked. |

`pilot_train` and `pilot_dev` cover open rooms/boxes, thin walls/isolated obstacles,
corridor/topology scenes, and imported geometry. In `pilot_confirm`, eight geometries
come from the same families with new seeds, four use a held-out procedural topology
template, and four come from an imported-geometry source absent from encoder
pretraining. Report these three confirmation groups separately; do not tune their
weights after P7 begins.

Sample radii 8 and 16 equally for P0-P4. Generate radius-32 observations from the same
IDs only when P5 starts. Balance boundary, topology, ordinary free-space, open-space,
and unknown cases using the governing sampling shares. Within every nested split,
balance low, medium, and high occupied fractions. No observation may move between
nested splits, and no augmented view may cross a split.

The frozen pilot probe set is smaller than certification:

| Probe | Training examples | Dev/confirm examples | Maximum updates |
|---|---:|---:|---:|
| Global linear | 12,000 observations | 3,000 | 2,000 |
| Occupancy/clearance coordinate | 100,000 queries | 20,000 | 5,000 |
| Reachability/geodesic pair | 50,000 balanced pairs | 10,000 | 5,000 |
| Topology decoder | 8,000 observations | 2,000 | 5,000 |

Probe architecture and optimizer are fixed after P0. Every coordinate and pair probe
still runs the control-target, zero-embedding, and shuffled-embedding controls. Pilot
queries and their stratum weights are immutable after their hashes are recorded.

## Common comparison contract

Unless a pilot says otherwise:

- use the Tiny capacity family and a 192-dimensional global embedding;
- initialize from scratch; no candidate receives a pretrained parent;
- use seed 0 for direction finding and fresh seeds 1 and 2 for P7;
- use the same ordered observation batches, augmentation draws, probe examples, and
  checkpoint steps within a paired comparison;
- count encoder updates, observations, encoded valid voxels, accelerator-hours, peak
  memory, and wall time;
- run on one declared reference accelerator, disable compilation, and use BF16 only
  when every candidate supports it reliably; otherwise use FP32 for the comparison;
- compare trainable encoder parameters within 10%; report decoder, projector, and
  predictor parameters separately; and
- evaluate frozen probes at 25%, 50%, and 100% of each run's update budget.

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

The following vetoes apply to every comparative pilot:

- state-integrity, numerical-reproducibility, or applicable mask-isolation failure;
- effective-rank fraction below 0.25 or more than 5% near-dead dimensions at the final
  checkpoint;
- control-target selectivity below 0.05 pilot-score units;
- zeroed or shuffled embeddings within 0.05 of the real-embedding pilot score;
- `pilot_dev` false-open rate above 5% or more than 2 percentage points worse than the
  current encoder; or
- unsupported output shapes, invalid masks, OOM, or missing resource accounting.

A one-seed difference below 0.03 pilot-score units is a tie. Never use a lower pretext
loss to break a frozen-probe tie. Carry tied candidates forward when the next pilot has
capacity; otherwise prefer the lower-memory candidate while recording the tie.

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
updates and seed 0: eight trained trials. Masked and unmasked paths retain the same
residual stage widths, output dimensions, and probe contracts; report their different
executed-voxel counts rather than claiming identical kernels.

Exit: retain at most two bundles. A bundle must pass all vetoes and improve at least
three of the five pilot-score components over random weights. Select the best learning
rate per bundle by pilot score. When T1/T3 and T0/T2 are within 0.03, retain one masked
or latent bundle and one direct-geometry bundle so a one-seed tie does not erase a
meaningfully different direction.

### P2: Native training-mechanics screen

**Hypothesis:** one native recipe choice matters more than broad optimizer tuning once
a useful target family has been found.

For each of the two retained bundles, run the baseline plus its two applicable variants
below for 4,000 updates and seed 0: at most six trained trials total.

| Bundle | Baseline | Variant 1 | Variant 2 |
|---|---|---|---|
| T0 | class-balanced full-volume occupancy | focal loss, gamma 2 | surface/frontier-only target sampling |
| T1 | mask ratio 0.60 | mask ratio 0.40 | mask ratio 0.75 |
| T2 | ESDF truncation `0.25 * radius` | `0.125 * radius` | `0.50 * radius` |
| T3 | mask 0.60, EMA 0.996 | mask 0.40 | EMA 0.99 |

All variants use proper cube rotations and no other augmentation. Promote a variant
only when it gains at least 0.03 pilot-score units or improves one component by at
least 0.05 without regressing another by more than 0.02. Otherwise retain the simpler
baseline. The result is a locked training bundle for each retained target family.

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

Train every P3 survivor with the best P2 bundle for 4,000 updates, seed 0, radius 16,
and identical pilot batches. Every candidate sees the full radius-16 physical extent.
The dense and residual candidates use a `33^3` input; the pyramid uses side 17 at
strides 1, 2, 4, and 8; the tri-planar model uses the three orthogonal `33^2` planes.

Retain the best quality candidate and every candidate within 0.03 pilot-score units
that reduces peak memory or p95 latency by at least 25%. Keep no more than two base
families. If the shared pyramid is retained, spend up to two additional trials on FiLM
and residual-adapter conditioning. If a dense residual family is retained, spend one
additional trial on the matched-parameter two-branch dilation/Inception block. Do not
test independent per-scale weights, norm variants, or equivariance yet. P4 is capped at
eight trained trials including conditional variants.

Exit: name a provisional primary architecture by quality and a fallback by the Pareto
frontier of quality, memory, and latency. If no learned architecture beats the random
encoder on three pilot-score components, return `no viable direction` and stop.

### P5: Field-of-view micro-ablation

**Hypothesis:** the provisional primary benefits from multiscale context without
requiring a large per-level dense volume.

Use the P4 primary and its fixed P2 training bundle for four seed-0 trials of 4,000
updates:

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

Exit: choose the smallest side and fewest scales within 0.03 of the best radius-16
pilot score and within 0.02 on every component. Radius 32 advances only if it improves
reachability or geodesic score by at least 0.03 without a veto and adds no more than
one declared scale level. Otherwise keep radius 16 for the next pilot and leave wider
context to the full radius study.

### P6: Objective-by-architecture interaction check

**Hypothesis:** the selected recipe and architecture directions are not artifacts of
being evaluated with only one counterpart.

Cross the top two P2 training bundles with the P4 primary and fallback architecture/
field-of-view bundles. Train the four pairings from scratch for 8,000 updates with seed
0. Use the same batches and cap each pairing at the smaller of the fixed update budget
or the preregistered accelerator-hour budget.

Report the recipe effect within each architecture, the architecture effect within each
recipe, and rank correlation between the two recipe rankings. Treat either of these as
a material interaction:

- the preferred recipe reverses by at least 0.03 pilot-score units; or
- an architecture effect changes by at least 0.05 between recipes.

Exit: without a material interaction, retain the best pairing and the most efficient
pairing within 0.03. With an interaction, retain the best pairing from each
architecture and prohibit independent recipe/architecture conclusions in later
reports.

### P7: Fresh-seed confirmation

**Hypothesis:** the two retained pairings preserve their direction on fresh seeds and
previously unopened pilot geometries.

Lock all choices, then train both pairings from scratch for 10,000 updates with seeds 1
and 2: four trained trials. Open `pilot_confirm` only after the run manifests and
checkpoint-selection rule are committed. Report mean and per-seed metrics for the
ordinary, held-out-topology, and held-out-imported groups. Two seeds are not enough for
a significance claim; they are a guard against a single lucky exploratory seed.

Declare `winner` only when one pairing:

- passes every pilot veto on both seeds;
- leads by at least 0.03 mean pilot-score units;
- has the same score direction on both seeds; and
- has no component regression greater than 0.02.

Otherwise declare `tie` and carry both pairings into the existing Stage 1/2 program.
Declare `no viable direction` if neither pairing passes the vetoes. Never reopen P1-P6
or tune a configuration after reading `pilot_confirm`.

## Budget and stop rules

| Pilot | Maximum trained trials | Updates per trial | Maximum updates |
|---|---:|---:|---:|
| P0 | diagnostic only | 500 | not comparative |
| P1 | 8 | 2,000 | 16,000 |
| P2 | 6 | 4,000 | 24,000 |
| P3 | profiling only | 20 steps | not comparative |
| P4 | 8 | 4,000 | 32,000 |
| P5 | 4 | 4,000 | 16,000 |
| P6 | 4 | 8,000 | 32,000 |
| P7 | 4 | 10,000 | 40,000 |
| **Total** | **30 comparative trainings** | | **160,000** |

Before P1, record a per-pilot and total accelerator-hour cap. The total program stops
at the first of 160,000 comparative encoder updates or that accelerator-hour cap.
P0/P3 diagnostic work is reported separately so profiling cannot silently consume the
training budget. A pilot may spend unused trials from its own cap only; budget cannot
be moved into a later pilot after results are visible.

The 160,000-update cap is 11.9% of the 1.35 million maximum encoder updates in the
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
  "locked_inputs": {},
  "candidates": [],
  "vetoes": {},
  "pilot_scores": {},
  "resource_metrics": {},
  "decision": "winner | tie | no_viable_direction | blocked",
  "retained": [],
  "rejected": [],
  "reason": "...",
  "next_pilot": "P5"
}
```

Every rejection names the preregistered rule that fired. Store resolved configs,
checkpoints, per-geometry predictions, probe ablations, metric components, resource
traces, and failed-run logs. Failed/OOM trials count against the trial cap.

## Handoff to the full experiment plan

The pilot winner becomes the first queued direction in Stage 1, not a certified model.
The fallback remains queued until Stage 2 establishes a multi-seed result. R0, the
random encoder, the raw-grid control, and the current encoder remain mandatory even if
they lose in the pilots.

P0 evidence may satisfy a governing Stage 0 item only when it used the identical
implementation, fixtures, tolerances, and artifact contract. The remaining Stage 0
checks still run before full Stage 1; a successful pilot is not a blanket Stage 0 pass.

If P7 returns a tie, Stage 1/2 must retain both pairings and spend its additional data,
updates, and seeds on resolving the tie. If P7 finds a material recipe/architecture
interaction, Stage 2 compares complete pairings rather than swapping independently
selected parts. Architecture normalization, equivariance, independent scale weights,
Base/Large capacity, radii above 32, and final certification remain in the governing
later stages.
