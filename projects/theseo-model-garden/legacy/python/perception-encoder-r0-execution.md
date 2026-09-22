---
title: v2r2 R0 execution registration
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/perception-encoder-r0/README.md
  - ../../experiments/perception-encoder-r0/protocol.md
  - ../../experiments/perception-encoder-r0/iterations/registered-run/execution.md
  - ../../experiments/perception-encoder-r0/iterations/registered-run/results.md
  - perception-encoder-r0-result.md
---

> This entry is historical and is not an authoritative specification. The original
> registration is preserved below without normalizing its identity-bearing paths,
> revisions, hashes, limits, or claims.

## Archived material

This record is the pre-data v2r2 R0 execution registration. It froze the topology-
identifiability question, generator and query policy, sample counts, controls,
uncertainty treatment, decision gates, calibration commitments, budgets, and stop
rule before the audit opened its data.

## Why it was archived

The flat registration and its result were migrated into a structured experiment so
that the frozen protocol, execution evidence, and results have distinct owners. This
archive remains provenance for the original wording and identities; it must not be
used to define a new run or to authorize continuation past R0.

## Authority ended

By the 2026-09-22 structured migration, current interpretation and navigation moved
to the canonical `perception-encoder-r0` experiment. The immutable pre-data
registration at revision `a0d03c434be72d6eab7d962e53af62a7dd57b11d` remains part
of the evidence chain rather than an active specification.

## Current replacement

- [Experiment overview](../../experiments/perception-encoder-r0/README.md)
- [Canonical frozen protocol](../../experiments/perception-encoder-r0/protocol.md)
- [Registered-run execution](../../experiments/perception-encoder-r0/iterations/registered-run/execution.md)
- [Registered-run results](../../experiments/perception-encoder-r0/iterations/registered-run/results.md)

## Continuing evidential value

Keep this record to interpret old reports, checkpoints, reviews, and manifests that
cite specs issue 27, Theseo AnySearch issue 340, implementation PR 352, governing
pilot revision `0060366f43892bade5acf734cf2e189d8a666ad2`, configuration hash
`6a56e73552066d03d4c1f6d1e08aecbc4171d4ad4ddb22d92eb17462b5215c29`, or the
pre-data registration revision above. The post-run evidence remains preserved in
[the historical R0 result](perception-encoder-r0-result.md).

---

## Preserved historical registration

# v2r2 R0 execution registration

Status: registered before audit data; review pending
Tracking: specs#27, theseo-anysearch#340, implementation PR #352
Governing pilot specification: `0060366f43892bade5acf734cf2e189d8a666ad2`

This document resolves the pre-data choices required by the v2r2 section of
[the pilot specification](perception-encoder-pilots.md). It does not amend the
completed v1/v2/v2r1 runs, weaken the topology stop rule, or authorize a comparative
run. The source implementation, this registration commit, and the resolved audit
contract must be committed and pushed before R0 opens its pools. Review remains
required before merging either repository's PR.

## Question and scope

Does a visible-input predictor obtain usable completed-connectivity signal under
the specified empirical patch-completion distribution, beyond a geometric-summary
prior, while surviving the frozen uncertainty and generator-robustness checks?

This is **not** an exact posterior for the native world generator, nor a learned
sensor-completion model. A deferral establishes insufficient evidence for this
distribution, sampling policy, predictor and budget. It does not prove that
topology is impossible to learn or rank encoder architectures.

## Generator and query policy

- Use fresh `pilot-v2r2-s3402701-*` IDs from the parent training partition.
  No opened historical geometry or observation is reused.
- Source volumes use the existing procedural voxel generator: boxes, thin
  obstacles, topology walls, and synthetic ellipsoids. The last family retains
  its historical `imported` key but is not real imported geometry.
- Configuration A is a native radius-8 crop. Configuration B is a radius-16 crop
  sampled at stride two. Both yield `17^3` arrays. B is absent from predictor
  fitting. This is a spatial-sampling transfer check, not a wholly new generator.
- Construct separate fixed donor banks of 96 volumes per configuration, balanced
  over four families and three density bands. Donors are not fitted predictor
  examples. All conclusions condition on these banks.
