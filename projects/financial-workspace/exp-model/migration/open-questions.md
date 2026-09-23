# Decisions still needed before promotion

- Destination: reuse an existing Notion dataset or create a new transaction dataset; capture live schema first.
- Mixed-category amounts: keep Mixed, or add explicit per-category amount columns/another allocation presentation.
- Receipt-only procurement: retain a linked procurement view alongside actual cashflow; do not invent movements.
- Accounts with absent statements and non-booked transactions: define completeness per account/period.
- Income and liability breakdown: preserve observed net transactions; model gross/deductions or principal/interest only with sufficient evidence.
- Cross-currency allocation and account funding: approve reporting conversion and residual-review policy before automated totals.

Resolved here: one row per booked transaction per sheet; receipt formats are representations; recurring occurrences are distinct from agreements; multi-item purchases use item identities; many-to-many monetary links require reviewed allocation records.
