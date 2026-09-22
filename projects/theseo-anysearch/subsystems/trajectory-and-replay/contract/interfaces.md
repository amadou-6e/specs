# Trajectory and replay interfaces

This page records storage and command boundaries at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/experiments/trajectory.py` defines trajectory collection and payload
construction. `theseo_anysearch/experiments/trajectory_storage.py` owns compressed
storage, compatibility reads, selectors, and export safety.

Each replay contains initial task/world state and ordered steps with action, reward,
positions, lifecycle result, and relevant mutations. Small-world initial occupancy is
held in a sidecar; compiled-world replay carries a content-addressed reference and
sparse overlay changes.

`theseo_anysearch/cli/commands/replay.py` resolves a run artifact and launches the
`voxel-replay` binary. That binary must be built separately; the Python package alone
does not guarantee its availability. Selector names (`best`, `latest`, or iteration)
refer to trajectory artifacts, not merely run metadata.
