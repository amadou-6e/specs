# Rust explainability responsibilities

This page describes native viewer integration at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/core/src/replay/explain.rs` manages explanation state and communication
with the persistent Python JSONL bridge. `theseo_anysearch/core/src/bin/voxel_replay.rs`
integrates the controls and artifacts into replay. Rust presents schema-derived fields
and results; it does not reinterpret logits as Q-values or perform policy attribution.
