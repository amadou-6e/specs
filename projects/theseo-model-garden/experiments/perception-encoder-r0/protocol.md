# Frozen protocol

This is the canonical protocol for run `voxel-encoder-pilot-v2r2-r0-1`. Its choices
were published before audit data opened at specs revision
`a0d03c434be72d6eab7d962e53af62a7dd57b11d`; the immutable protocol identity is
`8230bd97ea14f14f8a8910af61cde7ad211a6c189c9129981d225b45c79a8fe3`.
The earlier flat [registration](../../legacy/python/perception-encoder-r0-execution.md)
is migration provenance, not the authority for this experiment.

## Question

Does a visible-input predictor obtain usable completed-connectivity signal under the
registered empirical patch-completion distribution, beyond a geometric-summary
prior, while surviving frozen uncertainty and generator-robustness checks?

## Scope and non-claims

R0 audits whether topology is identifiable enough to authorize P0C. It is not an
encoder comparison, exact posterior for the native generator, learned sensor
completion model, or architecture certification. Deferral means this distribution,
sampling policy, predictor, and budget supplied insufficient evidence; it does not
prove topology is unlearnable.

## Data and query contract

- Use fresh `pilot-v2r2-s3402701-*` identities from the parent training partition;
  reuse no opened historical geometry or observation.
- Generate boxes, thin obstacles, topology walls, and synthetic ellipsoids. The
  historical `imported` label denotes ellipsoids, not imported assets.
- Configuration A is a native radius-8 crop. Configuration B is a radius-16 crop at
  stride two. Both yield `17^3` arrays; B is excluded from predictor fitting.
- Build separate fixed donor banks of 96 volumes per configuration, balanced across
  four families and three density bands.
- Hide a central depth-axis slab of width 1, 3, or 6. Choose endpoints immediately
  outside its faces without reading completed labels. Bin queries by observable
  optimistic-path span: `1-2`, `3-5`, and `6+`.
- Rank donors by visible-cell Hamming distance with frozen donor index as tie-breaker.
  Draw 64 completions with replacement from the nearest 16 donors, copy only hidden
  cells, and label by six-connected reachability.
- Treat entropy as conditional on this empirical distribution and fixed donor banks.
  Patch joins may be unnatural.

## Counts and selection

Per stratum, reserve 144 training candidates, 48 in-domain audit candidates, and 48
transfer candidates. In frozen order, select the first 72, 24, and 24 eligible
geometries, with family/density quotas of 6, 2, and 2. Eligibility requires visible
occupancy and an observed query. Exclude duplicate observation hashes globally in
training, in-domain, then transfer order. Selection reads neither completion labels
nor predictor scores.

The planned totals are 216 training geometries, 144 audit geometries, one query per
geometry, and 23,040 completion labels. Draw no replacement identities if a quota
fails. Keep later-stage pools unopened.

## Controls and fitting

Use full-batch AdamW for 1,024 updates, learning rate `0.001`, weight decay `0.01`,
initialization seed `3402703`, and the final checkpoint. Fit geometry-weighted
standardization on training examples only.

| Control | Inputs and model |
|---|---|
| Geometric prior | Linear model over observed occupancy fraction, unknown fraction, and normalized endpoint L1 separation. |
| Coordinates | Linear model over six normalized endpoint coordinates; diagnostic only. |
| Visible context | Flattened occupancy, unknown mask, and coordinates; one hidden ReLU layer of width 128. |
| Forbidden ablation | Generator seed, family/density metadata, configuration, and slab width; one hidden ReLU layer of width 32. These inputs must not reach the visible model. |

Use the same training pool and recipe for both evaluation domains. Preserve
preprocessing, model, fitting, and parameter-count identities. The forbidden
ablation diagnoses metadata predictability, not input leakage.

## Uncertainty and gates

Each domain/stratum requires 24 geometries and at least 64 queries of each label.
Resample complete geometries while preserving family/density strata, aggregate
equally over geometries and then contexts, and use 10,000 bootstrap resamples with
seed `3402702`. Use base-two binary cross-entropy clipped to `[1e-6, 1 - 1e-6]`.

Every required stratum must pass every gate:

| Gate | Frozen bound |
|---|---:|
| Worst-domain conditional-entropy upper bound | `< 0.90` bits |
| Weaker-domain visible-skill lower bound over geometric prior | `> 0.02` bits/query |
| Worse-domain forbidden-feature-skill upper bound over prior | `< 0.02` bits/query |
| Source-to-transfer visible-skill-drop upper bound | `< 0.05` bits/query |

Empty strata, insufficient support, or an interval touching a bound produce
`defer: insufficient_evidence`. Point estimates cannot override these gates.

## Pinned calibration commitments

The configuration `experiments/perception_encoder/v2r2-r0-config.yaml`, SHA-256
`6a56e73552066d03d4c1f6d1e08aecbc4171d4ad4ddb22d92eb17462b5215c29`,
fixed the R2/R3/R4/P0D choices before R0. These included candidate probe
`198 -> 128 -> 1`; nonlinear raw control convolutions `2 -> 8 -> 16 -> 32`; an
over-capacity reference `2 -> 32 -> 64 -> 128`; conditional-log-loss gain as the
only primary R4 measure; occupied IoU, boundary F1, clearance NMAE, and reachability
as required components; and geodesic performance deferred. The full numeric
registration remains preserved at its pinned revision and cannot be changed under
this protocol identity.

## Resource and stop rules

R0 is capped at 3,600 wall seconds and 0.5 accelerator-hours; each control fit is
capped at 900 wall seconds. Use four CPU generation workers and explicit CUDA fitting
with no silent CPU fallback. Execution errors remain errors.

If any R0 gate defers, record `no_topology_identifiable`, preserve all evidence, and
do not start P0C, P0D, or P1. A pass authorizes P0C only. Changing bins, thresholds,
primary metrics, or support requirements requires a new protocol identity.

## Validity limits

- Conditional entropy is not a native-world posterior.
- Completion draws are IID only conditional on fixed donor banks, not across voxels.
- Cluster-bootstrap coverage is approximate.
- Configuration B changes spatial sampling, not the whole generator family.
- External review had not completed when execution began. This does not alter the
  pre-data identity, but prevents claiming prior external approval.
