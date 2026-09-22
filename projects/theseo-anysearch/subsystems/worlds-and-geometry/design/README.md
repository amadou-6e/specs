# Worlds and geometry design

This page explains how the native occupancy view and offline compiler realize the [contract](../contract/README.md). Paths below are relative to the `theseo-anysearch` product repository at revision `72a413a`.

## Runtime read path

`theseo_anysearch/core/src/voxel/world/state.rs` holds a `WorldHandle` with an `Arc` immutable backend and a `WorldState` overlay owned by one episode. Reads check the overlay first, then the base; overlay tombstones suppress base blocks. Bounded-region reads combine both layers and sort the result. Reset clears only the overlay, so sharing the base does not share episode mutations. Replacing geometry constructs another backend and swaps its handle, preserving isolation from other holders.

The backend can be a chunked resident world or a compiled-pack-backed world. `theseo_anysearch/core/src/voxel/world/disk_backed.rs` manages decoded chunks and cache pressure; residency pinning keeps required chunks in memory across an operation. Prefetch is useful for this backend, while a cache miss can still load synchronously. This favors correctness for teleports or unexpected access over an unconditional no-I/O step guarantee.

## Offline compile and admission

`theseo_anysearch/worlds/compiler.py` converts `BoxSource`, `NpySource` and `StlSource` into a pack, chunk index, manifest, overview, candidate index and completion marker. It computes a content-derived identity before cache lookup, acquires a per-key lock, and validates any cached hit. For a miss, it writes into a temporary directory, validates its own output, then publishes by rename. `theseo_anysearch/worlds/manifest.py` owns the versioned schema and coordinate declaration; `theseo_anysearch/worlds/extent.py` enforces the narrower live-task coordinate limit.

`theseo_anysearch/settings/environment/geometry.py` defines typed source and compiled-world settings, including cache and prefetch controls. Configuration chooses sources or an existing compiled artifact; it does not change the overlay resolution rule. `theseo_anysearch/cli/commands/geometry.py` exposes geometry tooling, whereas `theseo_anysearch/cli/commands/worlds.py` addresses provider bundles and is not a second compiler authority.

## Boundaries and trade-offs

The immutable base plus mutable overlay avoids base copies at reset and allows cheap episode isolation, at the cost of resolving two layers for a read. Chunked or disk-backed access avoids dense-world materialization but makes locality and cache sizing consequential. Content-addressed compilation improves cross-machine reuse; exact artifact integrity checks add admission cost and intentionally fail closed when corrupt data cannot be rebuilt. Task reachability remains outside this storage design.
