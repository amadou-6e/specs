# Geometry configuration boundary

Status: draft. Parent: [configuration architecture](../overview.md).

## Geometry sources

`env.geometry.sources` is the single input surface for occupancy. Source adapters may
include:

- analytic boxes;
- STL and later reviewed mesh/CAD adapters;
- URDF/SDF collision geometry;
- `.3dmap` or other explicit voxel-map formats;
- dense or sparse occupancy artifacts;
- verified Theseo world bundles through `type: world`.

Adapter-specific unit, scale, transform, padding, and member-selection settings stay
with their source entry in the main YAML. They do not move to a task file.

## Geometry generation

Procedural generation and augmentation can be inline or referenced by
`generation_file`. The generation schema owns:

- generator/provider name and parameters;
- geometry-only randomization and augmentation;
- candidate attempt budgets;
- structural bounds and geometry validity checks;
- publication of a resolved geometry/world artifact and its provenance.

It does not own start/goal selection, route-difficulty filtering, observation settings,
agent actions, rewards, or experimental roles.

## Runtime world behavior

Runtime residency settings remain in `env.geometry`, including decoded-memory bounds,
prefetch margins, and worker-local staging. These controls affect loading performance,
not immutable world identity.

Initially, a disk-backed `type: world` source is exclusive with other occupancy sources.
Support for sparse overlays or transformations requires a separately accepted identity,
mutation, and verification contract.
