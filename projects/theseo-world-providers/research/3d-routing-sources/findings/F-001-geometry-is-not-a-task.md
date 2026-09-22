# F-001 — Geometry availability does not imply task readiness

## Characterization

- Classification: synthesis
- Status: supported
- Confidence: high

## Finding

An available 3D scene, mesh, voxel map, simulator, or CAD model is not by itself a
routing task. A usable task additionally requires explicit endpoints or demands,
movement and collision assumptions, checkable result semantics, and provenance.

## Supporting sources

- [S-002 — ShortestPathLab voxel benchmarks](../sources/S-002-shortestpathlab.md)
- [S-005 — Gazebo maps](../sources/S-005-gazebo-maps.md)
- [S-007 — IRIS-v2](../sources/S-007-iris-v2.md)
- [S-008 — IFC-Bench](../sources/S-008-ifc-bench.md)

## Evidence

ShortestPathLab supplies voxel maps together with task files, while Gazebo maps,
IRIS-v2, and IFC-Bench provide useful geometry but require derived routing tasks. The
existing inventories document those differing asset boundaries.

## Applicability to Theseo

Adapters must preserve geometry and task records separately. Any new endpoint, body
radius, roof, target mask, or movement constraint creates a Theseo-derived task rather
than an upstream benchmark result.

## Limitations and counterevidence

This finding classifies asset completeness. It does not rank source quality or prove
that any derived task is valid.

## Consequences

Require explicit world and task identities, provenance, and independent feasibility
validation before admitting a source to an experiment.
