# F-004 — Sparse and hierarchical processing remain candidates

## Characterization

- Classification: historical cross-source synthesis
- Status: unverified
- Confidence: low pending source-by-source reassessment

## Finding

The predecessor concludes that sparse or hierarchical spatial processing is more
plausible than one full dense cube for large radii, while recording substantial
semantic, batching, portability, and implementation risks.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 compares sparse CNN, octree, point, tri-plane, and implicit-field families and
links representative literature. That literature was not independently inspected in
this migration.

## Applicability to Model Garden

The candidate families inform future feasibility work, dependency review, and baseline
selection.

## Limitations and counterevidence

There is no preserved direct validation over Theseo's full radius range, occupancy
semantics, supported operating systems, or deployment hardware.

## Consequences

No sparse backend or hierarchical family should be adopted from this finding alone.
Each requires a bounded prototype and explicit portability evidence.
