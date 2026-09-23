# Specification structure

This project's guide for placing specifications, per the
[typed and named folder hierarchy](../../shared/conventions/typed_folder_system/README.md)
convention.

## Project layout

```text
financial-workspace/
├── README.md
├── SPECS.md
├── spec.json
├── architecture/
└── decisions/
```

This category set is closed. Categories have one of three structural types:

| Type | Expansion rule | Template rule | Categories |
| --- | --- | --- | --- |
| Fixed top-structured | One system-wide structure. | `template.md` optional; not used here. | `architecture` |
| Expandable document collection | Each entry is one independently owned Markdown document. | One copyable `template.md`. | `decisions` |

## Architecture

Fixed top-structured. The cross-system financial data model, the reproducible
cash-flow workflow, and the existing-system migration contracts. See
[architecture/README.md](architecture/README.md).

## Decisions

Expandable document collection. Copy `decisions/template.md` to a sequentially
numbered filename for a new decision. See the
[category container](decisions/README.md) — no real decisions are recorded yet.

## Metadata

Every entry opens with the frontmatter block defined in the
[typed and named folder hierarchy](../../shared/conventions/typed_folder_system/README.md#metadata-frontmatter)
convention. Allowed `status` values here are `draft`, `active`, `complete`,
`deprecated`, `superseded`, and `template`.
