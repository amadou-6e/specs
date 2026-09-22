# 33-to-65 execution

Run `voxel-context-65-v1-run1` on source `f848db6` used fresh 81-cubed parents,
nested 33/65 crops, and identical central-17 queries. Three continuation encoders were
frozen; each scale/task/seed received its own fixed 32-hidden probe. Corpus data stayed
on CPU and forward batches streamed to CUDA. Batch 4 was accepted under the registered
6 GiB allocation cap. Total recorded time was 84.797 seconds.
