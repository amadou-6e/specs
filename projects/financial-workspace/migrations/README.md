# Financial workspace migrations

## Contained elements

```text
migrations/
├── 1 README.md
├── 1 template.md
└── 0..* <NNNN>-<slug>.md entries
```
Structural type: expandable document collection.

Each entry is one bounded transition of live records, schemas, folders, or integrations. Migration documents define the source state, target state, stable identities, transformation, validation, rollback or recovery strategy, and completion evidence.

```text
migrations/
|-- README.md          1
|-- template.md        1
`-- NNNN-<slug>.md    0..*
```

Entries use four-digit sequential prefixes. Current entry: [0001-existing-system.md](0001-existing-system.md).
