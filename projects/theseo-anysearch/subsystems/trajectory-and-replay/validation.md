# Trajectory and replay validation

Evidence below was inspected at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`; **none was executed in this pass**.

| Guarantee | Inspected evidence |
| --- | --- |
| Selection, payloads, compiled references, and round trips | `tests/test_experiments/test_unit/test_trajectory.py` |
| Atomic cleanup, corruption precedence, finite rejection, compatibility selectors, and no-overwrite export | `tests/test_experiments/test_unit/test_trajectory_storage.py` |
| Policy inference capture | `tests/test_experiments/test_unit/test_trajectory_policy_inference.py` |
| Integrated trajectory production | `tests/test_experiments/test_integration/test_trajectory_integration.py` |
| CLI replay/explanation gating | `tests/test_cli/test_unit/test_replay_explain_gating.py` |
| Native storage, regional, cache, overview, LOD, and explanation behavior | tests embedded under `theseo_anysearch/core/src/replay/` |

Visual behavior additionally requires headless/full-window capture comparison; code
tests alone do not validate reviewed UI geometry. Relevant performance evidence is in
`docs/benchmarks/regional-replay.md` and `docs/benchmarks/lod-replay.md`, but it was not
rerun for this audit.
