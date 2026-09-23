# Financial workspace structure proposal

Status: discussion draft

## Core model

A concrete Google Drive layout populated with representative workspace files is available in [drive-folder-example](integrations/google-drive/example/README.md).

The reproducible Cash flow analysis, portable source index, Drive handoff, and Notion publication contract are specified in [cash-flow-layout.md](processes/cash-flow/workflow.md). Existing-system migration, recurring schedules, liability lifecycles, and tax-year workspaces are specified in [review-contracts.md](migrations/0001-existing-system.md). These are proposals; the remote Cash flow folder and replay CLI have not been created.

The repository, Notion, and Google Drive should share terminology and stable identifiers. Their structures do not need to be identical because they serve different purposes.

~~~text
Finance                                       # Contains the complete personal financial system.
|-- Financial position                       # Shows what is owned and owed at a specific date.
|   |-- Accounts                             # Registers banks, wallets, cards, loans, cash, and investment accounts.
|   |-- Assets                               # Records balances, investments, receivables, deposits, and other tracked value.
|   |-- Liabilities                          # Records loans, credit balances, taxes payable, and other confirmed obligations.
|   `-- Monthly snapshots                    # Preserves month-end balances, assets, liabilities, and calculated net worth.
|-- Cash flow                                # Records actual movements of money during a period.
|   |-- Earned income                        # Contains salary, investment income, and other earnings.
|   |-- Expense offsets                      # Contains receipts that reverse or reimburse earlier expenses.
|   |   |-- Employer reimbursements received # Records payments received for approved work expenses.
|   |   `-- Merchant refunds received        # Records money returned by sellers for purchases or cancellations.
|   |-- Expenses                             # Contains outflows for consumption, obligations, travel, tax, and fees.
|   |   |-- Procurement                      # Tracks meaningful goods and services at item or order level.
|   |   |-- Recurring expenses               # Tracks rent, utilities, insurance, memberships, and scheduled commitments.
|   |   |-- Everyday spending                # Groups groceries, dining, entertainment, and other frequent small purchases.
|   |   |-- Travel                           # Contains personal transport, accommodation, and travel-related spending.
|   |   |-- Taxes                            # Contains tax payments and related cash charges.
|   |   `-- Financial costs                  # Contains interest, account fees, exchange fees, and similar charges.
|   `-- Transfers                            # Links movements between accounts without treating them as income or expense.
|-- Open matters                             # Tracks processes that may create a future payment, receipt, or obligation.
|   |-- Returns and merchant refunds         # Tracks returned items and refunds requested from sellers.
|   |-- Compensation claims                  # Tracks claims for delays, cancellations, damage, or service failures.
|   |-- Employer expense claims              # Tracks submitted work expenses through approval and reimbursement.
|   |-- Insurance claims                     # Tracks insured events, submissions, decisions, and payouts.
|   |-- Deposits and recoverable balances    # Tracks money expected back from landlords, providers, or other parties.
|   `-- Tax matters                          # Tracks each tax year from evidence collection through filing and assessment.
`-- Documents                                # Contains or links to the original evidence supporting financial records.
    |-- Banking                              # Contains account statements, balance confirmations, and bank correspondence.
    |-- Purchases                            # Contains invoices, receipts, order confirmations, and warranties.
    |-- Recurring contracts                  # Contains leases, policies, subscriptions, and recurring service agreements.
    |-- Travel                               # Contains tickets, itineraries, bookings, and accommodation evidence.
    |-- Claims and reimbursements            # Contains claim forms, submissions, decisions, and settlement evidence.
    |-- Employment                           # Contains contracts, payslips, annual certificates, and employer correspondence.
    |-- Investments                          # Contains broker statements, trade confirmations, and investment tax documents.
    `-- Tax                                  # Contains filings, assessments, certificates, correspondence, and supporting evidence.
~~~

Financial position records what is owned and owed at a point in time. Cash flow records actual account movements. Open matters records processes that may produce future payments, refunds, reimbursements, or obligations. Documents contains the original evidence.

Employer reimbursements and merchant refunds are expense offsets so they do not inflate earned income. Transfers between owned accounts are neither income nor expenses.

## Tax

Tax is cross-cutting. Each tax year is an Open matter with a visible lifecycle status, living status/checklist/evidence-index/next-step documents, subject-based working analyses, immutable review artifacts, and links to filing, assessment, payments, refunds, and source evidence. Keep one original file and link it to every relevant tax year; see [review-contracts.md](migrations/0001-existing-system.md).

A tax-relevant purchase remains in its natural expense category and receives tax metadata: tax relevance, tax year, tax category, deductible percentage, business or personal allocation, supporting document, filing status, and filing reference.

Expected tax payments may appear as liabilities once sufficiently certain. Expected tax refunds may appear as receivables. Actual payments and refunds also appear in Cash flow.

## Claims and reimbursements

An open matter can exist before any payment and can relate to several transactions and documents.

~~~text
Draft -> Submitted -> Acknowledged -> Approved -> Paid -> Closed
                                      |-> Partially approved
                                      `-> Rejected or disputed
