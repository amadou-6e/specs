# Rust replay responsibilities

This page maps native viewer components at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/core/src/bin/voxel_replay.rs` owns application startup and UI
execution. `theseo_anysearch/core/src/replay/storage.rs` loads trajectory artifacts;
`regional.rs`, `render_cache.rs`, `overview.rs`, and `lod.rs` bound and cache geometry
for rendering. `live.rs` handles live state, while `explain.rs` integrates optional
explanation data.

The native layer owns replay cursor/frame state, world-reference resolution, surface
extraction, camera projection, depth behavior, minimap/overview, and headless frames.
It must apply overlays in recorded order and preserve task/storage coordinate
conversion.
