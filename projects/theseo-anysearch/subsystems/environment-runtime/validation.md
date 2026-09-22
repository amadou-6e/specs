# Environment runtime validation

This page maps guarantees to evidence inspected at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`. **None of these tests was run during this
documentation pass.**

| Guarantee | Inspected evidence | Coverage |
| --- | --- | --- |
| Lifecycle outcomes remain distinct | `tests/test_environments/test_integration/test_task_contract.py` | In-progress, success, step limit, and collisions |
| Scenario reset preserves lifecycle state | `tests/test_environments/test_integration/test_scenario_lifecycle.py` | Selection, reset, metadata |
| Concrete Gymnasium behavior matches spaces | `tests/test_environments/test_integration/test_voxel_env_core.py` | Construction, reset, step, spaces |
| Reward totals retain diagnostic breakdown | `tests/test_environments/test_integration/test_voxel_env_goal_reward_chain.py` | Goal reward composition |
| Python lifecycle order and precedence hold | `tests/test_environments/test_unit/test_lifecycle.py` | Hook ordering and final flags |
| Action mappings are stable | `tests/test_environments/test_unit/test_action_spaces.py` | Cardinalities and conversions |
| Heterogeneous agents retain distinct contracts | `tests/test_environments/test_integration/test_heterogeneous_multi_voxel.py` | Multi-agent spaces and execution |
| Native backends agree | `theseo_anysearch/core/src/voxel/environment/single/tests.rs` | Results, masks, native lifecycle |

## Gaps

- No Python, Rust, or bridge test was executed in this pass.
- No single indexed test compares every framework result field with its native source.
- `SurfaceEnv` has less inspected evidence than the other variants.
- Native predicate failure evidence should be indexed by exact test function in a
  subsequent audit.
