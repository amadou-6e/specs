# Account

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
account/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
> One owned bank, loan, card or wallet account.

Identity: account_id.

Includes: Institution, account kind, ownership. Optional: Masked native reference, currencies, open/closed dates.

- [Fields](schema.yaml)
- [Relationships](relationships.md)
- [Source forms](representations.md)

These are type definitions; no illustrative instance is claimed as an observed record.

Account balance item records dated balances [1 : 0..*]. Liability is optionally linked via account-liabilities [0..1 : 0..*]; the debt may exist before an account is mapped.
