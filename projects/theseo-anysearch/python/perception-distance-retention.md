# Frozen encoder distance retention

Issues specs#43 / theseo-anysearch#368. User-authorized continuation without
integration merges. Source encoders are those from the continuation experiment
governed by 4349ad2ac47cbad912a7a984407f97bbd9042628 in specs. No encoder updates.

Study `voxel-distance-retention-v1`; fresh dataset
`voxel-distance-retention-v1-development-1`, 192 probe-training /48 assessment
geometries. Same four procedural families and density strata. Content hashes
must be disjoint across splits and from continuation. No unseen-family claim.

Compare old/new frozen encoders, all seeds0/1/2, on clearance and recovery NMAE.
Use the established LG1 query algorithm on CPU: streams34101/34102 for
train/assessment, 20% missingness, 256 queries per geometry; clearance queries
observed-free cells, recovery queries hidden ground-truth-free cells. Missingness
mechanism is reused; complete query banks are fresh because geometry is fresh.
Targets are crop-local positive signed distance, truncated/divided by eight.

For each encoder/task/seed, fit the fixed32-hidden SiLU probe, train-only
normalization, AdamW lr0.001/wd0.01, batch1024, 1024 updates, SmoothL1. Evaluate
final probe; no assessment selection. Clamp predictions to [0,1] consistently
with the existing distance protocol. Equal probe exposure and update budgets.

Freeze exact source/spec commits, source report hash, all six encoder file/state
hashes, geometry/query/target hashes before fitting. Verify pre/post-probe state.
One-hour limit checked before encoder fitting and after every bounded1024-update
probe fit; do not retry or expand. Identity/state errors invalidate; incomplete
seeds are inconclusive, never a pass. No weights or corpora committed.

Retention requires both tasks: paired new-minus-old error upper95% CI <=0.02,
every seed difference <=0.02, and every new seed <=0.15 clearance /0.20 recovery.
These are engineering non-inferiority criteria, not literature-established minima.
Bootstrap whole geometry within the12 family/density strata, preserve pairing,
average three seeds, 2000 draws with seed368. Report seed scores and intervals.
Passing permits new-family validation to be proposed; no promotion, topology or
radius-scaling claim follows. Old surface results remain unchanged.
