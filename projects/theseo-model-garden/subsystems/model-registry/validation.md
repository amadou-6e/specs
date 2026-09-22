# Model-registry validation

This page maps the implemented registry contract to concrete checks and separates
tests present in the repository from validation actually run during this
specification pass.

## Contract-to-check map

| Guarantee or behavior | Current check | What it proves |
|---|---|---|
| Saving writes all four package files | `TestGardenStoreSave.test_save_creates_files` in `tests/test_garden/test_unit/test_garden_store.py` | Full and encoder states, metadata, and loss history exist |
| Tagged packages use a tag directory | `test_save_with_tag` | `name/tag/encoder.pt` is created |
| Core metadata and loss history round-trip | `test_meta_contents`, `test_loss_curve_saved`, `TestGardenStoreMeta` | Selected fields and curve values are readable |
| Existence and listing work for tagged and untagged packages | `TestGardenStoreExists`, `TestGardenStoreListModels` | Directory scanning recognizes saved packages |
| Registered name and `name:tag` resolve | `TestGardenStoreResolveRef` | Valid aliases resolve and unknown names/tags reject |
| Config aliases are local and replaceable | `TestConfigRegistry` | Register, resolve, overwrite, and stale-path behavior |
| Run-source metadata round-trips | `TestGardenStoreRunRegistry` | `runs.json` registration and empty behavior |

All referenced checks are in
[`tests/test_garden/test_unit/test_garden_store.py`](https://github.com/amadou-6e/theseo-anysearch/blob/49fef5f4f9d3fb21325931e1ce1eed89e743cdcc/tests/test_garden/test_unit/test_garden_store.py).

## Validation run for this review

The specification was reconciled against implementation revision
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`. The focused store test command and specs
validator results should be recorded in the review handoff; this document does not
claim an unexecuted suite passed.

## Missing coverage

The present unit suite does not establish:

- compatibility between a saved package and `PretrainedVoxelModel` end to end;
- built-in preset registration, explicit-path resolution, or Windows drive-letter
  parsing;
- behavior under malformed YAML/JSON, corrupt or mismatched checkpoints, interrupted
  writes, or concurrent writers;
- that global alias registration points to the intended tagged and untagged release
  after repeated saves;
- integrity, content identity, schema migration, or immutable publication; or
- any gate in the proposed certification plan.

Certification evidence must remain attached to the relevant experiment and artifact.
Passing a research gate does not promote a package because the current store has no
implemented promotion state.
