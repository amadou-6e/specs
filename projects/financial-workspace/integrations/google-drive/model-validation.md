# Validation

## Structural preservation

| Check | Expected result |
| --- | --- |
| Concrete hierarchy is modeled | `views/folder-topology.md` contains both the dated implemented remote tree and target tree |
| Historical claims are dated | Remote topology is explicitly scoped to 2026-09-13 and never presented as current without a new inventory |
| Stable identity survives moves | Known folders and native Google Docs retain their `drive:` or `gdoc:` references |
| Filing exceptions survive refactors | Midjourney, Siemens, purchase, travel, and procurement-automation locations remain explicit |
| Fixture does not replace model | Integration example is linked as representative evidence; topology remains normative here |


This record maps Drive guarantees to evidence and distinguishes checks run for this revision from historical results.

| Guarantee or risk | Check or evidence | Current evidence and limit |
| --- | --- | --- |
| Native identity and namespaced uniqueness | Inspect `config/cashflow/sources.yaml`; catalog builder rejects duplicate `source_id` | 30 `drive:<id>` records; no live ID resolution in this update |
| Local bytes match pinned size and SHA-256 | `python -m src.cashflow.sources verify` from `financial-workspace/` | Passed 2026-09-23: 30/30 legacy originals; local evidence only |
| Safe remote acceptance and cache replacement | `python -m unittest tests.cashflow.test_fetch` | Passed 2026-09-23: 5 tests; rclone is mocked |
| Historical remote content matched pinned hashes | Saved `verification-20260915T091436483129Z/verification.json` | 30/30 `verified_remote` on 2026-09-15; not current freshness |
| Coverage basis remains explicit | `sources.py::coverage` and `docs/cashflow/source-coverage.md` | Filename inference labeled; unknowns stay null |
| Specification structure and links | `python tools/validate_specs.py` from `specs/` | Passed 2026-09-23: 5 projects, 1,418 files, 0 errors; one unrelated large-file warning |

## Checks run on 2026-09-23

- `python -m unittest tests.cashflow.test_fetch` from `financial-workspace/`: passed, 5 tests.
- `python -m src.cashflow.sources verify` from `financial-workspace/`: passed, 30/30 local legacy files verified by SHA-256.
- `python tools/validate_specs.py` from `specs/`: passed, 5 projects and 1,418 files with 0 errors; one unrelated 26.0 MiB Draw.io warning.

## Remaining gaps

No live Drive access was used. Current existence, permissions, owners, parents, revisions, shortcuts, trash state, native Google-document exports, full pagination, and complete folder/account/period coverage remain unverified. The saved inventory dates to 2026-09-14 and successful online byte report to 2026-09-15. A future read-only current-state check must retain scope and observation time, prove pagination for its declared scope, and record inaccessible objects without treating them as absent.