~~~

A merchant refund relates to the original order. A travel compensation claim relates to its journey. An employer expense claim groups its business expenses, submitted report, approved amount, rejected items, and eventual reimbursement transaction.

Claims can remain beside their subject evidence in Drive while a central index in Notion links to them. This avoids duplicate documents.

## Recommended systems

Notion databases:

- Accounts
- Transactions
- Procurement
- Recurring expenses
- Matters
- Monthly snapshots

### Current remote Drive after reorganization

Verified against the connected Drive on 2026-09-13. The existing Financial folder was moved from Documents to the Drive root and renamed Financial Workspace; its folder ID and links were preserved. The following is the implemented remote hierarchy, not a local copy.

~~~text
My Drive/
+-- Documents/
|   +-- E-Commerce/Billing/Midjourney/  # Invoice and receipt PDFs
|   +-- Work/Siemens/Financial records/ # Siemens agreement
|   +-- Reisen/                         # Existing travel evidence
|   `-- other document areas
`-- Financial Workspace/
    +-- 🏦 Banking/
    |   +-- SSKM/2021/ ... 2026/
    |   +-- DKB/2023/ ... 2026/
    |   +-- PayPal/2023/ ... 2026/
    |   `-- Revolut/2023/ ... 2026/
    +-- 📉 Liabilities/
    |   +-- SSKM/S-Privatkredit/
    |   +-- KfW/2026/
    |   `-- BVA/
    +-- 🔁 Recurring spending/
    |   +-- Housing/2021/, 2024/, 2026/
    |   +-- Insurance/2023/, 2026/
    |   `-- Subscriptions/2026/
    +-- 🧾 Everyday spending/Receipts/2026/
    +-- 💼 Employment/bridgingIT/2024/ ... 2026/
    +-- 📈 Investments/
    +-- 🧮 Tax/
    |   +-- Elster/                      # Existing older tax files
    |   `-- 2026/
    |       +-- Income/
    |       +-- Deductions/
    |       +-- Filing/
    |       +-- Assessment/
    |       `-- Correspondence/
    +-- [Google Doc] Workspace links  # Links to purchase and travel folders
    `-- [Google Doc] README             # Explains the workspace and filing rules
~~~

