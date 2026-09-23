# Financial processes

## Contained elements

```text
processes/
├── 1 README.md
├── 1 template/
└── 0..* <process>/ entries
```
Structural type: expandable folder collection.

Each child folder specifies one repeatable workflow that a person or agent can execute without relying on conversation history. Process entries own their inputs, outputs, invariants, decision flow, validation, and maintenance contract. Generated run artifacts live in the financial repository, not in this specification repository.

```text
processes/
|-- README.md   1
|-- template/   1
`-- <process>/ 0..*
```

Every named process is copied from `template/` and contains:

```text
<process>/
|-- README.md    1
|-- workflow.md  1
`-- examples/   0..1
```

Current entry: [cash-flow](cash-flow/README.md).
