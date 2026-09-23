# Validation

This record maps guarantees to evidence. No external system was queried or mutated for this revision.

## Checks run on 2026-09-23

| Check | Evidence | Result |
| --- | --- | --- |
| Specification structure and links | `python tools/validate_specs.py` from `specs/` | Cross-system entry passed; repository-wide run reported one pre-existing broken link in `model/systems/repository/README.md` to absent `sources.md` |
| Source identity | Read-only `config/cashflow/sources.yaml` | Passed: namespaced IDs, native IDs/URLs, hashes, coverage and observation metadata |
| Destination identity | Read-only `config/cashflow/notion_sources.json` | Passed: page, database, and data-source identities remain distinct |
| Handoff provenance | Procurement test-run manifest | Passed with declared gaps: tree state, hashes, scoped baseline, Gmail IDs, gaps, publication `not_run` |
| Ownership | Model contracts, cash-flow workflow, migration 0001 | Passed: this entry owns only cross-system rules |

Evidence came from branch `main`, commit `dcc72d596aac78bc90b5e45e6e89ba94be6baeef`, with extensive pre-existing tree changes. The representative run records commit `d6319984ae3e4df706f882a8cfd37b38dea478f4`.

## Required controls and gaps

Schema/property tests must reject invalid namespaces, duplicates, collisions, missing evidence, hash changes, unbalanced exact allocations, and unsupported transitions. Replay must compare stable IDs, values, and hashes. Publication tests must cover baseline freshness, duplicates, package-bound approval, dry-run diff, repeated upsert, receipts, and post-write controls.

Generic reference, link, projection, approval, and receipt schemas are not implemented. The inspected run is candidate-scoped and partial; complete-month Gmail discovery and generic historical settlement are unproved. Remote observations were not refreshed. Migration 0001 choices remain open. The dirty implementation tree is not a clean deployable baseline.
