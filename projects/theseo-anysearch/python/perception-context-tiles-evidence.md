# Frozen tiled spatial coverage evidence

Issues specs#51 / theseo-anysearch#376. Protocol commit
76bb3c403fb36b30ebf5335dcbc8f77005cf2db4; source c4f1787.
Run voxel-context-tiles-v1-run1,51.812 seconds including preparation. No fits.

All four noninferiority checks pass versus both dense controls. Same-head
comparison: surface gain intervals cross0; clearance/recovery improve about.0022.
Tiled versus adapted65 head: all four pilot intervals positive (not adjusted for
multiple comparisons). Tiled boundary F1 .6905/.6838/.7021; sampled central49,
not exhaustive output. Source heads, thresholds and normalization unchanged.

Dense65 encoder coverage21.8-23.5 ms/scene,176.60 MiB allocated peak. Tiled33
96.9-104.7 ms/scene,112.19 MiB. Tiling is4.1-4.8 times slower for36.5% lower
allocation; retain as memory option, not speed/default deployment. Profiles
exclude transfer, heads and stitching; no device-total or radius512 extrapolation.
Prefer dense where memory fits and retain shared frozen weights/33-context heads.

Implementation docs/perception-context-tiles-assessment.md and
docs/perception-encoder-local-geometry/tiles-report.json contain full evidence.
Report SHA2560923d9216166f5e2e9ef259a68b7f1723f1d848e4b5486e9d6830dcb8e740ed2.
Fresh parents disjoint from context65 corpus;36 prediction artifacts hashed.
Full garden418 passed before extra evidence replay test. No merges, promotion,
topology or planning claims. Disposition retain.
