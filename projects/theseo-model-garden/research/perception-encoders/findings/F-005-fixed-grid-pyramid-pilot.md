# F-005 — A fixed-grid multiresolution residual encoder was recommended for the first scalable pilot

## Characterization

- Classification: historical recommendation
- Status: proposed
- Confidence: medium as a faithful reconstruction; unknown technical merit

## Finding

The predecessor recommends first piloting a shared residual encoder over several
centered fixed-size grids sampled at power-of-two strides, with conservative
aggregation and bounded per-scale tensors.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 specifies candidate E and a detailed `voxel_pyramid_resnet_3d` proposal,
including scale construction, backbone, fusion outputs, and capacity families.

## Applicability to Model Garden

The proposal uses ordinary dense operations and a fixed output contract, which could
simplify registry integration relative to specialized sparse kernels.

## Limitations and counterevidence

S-001 explicitly calls the design an engineering hypothesis and notes thin-barrier,
shared-weight, aggregation, and construction-cost risks. No completed benchmark is
part of this topic.

## Consequences

If revived, implement the smallest pilot and matched controls before broader capacity
or radius scaling.
