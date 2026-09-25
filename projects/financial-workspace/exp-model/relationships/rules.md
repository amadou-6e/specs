# Relationships

Canonical edges and cardinalities are in graph.yaml. targets_per_source counts targets for ONE source; sources_per_target counts sources for ONE target.

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| commitment-terms | recurring-expense | commitment-term | 0..* | 1 |
| income-statement-items | income-statement | income-statement-item | 0..* | 1 |
| account-balance-items | account | balance-item | 0..* | 0..1 |
| liability-balance-items | liability | balance-item | 0..* | 0..1 |
| liability-terms | liability | liability-term | 0..* | 1 |
| statement-balance-items | transaction-statement | balance-item | 0..* | 0..* |
| account-liabilities | account | liability | 0..* | 0..1 |
| provides | financial-institution | account | 0..* | 1 |
| issues-for | account | transaction-statement | 0..* | 1 |
| records | account | transaction | 0..* | 1 |
| contains | transaction-statement | transaction | 0..* | 0..* |
| issues | employer | income-statement | 0..* | 1 |
| employer-recurring-income | employer | recurring-income | 0..* | 1 |
| recurring-income-statements | recurring-income | income-statement | 0..* | 0..1 |
| recurring-income-entries | recurring-income | cashflow-entry | 0..* | 0..* |
| substantiates-income | income-statement | transaction | 0..* | 0..* |
| defines | recurring-expense | payment-occurrence | 0..* | 1 |
| settles-occurrence | transaction | payment-occurrence | 0..* | 0..* |
| settles-single-expense | transaction | single-expense | 0..* | 0..* |
| contains-item | single-expense | single-expense-item | 0..* | 1 |
| substantiates-purchase | receipt | single-expense | 0..* | 0..* |
| supports-occurrence | receipt | payment-occurrence | 0..* | 0..* |
| contains-entry | cashflow-sheet | cashflow-entry | 0..* | 1 |
| projects | cashflow-entry | transaction | 1 | 0..* |
| supported-by-receipt | cashflow-entry | receipt | 0..* | 0..* |
| refunds | transaction | transaction | 0..* | 0..* |
| settles-single-income | transaction | single-income | 0..* | 0..* |
| supports-single-income | income-statement | single-income | 0..* | 0..* |
| account-budgets | account | budget | 0..* | 0..1 |
| account-forecasts | account | forecast | 0..* | 0..1 |
| single-expense-budgets | budget | single-expense | 0..* | 0..* |
| single-income-budgets | budget | single-income | 0..* | 0..* |
| single-expense-forecasts | forecast | single-expense | 0..* | 0..* |
| single-income-forecasts | forecast | single-income | 0..* | 0..* |
| documents-expense-item | receipt | single-expense-item | 0..* | 0..* |
| statement-item-supports-single-income | income-statement-item | single-income | 0..* | 0..* |
| reimburses-single-expense | single-income | single-expense | 0..* | 0..* |
| reimburses-single-expense-item | single-income | single-expense-item | 0..* | 0..* |

A statement can be empty; multiple overlapping statements can mention one transaction. A receipt may be unassigned during review, and a single expense can lack a receipt while evidence is incomplete. Publishing cashflow requires transaction evidence, not a receipt.

## Relationship record

Retain link_id, edge type, source_id, target_id, state (candidate/verified/rejected), evidence references, rationale, reviewer/rule version and decision time. Candidate matches never imply verified settlement.

Monetary settlements retain allocation_id, transaction_id, target kind/ID, allocated_amount, currency and role (payment/refund). Store the magnitude with explicit role, preserving transaction sign separately. For a fully allocated movement, allocations within one allocation dimension equal its magnitude. Partial allocation retains a visible residual. Do not add order-level and item-level allocations together: they are alternative detail levels of the same payment. Never allocate across currencies without explicit conversion evidence.

Receipt links on cashflow entries are derived from reviewed source links. Enrichment references single-expense IDs, item IDs, commitment/occurrence IDs and income statement IDs. They do not constitute new payments.

## Lifecycle

Evidence deletion or missing access marks a gap; it does not delete a financial transaction. Corrected observations supersede prior assertions. Rejected links remain auditable. Actual records are not cascade-deleted when a receipt, commitment or Notion page disappears.

Planned Single income and Single expense records may lack transactions. Their budgets and forecasts are planning links. A cashflow entry still requires a posted transaction; one event may settle through several transactions.

A Single expense can have zero or more Single expense items and can be supported by receipts. A receipt may document the whole expense or particular items. A reviewed reimbursement Income statement item can support a reimbursement-kind Single income, which references the expense or specific items. Retain an allocation amount and currency when one salary line covers several expenses. The sum of verified expense allocations must not exceed the reviewed reimbursement Single income amount. Do not count the same reimbursement at both parent and item level. The linked salary transaction remains one cashflow movement.