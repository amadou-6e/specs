# Environment runtime interfaces

This page describes framework-facing calls at audited product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`. Paths are relative to the product root.

## Gymnasium

`theseo_anysearch/environments/gymnasium/voxel_env.py` implements `VoxelEnv` above
`theseo_anysearch/environments/gymnasium/base.py`.

- `reset(...) -> (observation, info)` initializes one episode.
- `step(action) -> (observation, reward, terminated, truncated, info)` advances it.
- `action_space` and `observation_space` declare accepted and returned values.
- An optional action mask follows the selected action mode's index ordering.

The concrete override is authoritative where it is more specific than the base class;
the base wrapper alone does not describe the complete reset lifecycle.

## PettingZoo

`theseo_anysearch/environments/pettingzoo/multi_voxel_env.py` and
`theseo_anysearch/environments/pettingzoo/surface_env.py` build on
`theseo_anysearch/environments/pettingzoo/base.py`. Reset and step return per-agent
mappings; step accepts an action mapping. Agent-specific spaces permit heterogeneous
agents. Consumers must not flatten this into the Gymnasium tuple contract.

## Native boundary

Bindings under `theseo_anysearch/core/src/bridge/python/environments/` translate
Python values and native result DTOs without redefining transition semantics. Actions
are centralized in `theseo_anysearch/environments/action_spaces.py`; native execution
lives in `theseo_anysearch/core/src/voxel/environment/single/action_pipeline.rs` and
`theseo_anysearch/core/src/voxel/environment/multi_action_execute.rs`.

Lifecycle results include `termination_reason` when an episode ends and may include
reward breakdown, scenario metadata, and extension diagnostics.
