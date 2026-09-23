# Object definitions

This is the candidate replacement catalogue. Each object has a stable internal ID; names, amounts, paths and dates are attributes, not identities. Unknown values remain null. Money uses exact decimal strings and an explicit currency. Source observations and reviewed corrections remain traceable.

| Object | Meaning and identity | Required information | Optional enrichment |
| --- | --- | --- | --- |
| Financial institution | Provider of an account; institution_id | Name | Provider identifiers |
| Account | One owned bank, loan, card or wallet account; account_id | Institution, account kind, ownership | Masked native reference, currencies, open/closed dates |
| Transaction statement | A dated account report/export; statement_id | Account, coverage, source representation | Opening/closing balances, issue date, revision |
| Transaction | One booked movement on one account; transaction_id | Account, signed amount, currency, booking date, source observation | Value date, merchant, original reference, provider transaction ID |
| Employer | Issuer of employment income evidence; employer_id | Name | Provider/employment references |
| Income statement | One payslip or employer payment statement; income_statement_id | Employer, period, source | Gross/net amounts, deductions, reimbursement component |
| Recurring-payment agreement | Continuing commitment; agreement_id | Provider, service description, source or reviewed basis | Cadence, effective dates, versioned price terms |
| Recurring-payment occurrence | One expected instalment/service period; occurrence_id | Agreement, period or due date | Expected amount, observed settlement state |
| Procurement | One order/acquisition, regardless of payment splits; procurement_id | Merchant, order date when known, source | Merchant order reference, order total, travel details |
| Procurement item | One identifiable line in an acquisition; item_id | Procurement, description, quantity | Unit/line amount, category, receipt line |
| Receipt | Purchase-related document in the broad workspace sense; receipt_id | Document kind, source representation | Issuer, order/document reference, issue date, items, total, currency |
| Cashflow sheet | Destination dataset in Notion; sheet_id | Workspace/database/data-source identity and schema version | Views and chart configuration |
| Cashflow entry | One transaction projected into a sheet; entry_id | Sheet, transaction, flattened reporting properties | Receipt, procurement, agreement and income details |

Receipt kinds distinguish order confirmation, invoice, paid receipt, refund confirmation and booking confirmation. An invoice or order confirmation does not prove settlement. A refund request may be retained as correspondence but is not a posted refund.

A loan account supports current liabilities through its statements/balances. Loan repayments are cash outflows; do not label the entire payment consumption expense or infer principal/interest without evidence. Investments, tax, cash and manual undocumented purchases remain outside the expansion.

## Identity and lifecycle

- Scope provider transaction IDs by institution/account. If absent, assign a persistent internal ID and retain the source row/page locator. Amount + date + merchant is only a matching candidate.
- Overlapping statements and revised exports add observations of an existing transaction after review; they do not automatically create new movements.
- Procurement item IDs persist across re-extractions; Gmail message ID alone is insufficient for multi-item orders.
- A receipt identity is distinct from the identities of its email and attachment. Different files can represent the same document; one email can contain several documents.
- Cashflow entry uniqueness is (sheet_id, transaction_id). Retain Notion page ID separately. Repeated publication updates the same entry.
- Keep extraction, matching, procurement approval and publication states separate. Pending procurement is not a booked transaction.
