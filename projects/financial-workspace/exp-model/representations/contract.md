# Source forms and extraction

Financial meaning, delivery channel and encoding are independent. A receipt is a business document; PDF is a format; Gmail and Google Drive are storage systems. Even transaction inputs vary by provider and export. Do not assume one universal statement schema.

| Object | Source forms | Extraction and verification |
| --- | --- | --- |
| Transaction / statement | Native PDF, scanned PDF, CSV/XLSX export, provider data | Preserve original columns/text, account, source row or PDF page, debit/credit convention and booking/value dates. Reconcile statement totals when available. |
| Receipt | Plain-text or HTML email, PDF attachment, standalone PDF, receipt image/scan | Extract issuer, references, items, currency, totals and dates. OCR results require evidence review; locale and decimal conventions are explicit. |
| Procurement / travel | Confirmation email, invoice, ticket PDF, calendar attachment (.ics) | Combine documents using verified references. Calendar/ticket evidence supplies travel date and endpoints; mail sent date is not travel date. |
| Commitment | Contract PDF, scan, renewal email, provider notice | Retain effective terms and amendments. Repeated payments can suggest recurrence but cannot fabricate a contract. |
| Income statement | Payslip PDF/scan, employer export or reimbursement report | Keep gross, deductions, net and reimbursements distinct; link actual payment separately. |
| Cashflow entry | Notion row plus local publication package | Generated from transaction and reviewed enrichment; never re-parse a display title to recover canonical identity. |

## Source representation record

Each representation retains representation_id, system, native_id, native_url/location, media_type, observed_at and retrieval status. Captured bytes also retain SHA-256, extraction tool/version and extraction time. Gmail attachments retain parent message ID and attachment/part identity. Local cache paths are replaceable conveniences.

A separate field assertion records object_id, field path, value, representation_id, locator (page/row/MIME part/line), method (structured/text/OCR/manual), review state and correction history. Do not label an entire document reliable merely because one field was verified.

Multiple representations may support one object. One representation may support multiple objects. Delivery within an email does not by itself establish that every attachment concerns the same order.

## Convergence into cashflow

1. Retrieve and identify the original source; retain its location and capture metadata.
2. Extract source assertions without filling missing values by guess.
3. Normalize dates, decimals, currency and provider signs while preserving original values.
4. Resolve object identity and duplicates across statements, emails and attachments.
5. Review links and allocations. Store conflicting values and unresolved candidates.
6. Project one booked transaction into one cashflow row with reviewed document enrichment.

Missing receipts do not block a verified transaction row. Receipt-only purchases remain procurement records until settlement is evidenced. For Vinted this preserves the existing receipt-only procurement exception; it does not fabricate an internal-wallet transaction.

Evidence priority is field-specific: bank/wallet evidence supplies booked amount and payment date; purchase documents supply order/items; tickets supply itinerary; contracts supply expected terms; payslips supply income breakdown. Conflicts remain visible rather than being silently overwritten.
