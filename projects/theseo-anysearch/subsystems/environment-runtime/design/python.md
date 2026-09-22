# Python runtime responsibilities

This page follows Python execution at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

## Construction

`theseo_anysearch/settings/environment/environment.py`,
`theseo_anysearch/settings/environment/action.py`, and
`theseo_anysearch/settings/environment/lifecycle.py` validate runtime settings.
`theseo_anysearch/environments/action_spaces.py` constructs spaces and encodes actions.

## Single-agent flow

`theseo_anysearch/environments/gymnasium/base.py` provides common plumbing.
`theseo_anysearch/environments/gymnasium/voxel_env.py` owns concrete scenario
preparation, native reset/step calls, observations, reward accumulation, and results.

## Multi-agent flow

`theseo_anysearch/environments/pettingzoo/base.py` provides ParallelEnv plumbing.
`theseo_anysearch/environments/pettingzoo/multi_voxel_env.py` and
`theseo_anysearch/environments/pettingzoo/surface_env.py` own their spaces and result
adaptation.

## Lifecycle

`theseo_anysearch/environments/lifecycle.py` executes ordered Python rules after the
native transition and enforces terminal precedence in the final result.
