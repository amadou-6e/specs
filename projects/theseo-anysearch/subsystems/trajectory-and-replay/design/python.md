# Python trajectory responsibilities

This page follows capture and storage at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/experiments/trajectory.py` collects episode state, ranks buffered
episodes, and builds small- or compiled-world payloads.
`theseo_anysearch/rllib/trainer/reporting/trajectories.py` schedules snapshots and
best-so-far output. `theseo_anysearch/experiments/trajectory_storage.py` validates
finite values, compresses, atomically publishes, reads compatibility formats, and
resolves selectors. `theseo_anysearch/cli/commands/replay.py` maps user selection to
the native viewer invocation.
