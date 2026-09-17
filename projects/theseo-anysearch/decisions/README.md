# Decisions

Decisions is an expandable collection of single-document decision records. Accepted
decisions normatively record durable choices and their rationale.

## Contained elements

```text
decisions/
├── 1 README.md
├── 1 template.md
└── 0..* <number>-<decision>.md entries
```

Each record has one lifecycle state and may affect one or more other specification
entries. A record may supersede zero or more earlier decisions and may itself be
superseded by at most one current decision.

Copy [template.md](template.md) and assign the next number to create an entry. The
template itself is not a decision record.
