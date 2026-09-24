# Transaction statement

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
transaction-statement/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
> A dated account report/export.

Identity: statement_id.

Includes: Account, coverage, source representation. Optional: Opening/closing balances, issue date, revision.

- [Fields](schema.yaml)
- [Relationships](relationships.md)
- [Source forms](representations.md)

These are type definitions; no illustrative instance is claimed as an observed record.

Opening and closing balance fields remain observed source summaries. They can substantiate Balance item records; do not count both as separate positions.
