# Validation

This page maps guarantees to checks and records evidence examined on 2026-09-23. Commands are relative to `financial-workspace/` unless stated otherwise.

## Checks run

| Check | Result | Proves | Limits |
| --- | --- | --- | --- |
| `python -m unittest discover -s tests -p "test_*.py"` | Passed: 3 tests | Source, fetch, and package behavior | Mocks do not prove remote access |
| `python -m src.cashflow.sources verify` | Passed: 30/30 files | Indexed legacy PDFs match pins | Local bytes only |
| `python tools/validate_specs.py` from specs root | Passed: 5 projects, 1,417 files; 0 errors, 1 unrelated large-file warning | Specification structure and links | Not implementation behavior |

Implementation revision: `feat/rclone-cashflow-fetch` at `89486b8`, with tracked changes and untracked runs. Current-file claims therefore include working-tree state.

## Evidence inspected

- `verification-20260915T091436483129Z/verification.json` records online checks for 30 cataloged sources.
- `procurement-2025-12-test-20260915T120000Z/` contains a manifest, orchestration state, work, package, audit, and review, but proves only one process layout.
- `recurring-expenses-2025-12-trial-20260923T080000Z/` contains an artifact index and failure inventory and was untracked.
- `notion/snapshots/2026-09-08/` is a dated baseline, not current remote state.

## Guarantee-to-check map

| Guarantee | Check | Status |
| --- | --- | --- |
| Provider identity | Rebuild catalog, assert unique IDs, compare inventory | Uniqueness implemented; rebuild not run |
| Pinned bytes | Run source verification | Recorded above |
| Safe cache replacement | Fetch tests for traversal, drift, duplicates | Recorded above |
| Remote freshness | Run read-only online fetch and retain report | Last saved success 2026-09-15 |
| Deterministic replay | Replay frozen closed month from fresh checkout | Runner exists; contract absent |
| Canonical controls | Validate IDs, decimals, transfers, allocations, statement totals | Canonical set absent |
| Uniform run immutability | Validate all runs against one schema and correction links | Shared schema absent |
| Exception history | Test deduplicated failure and in-place resolution | Partly unit-tested |
| Publication separation | Compare package hash, approval, status, provider result | Cash Flow writer absent |
| Secret exclusion | Secret scan and failure-message review | Not run |

## Gaps

The 30-object scope does not prove month completeness. Dirty state is not captured by the commit. Legacy and intended canonical layouts coexist without demonstrated parity. No manifest schema and correction mechanism spans all run types. No complete fresh-checkout closed-month replay or controlled Cash Flow publication has been demonstrated.
