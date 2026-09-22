# Trajectory and replay design

Python captures and publishes a compact, framework-independent episode record. Rust
loads that record, resolves referenced geometry, maintains replay state, and renders
frames. This keeps training processes free of an interactive renderer and lets the
viewer read local artifacts independently.

For large worlds, immutable base geometry remains content-addressed while each replay
stores only overlay deltas. Regional loading, surface caching, overview geometry, and
LOD keep visualization bounded by the viewed region rather than total world extent.
Those mechanisms do not promise arbitrary dense-world GPU throughput.

Atomic publish protects readers from partial writes. Strict corruption precedence
avoids showing a stale legacy episode when a newer compressed artifact is broken.
Whole-document decompression simplifies random scrubbing but uses memory proportional
to trajectory length.

See [Python](python.md) and [Rust](rust.md) responsibility maps.
