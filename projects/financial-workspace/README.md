# Financial Workspace

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
financial-workspace/
├── 1 README.md
├── 1 SPECS.md
├── 1 spec.json
├── 1 model/
├── 1 processes/
├── 1 integrations/
├── 1 migrations/
└── 1 decisions/
```
<!-- END GENERATED: contained-elements -->

## Intent

Financial Workspace is the evidence library for personal financial history and future analysis. It keeps original statements and financial documents in stable locations so account balances, cash flow, procurement, liabilities, and tax can be traced back to a source. A stored document is evidence, not a confirmed transaction or a forecast.

Before adding or reorganizing Financial Workspace specifications, read
[SPECS.md](SPECS.md). It defines the project's documentation taxonomy and points to
the live category templates.

The [financial structure](financial-structure.md) is the top-level map of the financial nomenclature and system responsibilities. The [model index](model/README.md) separates financial objects, system representations, and cross-system mappings.

The [live README](https://docs.google.com/document/d/1AtknilGP8OP8VvRN9U08vfABqhC2669euLQ-pjf9tnw/edit) gives the operating instructions for the Drive folder. [model/mappings/cross-system/README.md](model/mappings/cross-system/README.md) describes the current remote structure and the proposed cross-system model. [processes/cash-flow/workflow.md](processes/cash-flow/workflow.md) proposes a portable, reproducible Cash flow workflow with a Drive source index, versioned analysis code and decisions, and a separate Notion publication step. [migrations/0001-existing-system.md](migrations/0001-existing-system.md) specifies migration of the live Notion records, recurring schedules, liabilities, tracked statements, local Drive cache, and tax-year workspaces.

## System roles

- Google Drive stores original statements, receipts, contracts, certificates, and the native Workspace links and README documents.
- The local financial repository holds normalized transactions, reconciliation decisions, exception history, and projected figures with assumptions.
- Notion shows procurement cards, status, and dashboards. Its presentation is not a substitute for source evidence.
- Purchase, travel, and work case documents remain in their subject folders. The native [Workspace links](https://docs.google.com/document/d/14-h2WwcFpFYKDVveGAspKcE4eK-cGz1pRp8R4f1TqUo/edit) document points to the verified purchase and travel areas.

## Operating workflow

1. Collect the original file and record its provider, account, document date, and coverage period.
2. File it by financial category, provider, and year. Keep one original copy of a cross-year document and record its full period.
3. Link the Drive file ID or URL to the related local record. Keep order, travel, payment, and refund dates distinct.
4. Reconcile money movements against the evidence. Confirm a match only when the sources support it, then update local outputs and the relevant Notion view.
5. At monthly close, capture balances and liabilities, review transfers and refunds, and produce historical cash-flow and position snapshots. Label future values as projections and keep their assumptions.

## Evidence and exception rules

Do not infer a payment from an order email or an order from a bank debit alone. Split charges, partial refunds, shared order emails, and date differences need explicit review. Before reporting a financial record as missing, unmatched, excluded, or ambiguous, document the reason, sources searched, approach, and next action in the central `data/reconciliations/exception_register.md` in the financial repository. Update that entry if later evidence resolves it.

Vinted purchase confirmations can support procurement records without a bank or PayPal settlement because internal balance may be used. Preserve the item description and Gmail link; add settlement details when available. Keep reimbursed work travel outside personal procurement. Leave claim evidence with its purchase or journey until a dedicated claims area is established.

## Maintenance

Review new evidence and open exceptions monthly, or during a quarterly catch-up. Keep this README, the live Drive guide, and [model/mappings/cross-system/README.md](model/mappings/cross-system/README.md) aligned when the folder taxonomy or matching rules change. The checked-in [Drive folder example](integrations/google-drive/example/README.md) illustrates the structure with representative original PDFs; native Google Docs are linked from its README.
