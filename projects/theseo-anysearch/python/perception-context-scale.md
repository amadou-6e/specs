# Fixed-resolution 17 to 33 context pilot

Issues specs#47 / theseo-anysearch#372. Authorized stack on unmerged exp/370;
no integration merges or promotion. Prior validation specification:
bc3a092d07309eb8f22390bd2878f371713badad in specs. Separate local-geometry study.

## Paired scene contract

Study `voxel-context-scale-v1`; scene IDs `voxel-context-scale-v1-data-<split>-<index>`.
Pretraining48 /probe-training48 /selection24 /assessment48 parent scenes,
balanced over two stationary families and density fractions0.08/0.16/0.28.
This deliberately small pilot does not reproduce the earlier192-geometry training.

Generate a49-cubed parent once. Random-field family: Gaussian noise smoothed at
sigma1.5 voxels, reflect boundary. Oblique sheets: coordinates -24..24 divided by8,
unit-normal projection, frequency uniform[4,8], phase uniform[-pi,pi], absolute
sine. Occupancy threshold is the parent's fraction quantile, never recomputed per
crop. Seed NumPy from first8 little-endian SHA256 bytes of the scene ID.
Take exact nested central17 and33 crops. Voxel spacing never changes;33 doubles
radius8 to16, rather than increasing spatial resolution. Parent margin eight
beyond33 supports truncated distance targets without a new crop-boundary target.

Compute boundary and signed distance on the parent, truncation/divisor8. All
evaluation queries lie in the central17 and use exactly the same targets and
missingness in both arms. Independent20% parent masks seeded by SHA256 of
scene ID plus `-mask`; shared crop masks. Use256 eligible queries per geometry/task,
replacement only for small nonempty pools. Distance eligibility matches prior
protocols. Query RNG37200+split index, split order pretrain/train/selection/assessment.
Reject duplicate parent hashes and insufficient family class support (<20 each
binary class); never redraw. The comparison tests central predictions with more
context, not quality over the entire newly visible33 crop.

## Arms and budgets

Seeds0/1/2. Four arms per seed:

- Frozen validated encoder at17 and at33, weights identical across sizes.
- Fresh same-architecture encoder trained at17 and at33 for512 updates each.

Retraining: batch4, AdamW lr0.003/wd0.01, existing joint occupancy BCE +10 times
normalized ESDF SmoothL1, exact same architecture/global-projection exclusion.
Fresh initialization for each size, paired seeds and minibatch streams37210+seed.
Draw a33-cubed training mask then centrally crop for17, preserving paired physical
missingness. Use all hidden crop voxels for loss. Equal updates are not equal voxel
compute; record the cost difference. Final encoder weights only; the short budget
cannot establish fully tuned scale-specific performance.

Freeze each encoder during probe fitting. Separate fixed32-hidden heads per arm,
task and seed, AdamW0.001/wd0.01, batch1024,1024 updates; train-only normalization.
Classification thresholds selected by original-family selection F1 over0.01..0.99,
ties lowest. Distance probes unchanged. This tests shared encoder weights with
scale-adapted readouts, not transfer of unchanged probe heads.

## Comparisons and resource measurements

Report frozen33 versus frozen17, retrained33 versus retrained17 and retrained33
versus frozen33. Primary metric is each task's paired improvement, recomputing
pooled classification ratios on each bootstrap sample. Bootstrap whole parents
within six family/density strata, keep arm/seed pairing,2000 draws, seed372.
Non-inferiority lower95% improvement bound >=-0.03 classification or >=-0.02
distance. Absolute scores and per-family results remain visible diagnostics.
Do not reinterpret non-inferiority as evidence that added context helps.

Profile identical batch4 forward passes:3 warm-ups,20 timed iterations with CUDA
synchronization. Record crops/sec, ms/batch, total and incremental allocated peak
memory. Training records512-update duration and total allocated peak. Timings are
local pilot measurements, not isolated production benchmarks; no extrapolation
to65 or radius512. Memory is CUDA tensor allocation, not total device usage.

If frozen33 is non-inferior, shared weights remain a candidate, subject to resource
costs. If retraining improves33, investigate scale-conditioned training. Otherwise
record uncertainty; do not force an architecture decision from512 updates. No
automatic65-cubed launch. Any next run needs a separate frozen contract.

## Integrity

Freeze exact source/spec commits, parent/crop/target/query hashes and source encoder
file/state hashes before fitting. Verify unchanged evaluation states afterward.
Overall7200 seconds including preparation; maximum1200 per encoder fit, checked
each update, plus overall checks between bounded probe fits. Incomplete or invalid
runs cannot establish non-inferiority. Commit compact evidence only. No topology,
planning, full-volume accuracy or promotion claims follow.
