# Validation

This record maps consequential guarantees to evidence and distinguishes current checks from historical artifact results.

| Guarantee | Evidence/check | Result | Scope |
| --- | --- | --- | --- |
| Cash Flow topology preserved | `contract/cash-flow-schema.md` | Page, database, and data-source IDs for Cash Flow, Procurement, Recurring expenses, and Liabilities recorded | Dated 2026-09-14 |
| Procurement schema preserved | Schema contract versus migration/import artifacts | Operational and helper fields, vocabularies, currency behavior, and explicit unknown native types recorded | Dated local evidence |
| Procurement presentation preserved | `views/cash-flow.md` versus Kanban/unified configuration | Workflow first, 12 category tables, four chart elements, tab sets, filters, placements, and helper behavior recorded | Dated 2026-09-09 |
| Recurring/Liabilities schemas | Fresh schema capture | IDs known; property/view schemas absent locally and explicitly open | Blocks reconstruction |
| Structure and links | python tools/validate_specs.py from specs | Run after editing; handoff records result | Specification only |
| Native/external identity separation | IDs config, migration 0001, receipt, plan | Document review passed | Historical/local |
| Legacy coverage | 2026-09-08 manifest/README | 260 rows, 12 databases, complete pagination, five hashes | Legacy only |
| Duplicate prevention | Validator invocation in run audit | Historical exit 0; four skip_existing | Five-identity baseline |
| Identity uniqueness | Representative audit | Historical checks true | Test run only |
| Approval gate | Audit and procedures | Publication remained not_run | No writer validation |
| Migration preservation | 2026-09-09 receipt | 260 IDs, zero missing/mismatches, four repaired links | Not replayed |
| Current remote state/schema | Fresh Notion inspection | Not run by instruction | Blocks publication |
| Idempotent update/recovery | Writer integration test | Cash-flow/recurring writers absent; Procurement writer not exercised | Open gap |
| Presentation round trip | Provider export/import comparison | Not run; exact round trip unsupported | Open gap |

The named local specifications, configs, migration records, snapshot manifest, code, procedures, and run artifacts were reconciled. Branch, commit, and working-tree state were inspected without external access. Material gaps are no fresh baseline or permission/schema check, no end-to-end receipt, no update/recovery test, and no proof historical assertions still match Notion. These keep status draft and block publication.
