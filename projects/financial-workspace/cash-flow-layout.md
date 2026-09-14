# Reproducible cash-flow analysis and Notion publication

Status: proposed architecture. The commands, folders, and Cash flow database below are target behavior, not an implemented workflow. The existing-system migration and tax workspace rules are in [review-contracts.md](review-contracts.md).

## Goal and boundary

A person with access to the private GitHub repository and the linked Google Drive files can clone the project on another machine, fetch the evidence for a named period, reproduce the cash-flow analysis, inspect every reconciliation decision, and publish an approved result to Notion. The LLM may help classify and explain records, but the procedure and artifacts must remain usable without the original chat or the LLM's direct access to Notion.

GitHub is the portable control plane: code, setup instructions, source index, schemas, rules, exceptions, tests, and versioned analysis results. Google Drive holds the original statements and documents. Notion is a published view, not the source of truth. Drive Cash flow, if created, is a convenient review and import handoff; it must not become the only location for code or decisions.

Cash flow records actual account movements. Procurement contains item or order detail linked to those movements, so the same spend is not counted twice. Income, expense offsets, expenses, and owned-account transfers remain distinct. A monthly financial position snapshot is a separate derived result.

## Portable repository layout

```text
README.md                                    # Start-here link to the runbook and current coverage.
docs/cashflow/
|-- README.md                                # Setup and scripted replay from a fresh checkout.
|-- methodology.md                           # Inclusion, categories, transfers, refunds, FX, work travel.
|-- source-coverage.md                       # Accounts, periods, gaps, and latest verified close.
|-- notion-publishing.md                     # Review, approval, idempotency, and rollback procedure.
`-- decisions.md                             # Dated changes to rules and their rationale.
config/cashflow/
|-- accounts.yaml                            # Stable account IDs and account ownership.
|-- categories.yaml                          # Controlled cash-flow taxonomy.
|-- sources.yaml                             # Drive file IDs/URLs, provider, period, format, hash, status.
`-- example.env                              # Variable names only; never real credentials.
src/cashflow/
|-- fetch.py                                 # Retrieve indexed Drive files using user auth.
|-- parse/                                   # Versioned provider-specific statement parsers.
|-- normalize.py                             # Stable IDs and signed amounts.
|-- reconcile.py                             # Transfer, wallet, refund, and procurement links.
|-- classify.py                              # Deterministic rules plus explicit reviewed overrides.
|-- analyze.py                               # Totals, monthly series, coverage, and controls.
|-- export_notion.py                          # Validated, deterministic import package.
`-- upload_notion.py                          # Separate optional uploader; no LLM credentials.
tests/test_cashflow/                               # Parser fixtures and independent reconciliation checks.
data/cashflow/
|-- decisions/                               # Reviewed row-level classifications and match overrides.
|-- canonical/                               # Versioned normalized movements and relationship table.
|-- runs/<run_id>/                            # Immutable manifest, analysis outputs, validation, review.
cache/                                       # Top-level, ignored mirror of Financial Workspace in Drive.
data/reconciliations/exception_register.md    # Existing central exception trail.
```

This is a migration target, not a claim that the files already exist. Current `data/statements/YYYY/pdf/manifest.json` files supply initial Drive IDs. Existing `scripts/rebuild_ledger.py`, wallet and SSKM reconciliation outputs, and procurement importer supply logic and evidence to migrate. Record old-to-new IDs and compare totals before retiring any current script or artifact. A first implementation can keep the current folder names while exposing the same command interface.

The private repository should track source metadata, code, rules, reviewed decisions, schemas, test fixtures with synthetic/redacted data, run manifests, and compact normalized results needed for replay. It should not track tokens, OAuth files, credential-like certificates, or full statement PDFs. If normalized financial data in Git is too sensitive, use an encrypted artifact store and put its retrieval instructions and hashes in the repo; do not silently omit required replay inputs.

## Drive source index and fetch contract

Each source index entry needs `source_id`, Drive file ID and URL, provider, account ID, document type, coverage start/end, original filename, MIME type, expected SHA-256, parser name/version, and `available`, `superseded`, or `missing` status. A Drive folder link alone is insufficient: it cannot prove which statement version was analyzed. Cross-year files have one source entry with their full coverage period. Keep the existing Drive file IDs stable when folders move.

`fetch` checks account permissions, downloads only the indexed files needed for the requested period, verifies hashes, and stores them in the top-level ignored `cache/` mirror described in [review-contracts.md](review-contracts.md). It reports inaccessible, changed, or absent files before analysis and records specific gaps in `data/reconciliations/exception_register.md`. It must not substitute a similar-looking statement automatically. Cached originals can accelerate replay but are never the sole source index. Gmail-only evidence requires stable message IDs/links and an explicit export or retrieval method; a human-readable link without retrieval access is not sufficient for a fully automated replay.

Authentication is interactive user OAuth or another explicitly configured credential on each machine. The repo contains setup instructions and `example.env`, not secrets. Reproduction requires access to the private repo and every referenced source; without access, the tool produces a coverage report rather than an apparently complete analysis. Cloud automation is optional, not a prerequisite.

## Proposed Drive layout

Each upload run gets one subfolder named by its immutable `run_id` under `Incoming`, `Approved`, or `Archive`. Move that whole folder as its status changes, preserving the CSV, manifest, review, and validation report together. Account and year folders are not repeated here: original statements stay under `Banking/<provider>/<year>`, and the source index points to their exact Drive IDs. This separates upload packages from source evidence.

```text
Financial Workspace/
|-- Banking/                                # Original source statements remain here.
|-- Cash flow/                              # Optional human review and Notion import handoff.
|   |-- README [native Google Doc]          # Links to GitHub runbook and latest approved run.
|   |-- Incoming/<run_id>/                  # Frozen CSV, manifest, review, and validation report.
|   |-- Approved/<run_id>/                  # Same reviewed package, ready for upload.
|   `-- Archive/<run_id>/                   # Prior packages and upload receipts.
`-- other existing folders/
```

An upload package is named by immutable `run_id` and includes `cashflow.csv`, `manifest.json`, `review.md`, and a validation report. The exact same bytes are retained with the Git run or encrypted artifact. Moving a package between Drive folders changes workflow status, not its content. Original PDFs remain under Banking. The Drive Cash flow folder is not yet created.

## Transaction and decision model

One canonical row represents one posted movement on one owned account. Required fields: stable `transaction_id`, `account_id`, `posted_date`, signed `amount`, `currency`, `counterparty`, `reference`, `source_id`, `source_row_id`, `type`, `category`, `personal_work`, and `reconciliation_status`. Preserve the provider's original description and transaction ID. Optional fields include value date, documented EUR conversion and FX source, related matter or procurement IDs, and notes. Use exact decimal amounts, not floating-point arithmetic.

A separate relationship table supports many-to-many links: a charge can fund several procurement items, an order can have split charges, a refund can be partial, and a reimbursement can cover several expenses. Paired movements between owned accounts are transfers and net to zero in consolidated income/expense. Internal wallet movements are treated similarly; external settlement is counted once. Work-related expenses appear with a work classification but are excluded from personal procurement totals. Never infer a journey, payment, FX conversion, or match from amount alone.

Rules and row-level overrides must be reviewable files. Every override records target transaction ID, prior and new classification or match, rationale, evidence IDs, reviewer/date, and rule version. Changing a rule creates a new run, leaving the old run reproducible. Ambiguous, excluded, or missing records require the existing exception-register entry and evidence trail.

## Repeatable procedure

The target CLI should work on Windows, macOS, and Linux with a pinned Python version and locked dependencies. Its command names below are illustrative until implemented.

```text
1. git clone <private-repository> && follow docs/cashflow/README.md
2. cashflow doctor                       # Check Python, config, authentication, permissions.
3. cashflow fetch --period 2026-08        # Pull indexed evidence and verify hashes.
4. cashflow build --period 2026-08        # Parse, normalize, reconcile, classify.
5. cashflow validate --period 2026-08     # Check coverage, identities, totals, transfers, exceptions.
6. cashflow report --period 2026-08       # Produce tables, cash-flow series, and review.md.
7. cashflow export-notion --period 2026-08 # Freeze an import package; no remote write.
8. Review and approve the exact package.
9. cashflow upload-notion --run <run_id>  # Optional separate publication step.
10. cashflow verify-notion --run <run_id> # Compare IDs and totals with the approved package.
```

A full replay from a fresh checkout must regenerate the same canonical row IDs, categories, totals, and export bytes for a given code revision, source hashes, rule version, and decision set. Generated timestamps and upload receipts live outside the deterministic export bytes. The run manifest records Git commit, dependency-lock hash, source IDs/hashes and coverage, parser/rule versions, command arguments, row counts, per-account opening/closing or statement control totals where available, category totals by currency, unresolved exception IDs, and output hashes. A no-write dry run is the default for Notion publication.

Validation fails on duplicate IDs, unindexed inputs, hash mismatch, invalid dates/currencies, missing source references, double-counted transfers, or unexplained gaps. A period can be marked `partial` with explicit scope and exception IDs; it cannot be called a complete close. The runbook documents how to update a source, review an override, rerun, and compare old versus new outputs.

## Notion projection and publication

The proposed `Cash flow` database uses immutable `External transaction ID` as its upsert key. Visible properties include Date, signed Amount, Currency, Account, Type, Category, Counterparty, Reference, Personal/Work, Reconciliation status, Source link, and related procurement or matter. A table view exposes date/account/type/category/status filters. Confirmed charts use only verified movements and exclude transfers from income and expense totals. Notion formulas and charts are presentation, not authoritative calculations.

The export is generated from a named validated run, never edited manually after approval. The uploader compares the approved manifest and current Notion IDs, creates or updates by external ID, records per-row results and returned page IDs, and verifies count and amount totals after upload. Repeating the same run must create no duplicates. A failed upload is resumable from its receipt. A later correction is a new run with a diff, not a silent overwrite of history. The existing procurement Apps Script is separate and cannot be assumed to support Cash flow without a new schema and validation path.

## Implementation milestones

1. Inventory all account statements and other evidence, compare Git-tracked PDF hashes with Drive, migrate existing Drive IDs into `sources.yaml`, and publish a coverage matrix for 2024-11 onward. Identify missing periods explicitly.
2. Wrap or migrate the existing statement parsers and reconciliation rules; add independent controls against provider statement totals and known procurement links.
3. Make a fresh-machine replay succeed for one closed month using only the repo, Drive access, and documented setup. Compare its output to the historical analysis.
4. Add the deterministic Notion export and dry-run diff. Create the Drive handoff and Notion database only after the replay and import schema have been reviewed.
5. Extend by period and provider, keeping every run and rule change traceable.

## Open design choices

- Whether sensitive normalized transactions are kept in the private Git repository or in a versioned encrypted artifact store with a Git-tracked index.
- Whether provisional transactions are published to a Notion review view or withheld until verified.
- Whether work-related movements share the database with a default personal filter or use a separate view.
