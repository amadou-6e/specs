# Worlds and geometry validation

This matrix identifies checks present in product revision `72a413a` and what each can establish. The checks were inspected for this specification; **they were not run in this documentation pass**, so no current execution result is claimed.

| Contract claim | Present check and scope |
| --- | --- |
| Episodes share the same base allocation but isolate mutations | `theseo_anysearch/core/src/voxel/world/state.rs`: `shared_base_has_isolated_overlays`, `reset_clears_overlay_without_replacing_base` |
| Tombstones, updates and reinsertion produce one resolved occupancy view | `theseo_anysearch/core/src/voxel/world/state.rs`: `insert_update_tombstone_and_reinsert_resolve_correctly`, `raycast_observes_overlay_first_view` |
| Region and mutation queries return a stable, deduplicated view | `theseo_anysearch/core/src/voxel/world/state.rs`: `regional_queries_merge_without_duplicates`, `overlay_mutations_report_blocks_and_tombstones_in_stable_order`; `theseo_anysearch/core/src/voxel/world/regional_tests.rs` covers regional behavior |
| Compiled packs have stable identity and reject corruption | `tests/test_worlds/test_unit/test_compiler.py`, `test_manifest.py`, `test_artifacts.py` exercise compiler, manifest and artifact validation paths |
| Live extents respect the task-coordinate limit | `tests/test_worlds/test_unit/test_extent.py` |
| Disk residency and transformed-world paths have dedicated tests | `tests/test_worlds/test_unit/test_residency.py`, `test_transformations.py` |

These paths are relative to the product repository, not this specs checkout. The matrix is evidence of test coverage, not a claim of complete proof: no benchmark establishing memory/CPU limits for every world geometry is recorded here, and this pass did not run native or Python suites. A reviewer should also reconcile the older fixed-1000³ documentation before marking this subsystem stable.
