# S-001 — OpenVDB overview

## Material

- Canonical URL: [OpenVDB overview](https://www.openvdb.org/documentation/doxygen/overview.html)
- Owner: Academy Software Foundation OpenVDB project
- Publication date: not stated on the inspected page
- Version or revision: rolling official documentation; no immutable revision pinned
- Accessed: 2026-09-17
- Source type: official technical documentation
- Evidence class: primary
- Rights or license: not established by this record
- Local artifact hash: none; inspected online

## Relevance

The overview documents the sparse hierarchy, coordinate spaces, transforms, grids,
and value representations used by OpenVDB.

## Material inspected

The overview sections describing the tree, root/internal/leaf hierarchy, sparsity,
and voxel, tile, and background values were inspected. No source checkout or runtime
benchmark was performed for this record.

## Claims used

- The hierarchy can represent sparse volumetric values without storing every voxel as
  an independent value.

## Reliability and limitations

This is authoritative for documented OpenVDB design, but it does not independently
verify performance and does not characterize Theseo integration costs.

## Related findings

- [F-001](../findings/F-001-sparse-hierarchy.md)
