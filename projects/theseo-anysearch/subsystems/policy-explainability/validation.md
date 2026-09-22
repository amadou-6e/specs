# Policy explainability validation

Evidence below was inspected at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`; **none was run in this pass**.

| Area | Inspected evidence under `tests/test_rllib/test_unit/test_explain/` |
| --- | --- |
| Restore/inference smoke behavior | `test_backend_smoke.py` |
| Schema-derived grouping and metadata | `test_feature_schema.py` |
| Background selection and degeneracy rules | `test_interactive_session_background.py`, `test_service_replay_and_background.py` |
| Persistent native protocol | `test_native_bridge.py` |
| Fictional observation editing | `test_observation_editor.py` |
| DQN/PPO score terminology and values | `test_policy_scorer.py` |
| Requests, provenance, scenarios | `test_requests_and_scenarios.py` |
| Replay divergence/trace collection | `test_trace_collector.py` |
| UI artifact production | `test_ui_artifacts.py` |

CLI gating is inspected in `tests/test_cli/test_unit/test_replay_explain_gating.py`.
The principal open gap is a live VoxelEnv test for the generic trace collector after
removal of `cursor_pos`. Until that passes, legacy-fixture tests do not prove current
environment compatibility.
