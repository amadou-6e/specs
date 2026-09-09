# Encoder continuation and retention evidence

Implementation issues#366/#368; specification issues#41/#43. No merges/promotion.

Three new same-architecture encoders completed2048 joint occupancy/ESDF updates.
At matched192-geometry probe exposure, boundary F1 rose from0.6343/0.6129/0.6239
to0.7380/0.7328/0.7374. Paired loss improvement CI[0.04678,0.06215].
Surface protocol4349ad2ac47cbad912a7a984407f97bbd9042628, source2423714.
Report payload3756d04628a9c6e377e9ae67853ac440fe4afeae46ae4160ea064d8965710390.

Fresh frozen-distance validation also completed: clearance errors new
0.0308/0.0320/0.0361 versus old0.0487/0.0492/0.0512; recovery new
0.0309/0.0324/0.0360 versus old0.0485/0.0503/0.0504. Both pass the preregistered
retention rule and have negative paired new-minus-old error intervals.
Retention protocol762262d657b4320dbce39d3b53bc028105a2896b, source577da2e.
Report payload01c0be1f42549c7c6a4638638e8a5a48120f3f3daee1c0d6a41098ad119bf577.

Retain new encoders as local-geometry candidates for new-family validation.
Architecture/probe exposure matched, pretraining histories did not. Old LG2 also
used dynamic masks; these results do not isolate a single pretraining factor.
No unseen-family, topology, occupancy-retention, planning or radius claims.
Full implementation assessments: docs/perception-encoder-continuation-assessment.md
and docs/perception-distance-retention-assessment.md. Weights remain untracked.