- Hide a central depth-axis slab of width 1, 3 or 6. Select a transverse coordinate
  uniformly among locations where the cells immediately outside both slab faces
  are observed free. Those cells are the endpoints. The unique shortest optimistic
  path is straight across the slab; its unknown count is exactly the slab width.
  Neither the native completed label nor a sampled completion chooses the query.
- R0 strata are therefore **observable optimistic-path** bins `1-2`, `3-5`, `6+`.
  This keeps every fixed observation/query and all its completion labels together
  when estimating conditional entropy. R1, if reached, separately uses completed
  shortest-path span for positives and optimistic-path span for negatives; every
  negative belongs to exactly one bin. R0 does not claim these are identical
  stratifications.
- Rank donor volumes by Hamming distance over all visible cells. Break ties by
  frozen donor index. Draw 64 independent completions with replacement, uniformly
  from the nearest 16 donors, copying **only** their hidden cells. Completed
  reachability is computed by six-connected components, never inserted as a
  visible feature. Hidden-cell values and family/density metadata cannot affect
  donor ranking.
- Patch joins can be unnatural. Entropy is for this explicitly defined empirical
  distribution, conditional on configuration and fixed bank, not a certified
  Bayes-error bound. IID here describes donor draws, not independence of voxels.

## Counts and selection

Per optimistic-span stratum, reserve 144 training candidates, 48 in-domain audit
candidates and 48 transfer candidates. Generate candidates in their frozen order;
select the first 72/24/24 eligible geometries respectively, with quotas of 6/2/2
per family/density group. Eligibility requires visible occupancy and an observed
query. Maintain a global set of selected observation hashes, training first,
then in-domain, then transfer, to exclude repeated observations even if their
queries differ. Selection reads no completion labels or predictor scores.

Candidate eligibility, exclusion reasons and hashes are retained. Extra candidates
are a fixed predeclared reserve, not adaptive replacement sampling. No additional
identities are drawn if quotas cannot be filled. There is one query per selected
geometry and 64 completion draws per query. Expected selected counts are 216
training and 144 audit geometries, with 23,040 selected completion labels total.
All candidate completions may be materialized for fixed-order parallel generation;
unselected candidates never enter control fitting or assessment.

Future training, calibration, diagnostic and decision pools are separately reserved
in the protocol identity manifest and remain unopened by R0. The query-plan hash
addresses the deterministic sampling recipe and input identities; the data manifest
also records the materialized query hashes after execution.

## Controls and uncertainty

Frozen R0 recipe: full-batch AdamW, 1,024 updates, learning rate 0.001, weight decay
0.01, initialization seed 3402703, final checkpoint only. Geometry-weighted
standardization is fitted on training examples only. Completion-mean soft targets
give the exact completion-averaged binary cross-entropy without copying the full
voxel input 64 times.

| Control | Inputs and model |
|---|---|
| Geometric prior | Linear model over observed occupancy fraction, unknown fraction and normalized endpoint L1 separation. |
| Coordinates | Linear model over six normalized endpoint coordinates. Diagnostic only. |
| Visible context | Flattened observed occupancy, unknown mask and coordinates; one hidden ReLU layer of width 128. |
| Forbidden ablation | Normalized native-generator seed, family/density one-hot metadata, configuration and slab width; one hidden ReLU layer of width 32. These features do not reach the visible model. |

Fit the same training pool/recipe for both evaluation domains. No evaluation labels,
features or checkpoints affect fitting. Store fitting, preprocessing and model
hashes and parameter counts. The forbidden predictor measures metadata
predictability, not proof that those features leaked into an encoder.

For each domain/stratum require 24 geometries and at least 64 queries of each label.
Treat complete geometries as resampling units, preserving family/density strata;
aggregate equally over geometries and then contexts. Use 10,000 bootstrap resamples,
seed 3402702. Confidence bookkeeping targets 95% simultaneous coverage: half the
error budget covers exact-binomial envelopes for conditional label entropy and
half covers 21 population decision intervals (seven per stratum). Cluster-bootstrap
coverage remains approximate. Constant finite completion samples do not establish
zero population entropy.