The procurement automation folders remain separate at the Drive root: [Procurement imports](https://drive.google.com/drive/folders/1ZRcE8OLnbYVz3tbbnlyEAxtW91fK4xUk), [Incoming](https://drive.google.com/drive/folders/1OIm_NoHc-WPlIWTCCIk8ZYwDMyTPIwWn), [Needs review](https://drive.google.com/drive/folders/1yjfN5Zpd-cYfDme_QT7SUzFW-6Fnq2ry), [Processed](https://drive.google.com/drive/folders/1UfmtFudm3m8UTRJFABqcxT-8N2Q9NPbG), and [Failed](https://drive.google.com/drive/folders/1IROCGrG7ZuTkxbNOhQBNWuYlWN6GgLXX).

| Implemented remote location | Relation to proposal |
|---|---|
| [Financial Workspace](https://drive.google.com/drive/folders/11t4fi7yXKUSyZBpKkiuEehwxqXll6TN3) is a sibling of Documents, with [🏦 Banking](https://drive.google.com/drive/folders/1vQIl5CWKXT9ragc7Ml8YG_it1ictVczd), [📉 Liabilities](https://drive.google.com/drive/folders/1Tz0EyOtc1msQ3Fxp81OswPfNl9iB_Yuk), [💼 Employment](https://drive.google.com/drive/folders/18JclK-t-r1sPBQBBdKgrC8xAOgcSjK4g), [🧮 Tax](https://drive.google.com/drive/folders/1EfvBeHXYdjKtE-9S3B9DsPxdAyTflhd2), and the other proposed categories. | Matches the proposed top-level separation and main categories. |
| [PayPal](https://drive.google.com/drive/folders/1ClzG6OAFRx3txcx_cmGR0IU46lIwPgt4) and [Revolut](https://drive.google.com/drive/folders/1lnoY3R8RSyq2UzaCrVZlBY_q4LQDHyi3) statements are filed by year. The one Revolut file covering 2024 and 2025 is stored once under 2025. | Matches year grouping without duplicating cross-year evidence. |
| [SSKM loan](https://drive.google.com/drive/folders/1fokPnONYdp3us1ZMeQDFmWh7apmkXx-6) and [KfW](https://drive.google.com/drive/folders/1tx4YhVNV0gzUHm8DUKElEKNZDmFuEc7n) are under Liabilities; the dated KfW balance PDF is under 2026. | Matches the liability distinction. Undated loan files remain at provider level. |
| [Elster](https://drive.google.com/drive/folders/1JsLXmg2x8DVkUbij2AoyA0FFP7KvUAkL) is under Tax. | Older Elster files have not yet been classified into tax-year and document-type folders. |
| [Billing/Midjourney](https://drive.google.com/drive/folders/1E0jG_UbCaWX7HHgopAvZMJwAFs6C4Y6W) is under [E-Commerce](https://drive.google.com/drive/folders/1BNOTTGhBz6CA4S0Wd-Oo8f-LP0MVHse7). [Siemens financial records](https://drive.google.com/drive/folders/1b8ToXu8RtEOa2zSIx9UaAWEqg5TU4Wjo) are under the existing [Work/Siemens](https://drive.google.com/drive/folders/1k2DtLtCGUZIuBwwTBLdd9hjUpaCSp86R) folder. | Follows the explicit exceptions to the initial proposal. |
| [Recurring spending](https://drive.google.com/drive/folders/1bErFY9OC6HCf3jgy6NWsYBXDUr98CE-s), [Everyday spending](https://drive.google.com/drive/folders/1Rr0TqdpRuTk8mHB2UrzYf5Fpwe66cwzv), and [Investments](https://drive.google.com/drive/folders/1LAJZLhxkliR95pmE-5rdG5ocwhq95BHu) exist. [Workspace links](https://docs.google.com/document/d/14-h2WwcFpFYKDVveGAspKcE4eK-cGz1pRp8R4f1TqUo/edit) sits at the Financial Workspace root. | The native Google Doc links to the verified purchase and travel folders. [README](https://docs.google.com/document/d/1AtknilGP8OP8VvRN9U08vfABqhC2669euLQ-pjf9tnw/edit) explains the workspace; no dedicated Claims folder was identified. |

Population update, 2026-09-13: Three historical housing records were filed under Recurring spending/Housing/2021 and 2024. Three TK membership and payment-authorisation records were filed under Recurring spending/Insurance/2023. These years follow the available document dates; the actual expense periods have not been verified. Everyday spending and Investments still have no source evidence filed.

### Proposed Finance Drive

Google Drive should be organized by financial subject first and by year inside each provider or document class. This keeps the same account or obligation together across years.

Original financial evidence and workspace navigation documents belong here. Canonical normalized data, code, reconciliation decisions, and run manifests belong in the private repository or an indexed encrypted artifact store. Frozen Notion import packages may also be copied to the proposed Cash flow Drive folder for review, while the repository retains the reproducible package identity and hashes.

~~~text
Financial Workspace/
+-- 🏦 Banking/                                      # Original statements and bank correspondence.
|   +-- SSKM/
|   |   +-- 2024/  -> [PDF] SSKM_2024-12_Kontoauszug.pdf
|   |   +-- 2025/  -> [PDF] SSKM_2025-12_Kontoauszug.pdf
|   |   \-- 2026/  -> [PDF] SSKM_2026-08_Kontoauszug.pdf
|   +-- PayPal/
|   |   +-- 2024/  -> [PDF] PayPal_Umsaetze_2024.pdf
|   |   +-- 2025/  -> [PDF] PayPal_Umsaetze_2025.pdf
|   |   \-- 2026/  -> [PDF] PayPal_Umsaetze_2026.pdf
|   +-- Revolut/
|   |   +-- 2024/  -> [PDF] Revolut_2024.pdf
|   |   +-- 2025/  -> [PDF] Revolut_2024-2025.pdf
|   |   \-- 2026/  -> [PDF] Revolut_EUR_2026.pdf
|   \-- DKB/
|       \-- 2026/  -> [PDF] DKB_2026_Auszug-01.pdf
+-- 📉 Liabilities/                                  # Original evidence for loans and money owed.
|   \-- KfW/
|       \-- 2026/
|           +-- [PDF] KfW_Bildungskredit_Kontostand_2026-08.pdf
|           \-- [PDF] KfW_Zinsbescheinigung_2026.pdf
+-- 🔁 Recurring spending/                           # Financial documents for repeated obligations.
|   +-- Housing/
|   |   \-- 2026/
|   |       +-- [PDF] Mietvertrag.pdf
|   |       +-- [PDF] Nebenkostenabrechnung_2026.pdf
|   |       \-- [PDF] Strom_Jahresabrechnung_2026.pdf
|   +-- Insurance/
|   |   \-- 2026/
|   |       +-- [PDF] Versicherungspolice.pdf
|   |       \-- [PDF] Beitragsrechnung_2026.pdf
|   \-- Subscriptions/
|       \-- 2026/  -> [PDF] Jahresrechnung_2026.pdf
+-- 🧾 Everyday spending/                            # Original receipt images retained when useful.
|   \-- Receipts/
|       \-- 2026/
|           +-- 2026-08/
|           |   +-- [JPG] 2026-08-14_Supermarket_31-20.jpg
|           |   \-- [PDF] 2026-08-18_Restaurant_24-50.pdf
|           \-- 2026-09/
|               \-- [HEIC] 2026-09-03_Hardware-store_18-90.heic
+-- 💼 Employment/                                   # Financial employment evidence only.
|   \-- BridgingIT/
|       \-- 2026/
|           +-- [PDF] Lohnabrechnung_2026-08.pdf
|           +-- [PDF] Lohnsteuerbescheinigung_2026.pdf
|           \-- [PDF] Reisekostenerstattung_2026-05.pdf
+-- 📈 Investments/                                  # Statements, confirmations, and certificates.
|   \-- Broker name/
|       \-- 2026/
|           +-- [PDF] Depotauszug_2026-12-31.pdf
|           +-- [PDF] Jahressteuerbescheinigung_2026.pdf
|           \-- [PDF] Kaufabrechnung_EXAMPLE.pdf
+-- 🧮 Tax/                                          # Tax-year matters and original authority documents.
|   \-- <year>/                                     # Stable year folder; status lives in Matters and STATUS.
|       +-- STATUS, CHECKLIST, EVIDENCE MANIFEST, NEXT STEPS  # Living indexes linked to their canonical copies.
|       +-- subjects/                               # Funding, residence, exchange, employment, and other topics.
|       +-- review_artifacts/                       # Frozen findings and reviewed-input hashes.
|       +-- Filing/                                 # Original submitted returns and acknowledgements.
|       +-- Assessment/                             # Original assessment notices.
|       \-- Correspondence/                         # Original tax-authority correspondence.
+-- [Google Doc] Workspace links               # Links to related document areas.
\-- [Google Doc] README                       # Explains the workspace and filing rules.
~~~

Purchase and travel records remain in their subject folders, which hold invoices, tickets, itineraries, correspondence, and workflow state. The Finance Drive uses Workspace links to point to those verified folders and retains only independently financial documents, such as a reimbursement statement. A dedicated Claims folder has not been verified; claim evidence may remain with its purchase or journey.

The [Drive folder example](integrations/google-drive/example/README.md) describes representative original statement PDFs, but the copied binaries remain local and are excluded from this specs repository. Names shown above for unavailable document types are illustrative and are not fabricated files.

## Repository Tasks

The repository must support the complete lifecycle of every recurring financial process:

1. **Define:** State purpose, scope, ownership, inputs, outputs, invariants, evidence requirements, and completion criteria.
2. **Design:** Develop decision flows, rules, schemas, agent contracts, controls, review gates, and failure handling before relying on the process.
3. **Execute:** Create an isolated run, acquire pinned evidence, apply versioned code and decisions, review exceptions, produce a validated package, and publish only after the required gate.
4. **Maintain:** Preserve run evidence, review failures and exceptions, promote durable lessons through reviewed changes, test replay, and migrate consumers before retiring legacy paths.

Process-independent skills provide reusable agent behavior. The shared code harness implements acquisition, extraction, reconciliation, artifact management, orchestration, and publication controls. The local cache provides replaceable access to indexed Drive and Gmail evidence. Process workspaces contain execution-specific generated artifacts and never replace process definitions or source systems.

## Target repository workspace
The repository is organized by responsibility rather than by financial category. Domain concepts and external-system representations are defined once, reusable capabilities remain independent of individual processes, and each process owns its operating contract and generated runs.

~~~text
README.md                              # Entry point, setup, operating boundaries, and links to the specifications.
AGENTS.md                              # Repository-wide instructions for people, orchestrators, and delegated agents.

model/                                 # Versioned system-independent and system-specific data contracts.
|-- objects/                           # Financial concepts such as transactions, purchases, journeys, and matters.
|-- systems/                           # Repository, Google Drive, Gmail, and Notion representations.
`-- mappings/                          # Stable identities and relationships between systems and domain objects.

processes/                             # Definitions and lifecycle material for repeatable financial work.
|-- template/                          # Standard used to design and document a new process.
|-- procurement/
|   |-- README.md                      # Purpose, scope, ownership, inputs, outputs, and process status.
|   |-- rules/                         # Durable procurement classification and reconciliation rules.
|   |-- procedures/                    # Human-readable decision flows and operating procedures.
|   |-- runbooks/                      # Machine-readable orchestration and step dependencies.
|   |-- checklists/                    # Start, review, publication, and close gates.
|   |-- schemas/                       # Input, decision, package, audit, and report contracts.
|   |-- registers/                     # Exceptions, unresolved cases, and durable resolutions.
|   `-- subagents/                     # Bounded agent assignments, inputs, outputs, and stop conditions.
|-- recurring-expenses/                # The same process contract for recurring expense reconstruction.
|-- everyday-spending/                 # Receipt-backed and statement-derived everyday spending workflow.
|-- monthly-close/                     # Account coverage, balance controls, and month-end closure.
|-- travel/                            # Journey evidence, personal/work classification, and claims workflow.
|-- matters/                           # Returns, reimbursements, compensation, and other open matters.
`-- tax/                               # Tax-year evidence, classification, filing, and assessment workflow.

skills/                                # Process-independent capabilities that agents can reuse.
|-- source-discovery/                  # Locate evidence without assigning process-specific meaning.
|-- document-extraction/               # Extract structured facts with source locations and confidence.
|-- record-linking/                    # Propose and review cross-system links and monetary allocations.
|-- package-validation/                # Validate schemas, manifests, hashes, totals, and completeness.
`-- publication-review/                # Compare approved packages with destination state before writing.

src/                                   # Shared executable harness used across processes.
|-- acquisition/                       # Fetch indexed Drive files and exported Gmail evidence.
|-- extraction/                        # Provider parsers and normalized evidence readers.
|-- reconciliation/                    # Matching, allocation, exception, and decision utilities.
|-- artifacts/                         # Manifest, lineage, hashing, indexing, and validation code.
|-- publishing/                        # Dry-run, diff, upload, receipt, and recovery adapters.
`-- orchestration/                     # Run creation, task dispatch, gates, resume, and close behavior.

integrations/                          # External-system adapters and their operational configuration.
|-- google-drive/                      # Stable Drive IDs, retrieval, export formats, and cache mapping.
|-- gmail/                             # Message discovery, export, attachment retrieval, and source links.
`-- notion/                            # Baseline capture, projection, dry-run diff, upload, and receipts.

config/                                # Versioned catalogs and settings consumed by shared code and processes.
|-- accounts.yaml                      # Stable account identifiers and provider metadata.
|-- sources.yaml                       # Indexed evidence, native IDs, expected periods, and hashes.
|-- categories.yaml                    # Shared category vocabulary and mappings.
`-- processes/                         # Process-specific configuration that is not generated per run.

cache/                                 # Ignored, replaceable local access to remote evidence.
|-- google-drive/                      # Drive-shaped cache addressed through the source catalog.
`-- gmail/                             # Exported messages and attachments with retained native IDs.

workspaces/                            # Agent execution areas separated by process.
|-- procurement/
|   `-- runs/
|       `-- <run-id>/                  # Generated artifacts for one immutable procurement run.
|           |-- run.json               # Scope, code revision, rule versions, source coverage, and state.
|           |-- inputs/                # Frozen source references and verified input manifests.
|           |-- working/               # Regenerable candidates, parses, and intermediate calculations.
|           |-- decisions/             # Reviewed overrides and resolutions applied in this run.
|           |-- package/               # Validated records proposed for publication.
|           |-- reviews/               # Human and delegated-agent findings and gate decisions.
|           |-- publication/           # Dry-run diff, approval, upload receipt, and verification.
|           `-- report.md              # Final result, coverage, exceptions, and next actions.
|-- recurring-expenses/
|   `-- runs/<run-id>/                 # Generated recurring-expense run artifacts using the same contract.
|-- everyday-spending/
|   `-- runs/<run-id>/
|-- monthly-close/
|   `-- runs/<run-id>/
|-- travel/
|   `-- runs/<run-id>/
|-- matters/
|   `-- runs/<run-id>/
`-- tax/
    `-- runs/<run-id>/

tests/                                 # Contract, parser, reconciliation, replay, and integration tests.
|-- fixtures/                          # Synthetic or safely redacted deterministic test inputs.
|-- unit/                              # Isolated shared-code behavior.
|-- contract/                          # Schema and cross-system invariant checks.
`-- replay/                            # Closed-run reproducibility and regression checks.

migrations/                            # Bounded transitions from legacy paths, schemas, and remote layouts.
archive/                               # Superseded outputs retained only where audit or migration requires them.
~~~

`processes/<process>/` defines how work is designed, executed, reviewed, and maintained. `workspaces/<process>/runs/<run-id>/` contains generated evidence from an execution. A run may update a process rule only through a reviewed change to the process definition; generated findings do not silently become policy.

The current repository still uses `docs/cashflow/processes/` and `data/cashflow/runs/` alongside legacy `finance`, `ingestion`, `automation`, `scripts`, `reports`, and statement paths. Moving those paths into this target layout requires the migration, hash, replay, and path-consumer checks defined in [the existing-system migration](migrations/0001-existing-system.md).

## Cross-system identity

Connect systems through stable identifiers rather than matching paths: account_id, transaction_id, source_id, gmail_message_id, drive_file_id, notion_page_id, order_reference, journey_id, matter_id, claim_reference, and tax_year.

| Information | Primary source |
|---|---|
| Original financial document | Google Drive or original provider |
| Original correspondence | Gmail |
| Normalized transaction and matching result | Repository |
| Exception and resolution history | Repository |
| Current workflow status and dashboards | Notion |
| Import and schema definitions | Repository |
| Notion configuration | Notion, with repository snapshots |

## Relationships that cannot be exact

- One transaction can settle several purchases.
- One purchase can be split across several charges or payment sources.
- A partial refund reverses only part of a purchase.
- An employer reimbursement can be included in payroll without a separately labelled bank transaction.
- A claim can exist without a payment and later produce several payments.
- One email can describe several items while Procurement tracks one card per item.
- One Drive document can support several transactions or matters.
- Notion views, formulas, charts, relations, and automations have no exact filesystem equivalent.
- Drive permissions, comments, versions, and native identities cannot be fully represented in Git.
- Tax classification can be added after the original expense occurred.

These situations require explicit relationships and reconciliation statuses. Unresolved or ambiguous cases remain governed by data/reconciliations/exception_register.md.

## Decisions before migration

1. Should subscriptions be standalone or a subtype of recurring expenses?
2. When should a purchase receive a Procurement card instead of remaining Everyday spending?
3. Should Travel be a Notion database or a matter type linked to Procurement?
4. Should all claims use one Matters database, or should Tax have a dedicated database?
5. When should expected refunds and reimbursements count as receivables?
6. Which original documents should be removed from Git history and retained only in Drive?
7. Should migration preserve current paths temporarily or update all scripts at once?
