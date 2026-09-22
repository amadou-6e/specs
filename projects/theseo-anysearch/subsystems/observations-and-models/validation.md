# Observation and model validation

The following evidence was inspected at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`; **none was executed in this pass**.

| Guarantee | Inspected evidence |
| --- | --- |
| Observation keys, shapes, and removed-field absence | `tests/test_environments/test_unit/test_environments.py` |
| Single-agent mode conversion | `tests/test_environments/test_integration/test_voxel_env_obs_modes.py` |
| Radial distance/kind semantics | `tests/test_environments/test_integration/test_voxel_env_observations_radial.py` |
| CNN spatial and auxiliary assembly | `tests/test_rllib/test_unit/test_cnn_models.py` |
| Model registration and output contracts | `tests/test_rllib/test_unit/test_models.py` |
| RLlib integration of CNN models | `tests/test_rllib/test_integration/test_cnn_models_ray.py` |

The `test_cnn_models.py` fixture contains legacy `steps_remaining` and `cursor_pos`
keys. It proves arbitrary auxiliary handling, not that live environments emit those
fields. Explainability schema tests additionally inspect categorical metadata at a
consumer boundary.

Gaps include unexecuted tests, incomplete single/multi-agent parity characterization,
and no confirmed live-environment test for the generic explainability trace collector's
cursor dependency.
