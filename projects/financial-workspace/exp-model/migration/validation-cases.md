# Historical checks for the candidate

These are acceptance scenarios grounded in prior rules and the exception register, not newly verified source extracts or completed test results.

| Case | Required outcome |
| --- | --- |
| Amazon order 303-7581825-5753936 | Two debits (121.92 and 55.89 EUR) and two refunds (62.36 and 55.89 EUR) produce four cashflow rows and net spending 59.56 EUR; retain one order and its item identities. |
| Amazon order 303-6256092-0210767 | Three debits (15.99, 41.98, 9.99 EUR) total 67.96 EUR; each movement appears once. |
| Vinted receipt-only cases | Procurement and receipt retained; cashflow settlement absent until evidence exists. |
| Temu PO-076-18990601027191094 | Preserve 63.63 EUR order value, 64.01 EUR debit and separate 50.19/13.82 EUR refunds. Retain reviewed 0.38 EUR discrepancy; do not generalize it into tolerance. |
| DB calendar attachments | Extract itinerary from .ics; retain travel date, order date and payment date separately. |
| Employer work exclusions | Work travel remains in all-transactions view with work classification, excluded from personal spending; reimbursements link without overwriting original payments. |
| Statement exported twice | Same movements resolve to existing IDs; duplicate import creates no additional rows. |
| Receipt PDF plus email copy | Two representations may support one document; evidence duplication adds no transaction. |
| Changed recurring charge | Version commitment terms; actual booked amount remains authoritative for cash flow. |
| Bank funding PayPal | Retain observed bank and wallet movements, exclude verified funding from consolidated spending, count merchant settlement once. |

## Sources

- [Procurement rules](../../../../../financial-workspace/docs/cashflow/processes/procurement/rules/procurement.md)
- [Exception register](../../../../../financial-workspace/docs/cashflow/processes/procurement/registers/exceptions.md)
- [Existing Notion contract](../../model/systems/notion/schema.md)
- [Recurring model](../../model/objects/recurring-expenses/schema.md)

The existing recurring model supplies service, service period and effective contract terms. It does not prove that every recurring commitment or payment has been captured.
