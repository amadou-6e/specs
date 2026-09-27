# Single cashflow sheet

Target design: expected movements and all available booked account transactions appear in one Notion dataset. Each expected row keeps its identity when later realized. Existing Notion procurement and recurring databases are historical structures, not proof this target has been implemented.

The builder performs the joins before publication. Notion receives flattened, filterable properties and source links. Optional native relations are navigation aids, never necessary for totals.

| Property | Source and rule |
| --- | --- |
| Entry ID / External transaction ID | Stable entry_id for every row; transaction_id is null while expected and unique when realized |
| Name | Reviewed counterparty/description; never a key |
| Date / Expected date | Booking date for realized entries; expected date for planned entries, with separate fields |
| Amount / Currency | Signed expected amount until realized; then signed booked amount, with currency |
| Account / Institution | Resolved account and provider |
| Counterparty / Reference | Preserve original bank reference; normalized merchant is additional |
| Realization status / Expected basis | Expected requires reviewed commitment or contract basis; realized requires posted transaction |
| Type | Income, expense, refund, transfer, other, unknown |
| Expense category | Single expense, recurring expense, other, unclassified; one primary category |
| Purchase category | Existing detailed categories where supported; Mixed where necessary |
| Personal/work | Personal, work, mixed, unknown |
| Order date / Travel date / Service period | Separate enrichment fields; never replace Date |
| Single expense IDs / Item descriptions | Linked realized single expenses; multiple values retained |
| Single income IDs | Linked realized single income events, when applicable |
| Recurring Expense IDs / names | Linked recurring expenses |
| Recurring Income IDs | Linked recurring income streams, when applicable |
| Receipt links (including income statements) / Statement links | All relevant source references; use rich text with multiple hyperlinks |
| Evidence status / Match status | Missing, partial, verified, ambiguous as applicable |
| Reporting treatment | Include, internal transfer, wallet funding, liability movement, unresolved |
| Run ID / Model version | Publication provenance |

## Amounts and totals

All-transactions views show each observed movement, including transfers. Consolidated spending excludes verified internal transfers and wallet funding to prevent counting the same purchase at both bank and PayPal. Unresolved funding remains visible with a coverage caveat.

Refunds remain positive transactions linked to original purchases, preserving gross, refunded and net figures. Work purchases remain visible but are excluded by the personal view.

Aggregate only like currencies. An optional reporting-currency amount requires a documented conversion source, rate/date and method. Null is not zero.

Mixed-category transactions retain one primary value, Mixed, until an allocation design is approved. Multi-select categories may aid discovery but their filtered totals overlap. Item-level amount totals must use allocations, not repeat the full cashflow amount per item.

Calendar scaffold rows from the old procurement charts are presentation helpers, not transactions. This target adds no fake transaction rows to fill empty days; chart continuity needs separate presentation treatment.

## Publication contract

Validate transaction uniqueness, source links, monetary totals by account/currency and current destination schema. Produce a reviewable create/update/unchanged/conflict diff. Upsert by stable entry_id and enforce transaction uniqueness for realized rows and retain returned page IDs and per-row receipts. Verify rows and totals after publication.

Do not reuse legacy order Date or positive procurement Price as cashflow booking date or signed Amount. The existing uploader needs an explicit new contract before it can publish this sheet.

Expected movements belong in the Cashflow sheet with realization_status expected. Budget and Forecast connect to Cashflow entries. Expected amounts are excluded from realized cash totals; separate views may combine or compare plans and actuals without double counting.
