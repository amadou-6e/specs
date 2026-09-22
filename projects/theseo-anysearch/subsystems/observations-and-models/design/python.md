# Python observation and model responsibilities

This page follows the live Python path at audited product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/settings/environment/observation.py` validates observation mode,
radii, rays, and goal-field selection. `theseo_anysearch/environments/gymnasium/voxel_env.py`
declares spaces, allocates buffers, and converts native values to normalized `float32`
arrays. `theseo_anysearch/environments/pettingzoo/multi_voxel_env.py` owns the separate
multi-agent schema.

`theseo_anysearch/rllib/models/base.py` separates `local_grid`, auxiliary keys, and
`action_mask`. `theseo_anysearch/rllib/models/cnn.py` owns the spatial encoder and
heads, while `theseo_anysearch/rllib/models/models.py` exposes registered model names.
Optional pretrained packages live under `theseo_anysearch/garden/` and must conform to
the extension contract before loading.
