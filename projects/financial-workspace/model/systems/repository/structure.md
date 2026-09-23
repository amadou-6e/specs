# Repository structure

This storage and data-flow view answers where repository objects live and which are authoritative, generated, cached, or transitional. It explains the contract without adding guarantees.

| Path | Current role | Authority |
| --- | --- | --- |
| `config/cashflow/` | Catalog, Drive inventory, accounts, categories | Versioned configuration |
| `src/cashflow/` | Catalog, acquisition, replay code | Executable behavior; parsers incomplete |
| `tests/cashflow/` | Source and fetch tests | Checks, not passing evidence until run |
| `cache/` | Drive-shaped local copies | Ignored and disposable |
| `data/cashflow/canonical/` | Reserved posted movements and links | Intended canonical location; currently empty |
| `data/cashflow/decisions/` | Reviewed overrides | Intended decision history |
| `data/cashflow/runs/<run-id>/` | Verification and process artifacts | Generated evidence; manifests determine completeness |
| `data/ledger/`, `data/reconciliations/` | Existing ledger and matches | Transitional until parity |
| `data/statements/` | Legacy sources, manifests, extracts | Transitional tracked source storage |
| `notion/snapshots/` | Dated baseline | Historical observation |
| `ingestion/packages/` and run `package/` | Schemas and frozen packages | Review input; generation does not publish |
| `docs/cashflow/processes/` | Workflows and exception register | Operating contract |
| `scripts/`, `outputs/`, `reports/` | Legacy builders and presentations | Transitional and regenerable |

The earlier proposal used `workspaces/<process>/...`; implementation uses `docs/cashflow/processes/` and `data/cashflow/runs/`. A future move requires a migration with parity and path-consumer checks.

```text
provider original
  -> native ID + metadata + pinned hash
  -> source catalog and replaceable cache
  -> code + reviewed decisions
  -> run artifacts and manifest
  -> validation and review
  -> canonical data or publication package
```


