# Trajectory and replay contract

This page defines recording, persistence, selection, and replay guarantees. It does
not define environment correctness or the meaning of evaluation metrics.

Trajectory payloads contain finite values only. A completed write is compressed zstd
JSON (`.json.zst`) published atomically through a sibling temporary file, flush/fsync,
and replace. Interrupted temporary files do not become completed trajectories.

Readers accept both legacy `.json` and compressed files. If a selected compressed file
exists but is corrupt, loading fails; it must not silently fall back to a stale legacy
file. Legacy files remain readable and are not rewritten or deleted automatically.

Small-world payloads and compiled-world payloads are different encodings. Compiled
world schema v2 stores the immutable world identity/reference and sparse overlay
mutations, never a full enumeration. Both reconstruct ordered replay frames, but they
must not be described as byte- or schema-identical.

Selectors resolve best, latest, or a requested iteration deterministically from run
artifacts. Metadata alone is not replayable. The viewer loads the document into memory
for scrubbing; trajectory playback is not streaming even when world geometry is loaded
regionally.

Replay/explanation integration is optional and gated. Unsupported/corrupt payloads,
missing world references, and invalid finite-value constraints fail explicitly.
