# Governing protocol

This canonical protocol reconstructs the completed local-geometry program from the
three prospectively frozen registrations. It does not retroactively replace their
immutable specification commits. When exact wording or a field-level identity is
needed, the pinned legacy protocol listed in [sources.md](sources.md) remains the
historical authority.

## Shared question and boundary

Evaluate whether frozen eight-channel local encoder features support hidden occupancy,
exact occupied-boundary, observed-free clearance, and hidden-free clearance-recovery
probes. No iteration may claim topology, connectivity, planning, navigation,
wide-context or global-latent quality, real-world transfer, or model certification.

## Shared representation and data rules

- Dense mask-aware partial-convolution residual pyramid, stem width 8, stages
  8/16/32/64, eight local output channels, radius 8 (17 cubed cells).
- The global projection receives no local-loss gradient and is neither trained nor
  qualified by this program.
- Hiddenness is independent Bernoulli(0.20). Hidden input values are excluded through
  the support path. Missing-cell recovery is synthetic corruption, not visibility.
- Occupancy and boundary queries use hidden cells; clearance uses observed free cells;
  recovery uses hidden ground-truth-free cells. Each task samples 256 eligible cells
  per geometry. Empty pools or insufficient binary classes invalidate the run.
- Boundary is exact six-neighbor boundary with no spatial tolerance. Clearance is
  positive crop-local signed distance clipped at eight voxels and divided by eight.

## Shared frozen probe and controls

Discard pretraining heads, freeze and hash the encoder, normalize from probe-fitting
features only (standard-deviation floor 1e-5), and fit one
`Linear(8,32)-SiLU-Linear(32,1)` probe per task for 512 updates, batch 1,024, AdamW
learning rate 0.001 and weight decay 0.01. Use final checkpoints, classification
threshold 0.5, and clip regression predictions to [0,1]. Controls are paired random
encoders, zeroed features, row-shuffled features, and shuffled probe-fitting labels.
The 81-input raw-neighborhood probe and full-information oracle are diagnostics only.

## Shared absolute and control gates

Every participating seed must satisfy all four absolute bars: occupied IoU >=0.60,
boundary F1 >=0.70, clearance NMAE <=0.15, and recovery NMAE <=0.20. Against every
control, classification improvement must be >=0.05 and regression must provide >=10%
relative error reduction with positive gain. The seed-mean paired improvement must
also have a strictly positive lower 95% stratified geometry-bootstrap bound (2,000
draws). Finite predictions, unchanged encoder state, zero hidden-value isolation
difference, and <=5% near-dead local channels are hard integrity gates.

## LG1: specialist screen

- Identities: study `voxel-encoder-local-geometry-v1-lg1`, dataset suffix
  `dataset-1`, queries suffix `queries-1`.
- Arms: occupancy and ESDF; seeds 0 and 1; paired initialization.
- Data: 96 training, 48 probe-fitting, and 48 evaluation geometries, balanced across
  twelve procedural family/density strata and mutually disjoint.
- Encoder budget: 1,024 updates, batch 8, AdamW 0.001, weight decay 0.01, FP32;
  four-hour cap. Occupancy uses unweighted BCE; ESDF uses Smooth L1.
- LG1 additionally treated covariance effective-rank fraction >=0.25 as a hard gate.
- Disposition per arm: `qualifies_local_followup` or `not_qualified`.

## LG2: joint preservation

LG2 was a prospectively registered continuation with fresh identities and data, not
an amendment of LG1.

- Identities: study `voxel-encoder-local-geometry-v1-lg2`, dataset suffix
  `dataset-2`, queries suffix `queries-2`.
- Arms: occupancy, ESDF, and joint; seeds 0, 1, and 2. Joint loss is BCE plus ten
  times ESDF Smooth L1. Each arm receives the same 1,024-update budget.
- Data counts and twelve strata match LG1 but all identities are fresh.
- A preregistered development-fixture result made covariance/correlation rank
  diagnostic rather than a hard gate; dead-channel, task, control, and integrity
  gates remained mandatory. This does not alter LG1's verdict.
- Joint must also be noninferior to occupancy on IoU/boundary (margin 0.03) and ESDF
  on clearance/recovery (margin 0.02), for every seed and paired interval.
- Primary disposition: `joint_preserves_specialists` or
  `joint_hypothesis_not_validated`.

## LG3: independent-generator confirmation

LG3 froze the three LG2 joint encoders and performed zero encoder updates.

- Identities: study `voxel-encoder-local-geometry-v1-lg3`, dataset suffix
  `dataset-3`, queries suffix `queries-3`.
- Data: 48 probe-fitting and 48 evaluation geometries across `random_field`,
  `oblique_sheets`, `height_field`, and `curved_tubes`, each crossed with occupied
  fractions 0.08, 0.16, and 0.28. Generators were independently implemented but
  remain synthetic.
- Fresh target-domain probes are the primary path. Unchanged LG2 probes and
  normalizers form a separately reported zero-shot diagnostic.
- In addition to pooled gates, every generator family must pass every absolute bar
  in every seed. No family deletion, redraw, threshold adjustment, or training on
  LG3 evaluation labels is permitted.
- Primary disposition: `independent_generators_confirmed` or `not_confirmed`.

## Execution envelope and forbidden adaptations

All runs use deterministic CUDA FP32 with TF32 disabled and four CPU threads. LG1
and LG2 have four-hour caps; LG3 has a two-hour cap. No evaluation-guided retries,
post-hoc gate changes, architecture/radius scaling, corpus redraws, or best-seed
selection are authorized under these identities. Changed objectives, budgets,
thresholds, or claims require a new registration and fresh evaluation identities.

## Analysis and publication

Report every arm and seed, per-geometry sufficient statistics, curves, controls,
bootstrap intervals, integrity diagnostics, runtime, registration/report identities,
and artifact hashes. Weights, generated volumes, and tensor predictions remain
outside Git. A failed screen is a completed experiment and must remain visible.

## Threats to validity

Evidence is synthetic, crop-local, conditioned on few training seeds, and uses fitted
probes with fixed finite budgets. Geometry-bootstrap intervals do not estimate the
population of training seeds. Procedural family names do not imply real imported data
or topology supervision. The raw-neighborhood diagnostic is not capacity matched.
