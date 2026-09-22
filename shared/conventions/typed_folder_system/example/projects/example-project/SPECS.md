# Specification structure

This is the example project's guide for placing specifications. It exists only to
demonstrate the [typed and named folder hierarchy](../../../README.md) convention.

## Project layout

```text
example-project/
├── README.md
├── SPECS.md
├── spec.json
├── architecture/
├── subsystems/
└── decisions/
```

This category set is closed. Categories have one of three structural types:

| Type | Expansion rule | Template rule | Categories |
| --- | --- | --- | --- |
| Fixed top-structured | One system-wide structure. | `template.md` optional; not used here. | `architecture` |
| Expandable folder collection | Each entry is an independently owned multi-file folder. | One copyable `template/` folder. | `subsystems` |
| Expandable document collection | Each entry is one independently owned Markdown document. | One copyable `template.md`. | `decisions` |

## Architecture

Fixed top-structured. See [architecture/README.md](architecture/README.md).

## Subsystems

Expandable folder collection. Copy `subsystems/template/` and rename the copy for a
new subsystem. See the [live example](subsystems/widget-store/README.md) and the
[category container](subsystems/README.md).

## Decisions

Expandable document collection. Copy `decisions/template.md` to a sequentially
numbered filename for a new decision. See the
[live example](decisions/0001-use-sqlite-for-cache.md) and the
[category container](decisions/README.md).

## Metadata

Every entry opens with the frontmatter block defined in the
[typed and named folder hierarchy](../../../README.md#metadata-frontmatter)
convention. Allowed `status` values here are `draft`, `active`, `complete`,
`deprecated`, `superseded`, and `template`.
