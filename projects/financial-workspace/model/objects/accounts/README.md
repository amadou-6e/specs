# Accounts

<!-- BEGIN GENERATED: object-domain-summary -->
> Defines financial accounts and their stable identities independently of provider names, folders, and source systems.

## Domain boundary

**Includes:**

- Stable account identity
- Provider-scoped account references
- Account type and ownership scope
- Currency policy
- Account lifecycle and historical aliases

**Excludes:**

- Posted movements
- Statements and exports
- Balance snapshots
- Provider-specific APIs and export formats
<!-- END GENERATED: object-domain-summary -->

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
accounts/
├── 1 README.md
├── 1 structure.md
├── 1 schema.md or schema/
├── 1 rules.md or rules/
├── 0..1 examples/
└── 0..1 presentation/
```
<!-- END GENERATED: contained-elements -->

## Maturity

Status is **draft**. Implemented coverage varies by process; unsupported fields remain unknown rather than inferred.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
