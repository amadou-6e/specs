# F-006 — Geometry-aware objectives were recommended for pretraining

## Characterization

- Classification: historical recommendation
- Status: proposed
- Confidence: medium as a faithful reconstruction; effectiveness unverified

## Finding

The predecessor recommends truncated distance prediction, mask-aware semantic
occupancy reconstruction, physically aligned cross-scale consistency, and selected
planning-aware auxiliary probes rather than relying on raw occupancy reconstruction.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 describes the objective semantics, masking constraints, correspondence rules,
and disposable auxiliary heads. This migration did not inspect or reproduce the cited
precedents.

## Applicability to Model Garden

These objectives could test whether the latent retains boundaries, clearance,
connectivity, and multiscale correspondence needed by downstream consumers.

## Limitations and counterevidence

Loss weighting, label generation cost, leakage risk, negative transfer, and dataset
coverage remain unresolved. A reconstruction objective can score well without
supporting navigation.

## Consequences

Objective combinations should be ablated against raw-grid, random-feature, and simpler
pretraining controls.
