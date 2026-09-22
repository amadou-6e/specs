# Replaying a recorded episode

This guide helps a user find and open an existing trajectory. It assumes a completed
run with trajectory capture enabled and a separately built `voxel-replay` binary. The
expected result is an interactive viewer showing the selected episode and its world.

1. Locate the run output printed by training and confirm it contains a replayable
   trajectory, not only run metadata.
2. Invoke the replay command implemented by
   `theseo_anysearch/cli/commands/replay.py`, selecting `best`, `latest`, or a specific
   iteration according to its CLI help.
3. If the payload references a compiled world, keep the referenced content-addressed
   world cache available to the viewer.
4. Use viewer controls to scrub/play frames and adjust camera or regional display;
   these controls do not mutate the trajectory.

If loading reports corruption for an existing `.json.zst`, repair or regenerate that
artifact. Renaming an older `.json` file to encourage fallback is unsafe because the
loader intentionally refuses stale fallback. For deterministic visual diagnosis, use
the headless capture path and compare complete windows at known replay steps.
