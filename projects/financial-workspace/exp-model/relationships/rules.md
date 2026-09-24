# Relationships

Canonical edges and cardinalities are in graph.yaml. targets_per_source counts targets for ONE source; sources_per_target counts sources for ONE target.

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| agreement-terms | recurring-payment-agreement | agreement-term | 0..* | 1 |
| income-statement-items | income-statement | income-statement-item | 0..* | 1 |
| account-balance-items | account | account-balance-item | 0..* | 1 |
| statement-balance-items | transaction-statement | account-balance-item | 0..* | 0..* |
| account-liabilities | account | liability | 0..* | 0..1 |
| provides | financial-institution | account | 0..* | 1 |
| issues-for | account | transaction-statement | 0..* | 1 |
| records | account | transaction | 0..* | 1 |
| contains | transaction-statement | transaction | 0..* | 0..* |
| issues | employer | income-statement | 0..* | 1 |
| substantiates-income | income-statement | transaction | 0..* | 0..* |
| defines | recurring-payment-agreement | recurring-payment-occurrence | 0..* | 1 |
| settles-occurrence | transaction | recurring-payment-occurrence | 0..* | 0..* |
| settles-procurement | transaction | procurement | 0..* | 0..* |
| contains-item | procurement | procurement-item | 0..* | 1 |
| substantiates-purchase | receipt | procurement | 0..* | 0..* |
| supports-occurrence | receipt | recurring-payment-occurrence | 0..* | 0..* |
| contains-entry | cashflow-sheet | cashflow-entry | 0..* | 1 |
| projects | cashflow-entry | transaction | 1 | 0..* |
| supported-by-receipt | cashflow-entry | receipt | 0..* | 0..* |
| refunds | transaction | transaction | 0..* | 0..* |

A statement can be empty; multiple overlapping statements can mention one transaction. A receipt may be unassigned during review, and a procurement can lack a receipt while evidence is incomplete. Publishing cashflow requires transaction evidence, not a receipt.

## Relationship record

Retain link_id, edge type, source_id, target_id, state (candidate/verified/rejected), evidence references, rationale, reviewer/rule version and decision time. Candidate matches never imply verified settlement.

Monetary settlements retain allocation_id, transaction_id, target kind/ID, allocated_amount, currency and role (payment/refund). Store the magnitude with explicit role, preserving transaction sign separately. For a fully allocated movement, allocations within one allocation dimension equal its magnitude. Partial allocation retains a visible residual. Do not add order-level and item-level allocations together: they are alternative detail levels of the same payment. Never allocate across currencies without explicit conversion evidence.

Receipt links on cashflow entries are derived from reviewed source links. Enrichment references procurement IDs, item IDs, agreement/occurrence IDs and income statement IDs. They do not constitute new payments.

## Lifecycle

Evidence deletion or missing access marks a gap; it does not delete a financial transaction. Corrected observations supersede prior assertions. Rejected links remain auditable. Actual records are not cascade-deleted when a receipt, agreement or Notion page disappears.
