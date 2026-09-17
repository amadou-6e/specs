# F-001 — Sparse hierarchies avoid allocating uniform regions voxel by voxel

## Characterization

- Classification: source claim
- Status: supported
- Confidence: high

## Finding

OpenVDB represents sparse volumetric values with a hierarchy that can store tiles and
background values instead of allocating every voxel independently.

## Supporting sources

- [S-001 — OpenVDB overview](../sources/S-001-openvdb-overview.md)

## Evidence

The official overview describes the tree hierarchy and its voxel, tile, and background
value representations. This finding reports that documented property; it does not
claim a Theseo benchmark result.

## Applicability to Theseo

The representation is relevant when comparing sparse world-storage approaches. It
does not establish that OpenVDB is the correct dependency or that it outperforms
Theseo's current chunked storage for Theseo workloads.

## Limitations and counterevidence

No Theseo workload, memory profile, mutation pattern, or Python/Rust integration was
benchmarked for this finding.

## Consequences

Use this property as one input to a storage comparison. Require a separate experiment
before making an implementation decision.
