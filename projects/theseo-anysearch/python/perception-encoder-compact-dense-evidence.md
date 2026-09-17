# Dense compact learnability evidence

Specs#60 / implementation#386; protocolfd8eba978a6100b997cc762dbea6078d3b0f5686,
source2afe8f0. Run compact-dense-v1-run1,76.765s.1024 full-grid updates per arm.
Learned table128 and actual voxel encoder128 reach IoU/F1=1 already at128 updates.
Oracle6 reaches.9223/.9596, below frozen .95/.97 targets. Preserve all outcomes.

The actual compact training path can memorize four scenes; no generalization,
hidden-only quality, efficient deployment-head or HPO-winner claim follows.
Different head structure/LR/exposure prevent an isolated causal comparison to
query decoder fits. Proceed to fresh multi-scene training and independent frozen
readouts. User approved up to48 GPU-hours for the campaign on2026-09-12; no merges.
449 garden tests passed. Full report docs/perception-compact-dense-assessment.md
in implementation repository; machine payload
ab01e6a66c5c83969149f8ba9bbfdd2df3eff28f7b2b25f4573b7b5f19939e96.
Disposition retain engineering direction; no certification or promotion.
