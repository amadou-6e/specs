# Replacement plan

The candidate is intended to replace the old domain catalogue after evidence and consumer checks. System layouts, source references and historical observations remain authoritative in their existing locations until migrated.

| Current entry | Candidate destination |
| --- | --- |
| accounts | Account and Financial institution |
| transactions | Transaction and Transaction statement |
| procurement | Single expense, Single expense item and Receipt |
| recurring-expenses | Commitment, versioned terms and Occurrence |
| everyday-spending | Classification of a transaction; new manual capture excluded |
| travel | Single expense attributes and document assertions, including itinerary |
| financial-position | Balance item; Liability for debts; broader assets deferred |
| reconciliation | Reviewed relationships and allocations, plus process rules |
| cross-system mappings | Representation IDs, field assertions, publication identity |
| Notion procurement rows | Preserve original item identities; map settlements to transaction rows |
| Notion recurring rows | Agreements/occurrences enrich the same transaction sheet |

## Promotion gates

1. Inventory old fields, process consumers and source references; record each migration disposition.
2. Validate the historical scenarios in validation-cases.md against local evidence.
3. Reconcile one closed period by account and currency, including unmatched transactions, refunds and wallet funding.
4. Capture the current Notion schema and IDs; produce a dry-run mapping of old rows and new transaction entries.
5. Verify no order/item duplicates cash flow, no source links are lost and no receipt-only record acquires an invented payment.
6. Review the replacement; update model catalogues, templates, processes and publication schema together.
7. Retire old contracts only after replay and consumer checks pass.

No migration or remote update is executed by this specification change.

## Approved nomenclature change

The candidate now uses Recurring expense (recurring-expense), Commitment term (commitment-term), and Payment occurrence (payment-occurrence). The previous object names were Recurring-payment agreement, Agreement term, and Recurring-payment occurrence. References formerly named agreement_id/agreement_ids/agreement_names become recurring_expense_id/recurring_expense_ids/recurring_expense_names; existing identity values are preserved. term_id and occurrence_id remain stable. Both child relationships remain [1 : 0..*]. This is a specification rename, not a migration of published Notion records.

The candidate now names the former recurring-commitment object Recurring expense and its reference fields recurring_expense_id/recurring_expense_ids. Stored identity values remain stable; the rename is not a live Notion migration. Recurring income is a new Employer-owned object. Income statements and cashflow entries link to it optionally, so historical and one-off income remain valid.

## Single-event and planning transition

Single expense replaces the candidate Procurement object, and Single expense item replaces Procurement item. The existing procurement workflow, Drive folders, and Notion database keep their current names. Preserve existing identifiers as migration aliases; no live records are renamed by this spec. Single income adds one-off receipts. Budget and Forecast are planned allocations, optionally account-scoped. Planned events remain outside the transaction-backed cashflow sheet until a posted transaction is matched.

An Income statement is now a Receipt with document_kind income-statement. Preserve prior income_statement_id values by mapping them to stable receipt_id values before loading data; rekey Income statement items to receipt_id. The former Income statement object has no independent identity in the candidate model.
Legacy income_statement_links values migrate into receipt_links after deduplication by Receipt identity. The target Cashflow entry has one receipt_links field.
