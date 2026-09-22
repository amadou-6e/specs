# World-provider validation

Evidence below is present in `theseo-anysearch` `origin/develop` revision `72a413a`. I inspected implementation and test sources for this documentation update; I did **not** run the product test suite from the older root checkout. Test presence and a past report are not a fresh test pass.

| Guarantee or boundary | Current check | What it establishes |
| --- | --- | --- |
| Optional provider discovery and parameter schema | `tests/test_world_providers/test_world_providers.py::test_broken_optional_provider_does_not_break_builtin_list`, `test_provider_parameter_bounds_and_remote_catalog`, `test_provider_parameter_schema_rejects_non_numeric_bounds` | Broken entry points do not hide the built-in; declared parameters are constrained. |
| Deterministic fixture and admitted bundle with PNGs | `test_fixture_is_deterministic_and_has_checked_pngs`, `test_cli_lists_and_generates` | The built-in example is repeatable and the CLI reaches verified output. |
| Changed geometry/source/preview rejection | `test_changed_occupancy_is_rejected`, `test_changed_local_source_or_preview_is_rejected`, `test_preview_failure_never_marks_world_verified` | Reopening detects mutations and preview failure withholds verified status. |
| Training attachment and revalidation | `test_add_produces_loadable_config_and_is_idempotent`, `test_add_rejects_conflicting_geometry_and_split`, `test_loader_rechecks_world_after_manual_yaml_or_artifact_edit`, `test_same_study_second_yaml_cannot_reassign_root_to_test`, `test_same_study_rejects_different_split_record` | Config conflict and identity checks operate on actual YAML/artifacts, not only registry metadata. |
| Bounded source cache | `tests/test_world_providers/test_source_cache.py::test_verified_download_and_offline_reuse`, `test_manifest_paths_rejected`, `test_missing_offline_cache`, `test_invalid_download_never_published`, `test_max_file_bytes_up_to_32_mib_is_accepted`, `test_max_file_bytes_above_32_mib_is_rejected` | Hash, path, offline, and size constraints. |
| IFC-Bench task rotation and admission | `tests/test_world_providers/test_ifcbench_provider.py::test_seed_rotates_task_order_deterministically`, `test_report_task_order_matches_rotated_sidecar_files_and_is_validated`, `test_zero_tasks_never_published` | Provider-specific task order and result admission; not a claim of arbitrary benchmark generality. |

Relevant additional suites are `test_cavedrone_provider.py`, `test_gazebo_provider.py`, and `test_aerialgym_provider.py`. A focused product check from a checkout of `72a413a` is `python -m pytest tests/test_world_providers`; this document does not claim that command was run here. The specs validator checks document structure/links, not world-provider runtime behavior.

## Missing or narrower evidence

- No observed test establishes atomic whole-bundle publication after provider or preview failure; implementation writes to the final output directory.
- The tests above do not establish bounded memory for very large provider occupancy arrays; `theseo_anysearch/world_providers/bundle.py` deliberately loads the complete array.
- Remote catalog safety is bounded by schema/HTTPS/size checks, but catalogue entries are metadata and not provider integrity verification.
- Current `worlds add` tests cover the one-training-world path, not selectable tasks, non-training roles, or multi-world study updates; those paths are rejected or absent in implementation.
- Real-data validation for IFC-Bench was reported in PR #492, but this entry does not treat that report as a fresh local replay. Independent solid-space verification belongs to the IFC adapter's evidence, while the provider-neutral admission check verifies swept paths against voxel cubes.
