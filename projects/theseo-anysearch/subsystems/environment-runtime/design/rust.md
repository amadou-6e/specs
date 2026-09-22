# Rust runtime responsibilities

This page maps native transition ownership at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/core/src/voxel/environment/single/action_pipeline.rs` executes a
single-agent native action. `theseo_anysearch/core/src/voxel/environment/single/lifecycle.rs`
distinguishes termination from maximum-step truncation and emits reasons.

`theseo_anysearch/core/src/voxel/environment/multi.rs` owns multi-agent state, while
`theseo_anysearch/core/src/voxel/environment/multi_action_execute.rs` coordinates
actions against shared state. It is a separate native path, not a Python loop around
the single-agent wrapper.

Bindings under `theseo_anysearch/core/src/bridge/python/environments/` expose native
construction and results. They must preserve action ordering, flags, diagnostics, and
errors exactly.
