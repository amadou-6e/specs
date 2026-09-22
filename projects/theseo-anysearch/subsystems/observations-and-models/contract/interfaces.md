# Observation and model interfaces

This page identifies the live policy-facing shapes at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`. The authoritative settings schema is
`theseo_anysearch/settings/environment/observation.py`.

| Mode | Policy-facing content | Interpretation |
| --- | --- | --- |
| `scalar` | optional goal fields only | Without goal conditioning the mapping is empty |
| `box` | local voxel-kind tensor | Each kind is normalized by division by 5 |
| `radial` | ray hit distances and hit kinds | Distances and categorical kinds are normalized separately |
| `hierarchical_box` | concatenated boxes at configured radii | Retains local spatial structure at each scale |

`theseo_anysearch/environments/gymnasium/voxel_env.py` declares spaces in
`_observation_space`, allocates reusable arrays in `_init_obs_cache`, and converts
native data in `_obs_to_numpy`. Native observation DTOs are bridged in
`theseo_anysearch/core/src/bridge/python/environments/voxel/observation.rs`.

Multi-agent observations from
`theseo_anysearch/environments/pettingzoo/multi_voxel_env.py` instead expose a local
grid, six face neighbors, ray features, and optional goal fields. Stale docstrings that
mention cursor position do not override declared spaces and tests.

Models are registered through `theseo_anysearch/rllib/models/models.py`. Base feature
assembly and masking live in `theseo_anysearch/rllib/models/base.py`; convolutional
encoders live in `theseo_anysearch/rllib/models/cnn.py`.
