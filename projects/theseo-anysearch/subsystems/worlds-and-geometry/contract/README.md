# Worlds and geometry contract

This contract describes the occupancy view delivered to consumers and the conditions under which a compiled world can be reused. It does not assert that route endpoints are reachable: that is a task/environment concern. Statements reflect product revision `72a413a`.

## Coordinates and extent

Compiled-world storage coordinates are zero-based `u32` tuples with explicit extent and schema in the manifest. Environment-facing task coordinates are one-based. Conversion must be explicit at the boundary; equal numeric tuples from those two spaces do not necessarily identify the same voxel. Live environment construction rejects axes above 65,535 through `resolve_task_extent`, even though the artifact coordinate type is wider (`theseo_anysearch/worlds/manifest.py`, `theseo_anysearch/worlds/extent.py`). The old assertion that all worlds are fixed at 1000³ describes the legacy default, not compiled-world capacity.

## Resolved occupancy

`WorldState` exposes one resolved view: an overlay block replaces its base value, a tombstone makes a base block absent, and a coordinate without an overlay entry reads from the immutable base. Region queries merge those layers without duplicate coordinates and return stable order. Raycast uses the same resolved occupancy view. `clear()` removes only per-episode mutations; it neither copies nor reinserts base geometry. Replacing the base creates a new backend instead of mutating a base shared through `Arc` (`theseo_anysearch/core/src/voxel/world/state.rs`).

The default legacy state is chunked with chunk edge 32; a compiled pack may instead use a disk-backed backend with a bounded decoded-byte cache. Prefetch and pinning are residency mechanisms, not a different occupancy truth: a cold read remains correct even if it must synchronously load a chunk (`state.rs`, `disk_backed.rs`).

## Compiled artifact admission

The compiler accepts typed box, NPY and STL sources. Its identity includes schema, coordinate type, extent, compiler settings, overview settings, candidate-index mode and source *content* hashes rather than machine-local paths. A complete cached entry is reused only after validation. New entries are assembled in a temporary location, validated, and atomically published while a cache-key lock serializes competing compilers. Corrupt entries are quarantined and rebuilt only if inputs remain available; otherwise the compiler raises `WorldPackUnavailableError` (`theseo_anysearch/worlds/compiler.py`).

Validation checks the completion marker, identity contract, pack checksum, overview and candidate indexes, chunk-index consistency, and optionally every chunk checksum and decode. An existing path alone is not evidence that a pack is valid (`compiler.py`).

## Scope and open questions

Geometry validation can test candidate placement and task feasibility before an environment is admitted, but the world store itself does not promise navigability. The separate provider contract governs downloaded/generated bundles. Large-world memory and throughput depend on chunk shape, occupancy distribution, and access pattern; this contract promises bounded queries and cache limits, not constant work for arbitrary queries. The older imported [voxel](../../../rust/voxel-spec.md) and [world](../../../rust/world.md) documents still require supersession review where they conflict with these current implementation facts.
