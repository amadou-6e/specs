# Policy explainability design

The service restores the saved RLModule and authoritative spaces, resolves a state
source, validates or replays it, selects steps, computes policy scores, perturbs grouped
features against a declared background, and publishes a report. This order ensures
attribution uses the same preprocessing and inference path as evaluated behavior.

Feature grouping is schema-aware and deliberately coarser than individual-voxel
attribution. It produces tractable diagnostics but cannot isolate interactions within
a group. Background choice is explicit because zero/open semantics and empirical trace
semantics answer different questions.

Python owns restoration, scoring, validation, attribution, and artifact output. Rust
owns viewer integration and communicates with a persistent Python service over JSONL,
avoiding model reinitialization for every UI action.

See [Python](python.md) and [Rust](rust.md) responsibility maps.
