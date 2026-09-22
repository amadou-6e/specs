# Legacy Model Garden records

This folder preserves imported protocols and evidence whose paths participate in
historical provenance. Structured experiment entries link to these records while
they are migrated. Historical commit URLs and `spec_path` fields remain unchanged.

## Contained elements

```text
legacy/
|-- 1 README.md
|-- 1 template.md
|-- 1 SKILL.md
|-- 0..* <archive-entry>.md
`-- 0..* provenance support directories
```

Ordinary legacy entries are individual Markdown documents created from
[template.md](template.md) using [SKILL.md](SKILL.md). The existing `python/` tree is
a preservation area for imported, identity-bearing records, not a second template or
an active implementation partition. Active protocols belong under
[experiments](../experiments/README.md); current contracts belong under
[subsystems](../subsystems/README.md).