Every required stratum must satisfy the following conservative interval bounds:

| Gate | Frozen bound |
|---|---|
| Conditional entropy | Worst-domain upper bound < 0.90 bits. |
| Visible skill over geometric prior | Weaker-domain lower bound > 0.02 bits/query. |
| Forbidden-feature skill over prior | Worse-domain upper bound < 0.02 bits/query. |
| Source-to-transfer visible-skill drop | Upper bound < 0.05 bits/query. |

Use log-base-two binary cross-entropy with probabilities clipped to
`[1e-6, 1 - 1e-6]`. Empty strata, insufficient selected training/audit support,
or an interval touching/crossing a bound yield `defer: insufficient_evidence`.
The thresholds are pre-data pilot design choices, not values inferred from the
earlier non-evidential screen or a claim of universal encoder quality.

## Calibration commitments and stop rule

The machine-readable configuration fixes the R2/R3/R4/P0D choices before R0:
`experiments/perception_encoder/v2r2-r0-config.yaml`, SHA-256
`6a56e73552066d03d4c1f6d1e08aecbc4171d4ad4ddb22d92eb17462b5215c29`.

R2: candidate probe `198 -> 128 -> 1`; nonlinear raw control has three stride-one
3D convolutions `2 -> 8 -> 16 -> 32`, global mean, coordinates and MLP width 144.
It has 23,529 parameters versus 25,601 for the candidate probe (within 10%). The
over-capacity empirical reference uses `2 -> 32 -> 64 -> 128`, global mean,
coordinates and MLP width 512 (348,065 parameters). Convolutions use kernel 3,
padding 1, biases and ReLU; there are no normalization layers. All receive only
observed channels and coordinates. Fixed 5,000-update AdamW fits use learning rate
0.001, decay 0.01 and the final checkpoint. kNN with k=15 is diagnostic only, with
geometry-disjoint preprocessing/evaluation, never a certified ceiling.

R3: four hash-ranked observed-free anchors; complete fields use VI, Adapted Rand,
Betti-0, false merge and false split. Select thresholds from `0.05:0.05:0.95` on
three training-geometry folds by balanced accuracy, taking the lowest tie. Require
200 negative queries. Freeze the false-merge veto as the smaller raw/reference
95% upper cluster-bootstrap bound plus 0.02, capped at one.

R4: the admissible menu is conditional-log-loss gain and AUPRC, but this execution
selects **conditional-log-loss gain only, with no fallback**. Require the measured
nonlinear-raw minus reference loss gap to reach 0.10 bits. AUPRC stays diagnostic;
there is no switch merely because it passes. The four required components are
occupied IoU, boundary F1, clearance NMAE and reachability; geodesic is deferred.
Local target templates remain v2r1 and anchors are freshly measured. Selectivity
and embedding necessity require 0.05 normalized **per-component** gains, not a
five-component aggregate. P0D holds fitting updates fixed with four times the
observation density, requiring active denominators still to qualify and headroom
and false-merge changes no larger than 0.02 in their respective units.

Budgets: R0 3,600 wall seconds and 0.5 accelerator-hours; each R0 control fit at
most 900 wall seconds. P0C/P0D caps are two accelerator-hours each, P1 four.
Four CPU generation workers; explicit CUDA fitting, no silent CPU fallback.

If R0 defers, record `no_topology_identifiable`, preserve every report and do not
start P0C/P0D/P1. The local-geometry program remains a separate proposal. A
qualifying R0 authorizes P0C only. The comparative contract must verify the R0
and P0C payload chain and measured anchors before P0D/P1. Execution errors are
recorded as errors, not converted into scientific topology conclusions.

## Evidence

No evidential R0 data had been opened when this registration was committed.
Results will be appended separately, without editing the registered choices above.

Post-run evidence: [completed R0 result](perception-encoder-r0-result.md).
The pre-data version of this registration remains pinned at
`a0d03c434be72d6eab7d962e53af62a7dd57b11d`; the result records the external-review
ordering deviation explicitly.
