# LG3: independent-generator frozen-feature confirmation

Issue `theseo-anysearch#356`; specification issue `specs#33`.
The user explicitly authorizes stacking and execution before LG2 PR #355/specs#32
merge, but no merges. Source base: `f1082e4c45dadf47226f506d253b5152615abc11`.

## Question and boundary

Do the **existing three LG2 joint checkpoints**, without any encoder updates,
support the four local tasks on independently implemented synthetic generators?
This primarily tests frozen-feature transfer **with target-domain probe fitting**.
Separately report zero-shot predictions from unchanged LG2 probes. Neither should
be confused with the other. No topology, planning, global-latent, wide-context,
real-world or radius-scaling claim follows. No weights or heads are selected by
new evaluation outcomes. All three seeds participate.

Governing prior protocol:
[LG2 at its exact frozen commit](https://github.com/amadou-6e/specs/blob/ee173bc2a61064386ee8669f77bad9ddf016b709/projects/theseo-anysearch/python/perception-encoder-local-geometry-lg2.md).
Pin LG2 report payload `a1c99cf09adc3301dbd36307575e723a094c55a1335d996761a6cc5a1f3f135a`.
The LG3 registration records all six input artifact file hashes (three encoders,
three saved probe artifacts), initial/final encoder-state hashes, exact source and
spec commits, resolved settings and all fresh geometry IDs. Verify artifacts and
loaded state hashes **before** new data generation. No encoder retraining occurs.

## Fresh generator protocol

Study `voxel-encoder-local-geometry-v1-lg3`, dataset
`voxel-encoder-local-geometry-v1-dataset-3`, queries
`voxel-encoder-local-geometry-v1-queries-3`; fresh registration/report/run identities.
There are 48 probe-fitting and 48 evaluation geometries, disjoint by ID and from
LG1/LG2. Each split balances four families crossed with occupancy fractions
0.08, 0.16 and 0.28 (four geometries per stratum).

Each family is implemented independently of the old cuboid/wall/ellipsoid corpus,
on a 17-cubed lattice with coordinates [-1,1]. A deterministic NumPy generator is
seeded from the first eight SHA256 bytes of the geometry ID, little-endian.
Draw three phases uniformly in [-pi,pi], then construct:

- `random_field`: Gaussian white noise, smoothed by scipy Gaussian filter sigma
  1.5, reflect boundaries.
- `oblique_sheets`: absolute sine of a random unit-normal projection, frequency
  uniform [4,8], plus phase zero.
- `height_field`: z minus 0.35*sin(3*x+phase0), minus 0.25*cos(4*y+phase1),
  minus uniform[-0.3,0.3]*x.
- `curved_tubes`: minimum of squared distances to two sinusoidal coordinate
  centerlines, amplitude 0.45, frequencies two and three, as fixed in the source.

Occupancy is field <= its frozen fraction's empirical quantile. This intentionally
controls density; it is not natural-world sampling or externally supplied real
geometry. No candidate performance is used to choose a generator or threshold.
All development tests generate **development-prefixed IDs only**. No failed study
corpus is redrawn or silently replaced.

Use the same missingness and query algorithm as LG2: Bernoulli(0.20) independent
of labels, fixed streams 35401/35402 for probe/evaluation. The mask stream is
deliberately reused to hold corruption methodology constant; geometry identities,
targets and complete query banks are new, not recycled LG2 banks. Sample 256
uniform eligible queries per geometry/task, without replacement unless necessary.
Hidden occupancy/boundary; observed-free clearance; hidden ground-truth-free
recovery. Empty eligible pools or fewer than 100 positive/negative binary query
rows per entire split invalidate the run, without redrawing.
Each family also needs at least 20 positive and negative rows for each binary
task on both splits, preventing vacuous family-specific scores.

Compute clean crop-local targets using existing six-neighbor boundary and signed
distance utilities. Boundary F1 has zero spatial tolerance. Clearance is positive
signed distance clipped to eight voxels/divided by eight. All-free conditioning
limitations, synthetic missingness and crop-boundary limitations from LG2 remain.

## Fitting and controls

Use exactly the LG2 frozen eight-channel local outputs; the global projection is
not qualified. Fresh per-task probes: Linear(8,32), SiLU, Linear(32,1); train-only
mean/std (floor 1e-5), AdamW lr .001, weight decay .01, 512 updates of 1,024 rows.
BCE for binary tasks, Smooth L1 for normalized regression. Final checkpoint only,
classification threshold .5, regression outputs clipped [0,1]. No tuning or
early stopping. Seeds 0/1/2, initialization 41000+seed, batch draws 42000+seed.

Controls: matched initial random encoders with separately fitted probes; zeroed
and row-shuffled frozen features; probes fitted to shuffled fitting labels.
Reuse LG2's fixed control implementations/budgets. Diagnostic only: visible
3x3x3-neighborhood MLP (81 inputs, width32), full-information target oracle, and
**unchanged LG2 probe weights and normalizers** for zero-shot transfer. No new
labels fit the zero-shot path; its scores are not the primary decision.

## Frozen acceptance

Each seed must pass IoU >=.60, exact boundary F1 >=.70, clearance NMAE <=.15,
recovery NMAE <=.20. Additionally, **each of the four generator families must pass
these same absolute bars in every seed**. Pool counts across that family's 12
evaluation geometries. This prevents a weak generator from hiding in an average.

Aggregate control improvement gates stay unchanged: >=.05 classification gain,
or >=10% relative error reduction and positive gain for regression, against every
random/zero/shuffle/shuffled-label control in every seed. The three-seed mean gain
must have a positive lower 95% percentile interval from 2,000 stratified geometry-
bootstrap draws, seed354. Four geometries sampled with replacement per stratum;
identical draws across seeds and methods. Pool confusion counts/errors first,
then compute scores. Intervals are conditional on three seeds; no seed-population
or external-domain statistical guarantee follows.

Finite predictions, zero mask-isolation error, unchanged encoder state and at most
5% near-dead channels (std<1e-5) remain hard gates. Covariance/correlation rank remain
diagnostic under LG2's preregistered deviation, not a reclassification of LG1.
No noninferiority to LG2 scores is claimed across different data distributions.

Primary result: `independent_generators_confirmed` only if every gate passes;
otherwise `not_confirmed`. No threshold adjustment, failed-family deletion or
follow-up training on these evaluation labels is permitted under this identity.

## Execution and evidence

CUDA FP32, deterministic algorithms, TF32 disabled, four CPU threads, two-hour cap.
Zero encoder updates; 48 fresh probe fits (24,576 updates), plus zero-shot inference.
Persist checkpoint metadata/hashes, registration, per-geometry statistics, family
scores, all controls, zero-shot diagnostics, intervals and written assessment with
diagram. Keep weights, volumes and tensor predictions untracked. Publish evidence
in both implementation and specs PRs. An incomplete run cannot confirm transfer.
