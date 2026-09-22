# F-001 — Dense voxel inputs grow cubically

## Characterization

- Classification: historical project calculation
- Status: recorded
- Confidence: high that the source contains the calculation; not independently recomputed in this migration

## Finding

The predecessor records that a centered dense observation contains `(2r + 1)^3`
cells and argues that a normal dense 3D CNN is not viable at radius 512.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 provides a per-radius size table and states the excluded activation and training
costs. This migration preserved but did not independently recompute that table.

## Applicability to Model Garden

The scaling law directly constrains any Model Garden architecture consuming a full
dense cube. It does not by itself identify the best sparse or hierarchical alternative.

## Limitations and counterevidence

No target-hardware benchmark is preserved with the calculation. Kernel, dtype,
batching, compression, and streaming choices can change practical limits.

## Consequences

Large-radius candidates should be screened for hidden dense materialization and
measured against declared memory budgets.
