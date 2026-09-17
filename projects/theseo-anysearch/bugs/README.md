# Bugs

Bugs is an expandable collection of single-document defect records with durable
diagnostic or design value. GitHub issues remain authoritative for work status.

## Contained elements

```text
bugs/
├── 1 README.md
├── 1 template.md
└── 0..* <bug>.md entries
```

Each entry links at least one GitHub issue and at least one violated subsystem
contract. It may link affected implementation partitions, one fixing pull request,
and regression verification. Ordinary defects need only a GitHub issue.

Copy [template.md](template.md) to create an entry. The template itself is not a bug
record.
