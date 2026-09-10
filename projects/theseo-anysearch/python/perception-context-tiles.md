# Frozen tiled spatial coverage diagnostic

Issues specs#51 / theseo-anysearch#376. Authorized unmerged stack on #374/specs#49.
Prior protocol2f9fa46f3c26f96b9f0e1c05f9fa101a09923ad3. Local-geometry only.

## Contract

Study `voxel-context-tiles-v1`, run `voxel-context-tiles-v1-run1`. Generate48 fresh81
parents using context65 generators, family/density order and parent-target rules.
Scene IDs `voxel-context-tiles-v1-data-assessment-<index:03d>`; mask20%, same SHA
seeding convention, no redrawing. Extract central65 input; sample256 eligible
queries/task in central49, RNG37600, replacement only in nonempty small pools.
Reject duplicate parents and family binary class support below20 each. Distance
targets use parent EDT truncation/divisor8; occupancy/boundary hidden, clearance
visible free, recovery hidden free. No new training or selection data or fits.

Reuse all three continuation encoders and all24 probes from context65 run1.
Verify report payload, probe file hashes, encoder states, and freeze source/spec,
new input/query/target hashes before assessment. Reuse saved train normalization
and selected thresholds without changes. Three arms: tiled33 with head33, dense65
with head33, dense65 with head65. All weights fixed throughout.

Tiling:27 cubes of side33 with axis starts0/16/32 in the65 input. Emit cores
starting8,24,40: first two ownership intervals16 voxels, last17; union is central49
(indices8..56). For query coordinate q in0..48 use tile min(q//16,2), local
coordinate q+8-16*tile. No blending/padding, minimum8-voxel halo. Process4 tiles
per CUDA batch, final3. Dense arm processes one65 scene. Stream one scene at a
time, return only queried features to CPU; retain no full-corpus CUDA tensors.
This tests sampled wider-spatial output, not every voxel's prediction accuracy.

Profile encoder forwards for complete spatial coverage (all27 tiles versus
one65) on the first scene for each encoder:3 warmups,10 timed repeats, synchronize
CUDA; record latency/scene and allocated/incremental peak. Inputs resident for
profiles, input transfer/head/stitching costs excluded. Dense emits more edge
features; compare both methods covering the same central49, state redundant
compute rather than normalize it away.6 GiB allocated cap, no batch search;
resource failure yields resource_limited, no quality conclusion. Profiles precede
assessment. Same deterministic float32/no TF32 configuration as context65.
Overall3600 seconds including manifest preparation, checked per scene.

## Assessment

Two primary paired comparisons: tiled33/head33 versus dense65/head33 (tiling),
and tiled33/head33 versus dense65/head65 (deployment alternative). Also report
dense65/head33 versus dense65/head65 (head sensitivity). Whole-parent bootstrap
within six strata, seed372,2000 draws; unchanged .03/.02 noninferiority margins.
Report each task/seed and family. These intervals are pilot diagnostics, not
multiplicity-adjusted certification. No parameter selection from assessment.

If tiled quality passes and latency improves, retain as efficiency candidate.
If quality passes but latency worsens and memory drops, retain only as a
memory-limited option, not a speedup. If any task fails, diagnose halo/norm effects
under a new protocol before adoption. Prefer the simpler dense path where memory
fits unless benefits are demonstrated. No larger-radius extrapolation, full-volume
certification, topology or planning claim, integration merge or promotion.
