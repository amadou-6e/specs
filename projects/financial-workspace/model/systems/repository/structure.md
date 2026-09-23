# Repository structure

This storage and data-flow view defines both the implemented repository topology and its target topology. The implemented tree records paths that exist now. The target tree defines the intended ownership boundaries. A path is not considered migrated until parity, replay, and consumer checks pass.

## Implemented tree

```text
financial-workspace/
|-- AGENTS.md                         # Repository-wide agent instructions.
|-- README.md                         # Current setup and navigation.
|-- config/
|   `-- cashflow/                     # Source catalog, Drive inventory, accounts, and categories.
|-- src/
|   `-- cashflow/                     # Acquisition, catalog, and replay code.
|-- tests/
|   `-- cashflow/                     # Source, fetch, and replay-oriented tests.
|-- cache/                            # Ignored, replaceable Drive-shaped local evidence.
|   |-- 🏦 Banking/
|   `-- 📉 Liabilities/
|-- data/
|   |-- cashflow/
|   |   |-- canonical/                # Reserved canonical movements and links; currently unpopulated.
|   |   |-- decisions/                # Reviewed overrides and durable decisions.
|   |   `-- runs/<run-id>/            # Generated cash-flow and process artifacts.
|   |-- ledger/                       # Existing normalized procurement candidates.
|   |-- reconciliations/              # Existing matches, exceptions, and coverage reports.
|   `-- statements/                   # Legacy source PDFs, extracts, and manifests.
|-- docs/
|   |-- cashflow/processes/           # Current process definitions and registers.
|   `-- templates/processes/          # Current process documentation template.
|-- ingestion/packages/               # Schemas and frozen review or upload packages.
|-- notion/
|   |-- examples/                     # Saved presentation and schema examples.
|   |-- migrations/                   # Notion-specific migration material.
|   `-- snapshots/                    # Dated remote-state observations.
|-- automation/google-apps-script/    # Existing procurement uploader implementation.
|-- scripts/                          # Legacy builders, reconciliation scripts, and compatibility entry points.
|-- outputs/                          # Regenerable derived output.
|-- reports/                          # Historical human-readable reports.
`-- archive/                          # Retained superseded ledgers and artifacts.
```

| Implemented path | Current role | Authority |
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

## Target tree

```text
financial-workspace/
|-- README.md                          # Entry point, setup, boundaries, and specification links.
|-- AGENTS.md                          # Instructions for people, orchestrators, and delegated agents.
|-- model/                             # Versioned data contracts.
|   |-- objects/                       # System-independent financial concepts.
|   |-- systems/                       # Repository, Drive, Gmail, and Notion representations.
|   `-- mappings/                      # Identities and relationships across systems.
|-- processes/                         # Definitions for repeatable financial workflows.
|   |-- template/                      # Standard for designing and documenting a process.
|   |-- procurement/
|   |   |-- README.md                  # Scope, ownership, inputs, outputs, and status.
|   |   |-- rules/                     # Durable classification and reconciliation policy.
|   |   |-- procedures/                # Human-readable decision flows.
|   |   |-- runbooks/                  # Machine-readable orchestration.
|   |   |-- checklists/                # Start, review, publication, and close gates.
|   |   |-- schemas/                   # Input, decision, package, audit, and report contracts.
|   |   |-- registers/                 # Exceptions and durable resolutions.
|   |   `-- subagents/                 # Bounded assignments and stop conditions.
|   |-- recurring-expenses/
|   |-- everyday-spending/
|   |-- monthly-close/
|   |-- travel/
|   |-- matters/
|   `-- tax/
|-- skills/                            # Process-independent reusable agent capabilities.
|   |-- source-discovery/
|   |-- document-extraction/
|   |-- record-linking/
|   |-- package-validation/
|   `-- publication-review/
|-- src/                               # Shared executable harness.
|   |-- acquisition/
|   |-- extraction/
|   |-- reconciliation/
|   |-- artifacts/                     # Manifests, lineage, hashing, indexes, and validation code.
|   |-- publishing/
|   `-- orchestration/
|-- integrations/                      # External-system adapters and operational configuration.
|   |-- google-drive/
|   |-- gmail/
|   `-- notion/
|-- config/                            # Versioned shared and process configuration.
|   |-- accounts.yaml
|   |-- sources.yaml
|   |-- categories.yaml
|   `-- processes/
|-- cache/                             # Ignored, replaceable remote-evidence cache.
|   |-- google-drive/
|   `-- gmail/
|-- workspaces/                        # Generated execution areas owned by workflow agents.
|   |-- procurement/
|   |   `-- runs/
|   |       `-- <run-id>/
|   |           |-- run.json           # Scope, versions, coverage, and run state.
|   |           |-- inputs/            # Frozen references and verified input manifests.
|   |           |-- working/           # Regenerable candidates and intermediate calculations.
|   |           |-- decisions/         # Reviewed run-specific overrides and resolutions.
|   |           |-- package/           # Validated records proposed for publication.
|   |           |-- reviews/           # Human and delegated-agent findings.
|   |           |-- publication/       # Diff, approval, receipt, and verification.
|   |           `-- report.md          # Coverage, results, exceptions, and next actions.
|   |-- recurring-expenses/runs/<run-id>/
|   |-- everyday-spending/runs/<run-id>/
|   |-- monthly-close/runs/<run-id>/
|   |-- travel/runs/<run-id>/
|   |-- matters/runs/<run-id>/
|   `-- tax/runs/<run-id>/
|-- tests/
|   |-- fixtures/
|   |-- unit/
|   |-- contract/
|   `-- replay/
|-- migrations/                        # Bounded transitions of paths, schemas, and remote layouts.
`-- archive/                           # Superseded material retained for audit or migration.
```

`processes/<process>/` owns process design and maintenance. `workspaces/<process>/runs/<run-id>/` owns generated execution evidence. Run findings can change a process definition only through a reviewed specification change.

## Migration mapping

| Implemented path | Target path | Required gate |
| --- | --- | --- |
| `docs/cashflow/processes/<process>/` | `processes/<process>/` | Documentation parity and repaired links |
| `docs/templates/processes/` | `processes/template/` | Template parity and process validation |
| `data/cashflow/runs/<run-id>/` | `workspaces/<process>/runs/<run-id>/` | Manifest compatibility and deterministic replay |
| `data/cashflow/decisions/` | Process registers or run `decisions/` | Explicit split between durable policy and run-specific decisions |
| `config/cashflow/` | Shared `config/` plus `config/processes/` | Consumer inventory and configuration-schema validation |
| `src/cashflow/` | Capability-based `src/` modules | Import compatibility, tests, and replay parity |
| `tests/cashflow/` | `tests/unit/`, `tests/contract/`, and `tests/replay/` | Equivalent coverage and passing checks |
| Drive-shaped `cache/` | `cache/google-drive/` | Source-ID and hash-preserving cache migration |
| Gmail evidence embedded in ledgers | `cache/gmail/` plus indexed references | Stable message IDs, retrieval contract, and attachment hashes |
| `ingestion/packages/` | Run `package/` or shared schemas | Package identity, schema ownership, and consumer migration |
| `notion/` operational code or snapshots | `integrations/notion/` plus run `publication/` | Baseline, dry-run diff, receipt, and recovery checks |
| `automation/google-apps-script/` | `integrations/notion/` or compatibility wrapper | Uploader parity and idempotence validation |
| `data/ledger/`, `data/reconciliations/`, `data/statements/` | Canonical, workspace, register, and cache destinations | Remote hash verification, closed-period replay, and path-consumer checks |
| `scripts/`, `outputs/`, `reports/` | Shared harness, run artifacts, or archive | Replacement entry points and confirmed downstream parity |

The migration must follow [the existing-system contract](../../../migrations/0001-existing-system.md). Legacy files and scripts remain until remote hash checks, closed-period replay, and all known path consumers pass.

## Data flow

```text
provider original
  -> native ID + metadata + pinned hash
  -> source catalog and replaceable cache
  -> shared code + process rules + reviewed decisions
  -> workspaces/<process>/runs/<run-id>/
  -> validation and review
  -> canonical data or approved publication package
```
