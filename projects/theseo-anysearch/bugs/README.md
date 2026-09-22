# Bugs

Bugs is an expandable collection of single-document defect records with durable
diagnostic or design value. GitHub issues remain authoritative for work status.

## Contained elements

```text
bugs/
├── 1 README.md
├── 1 SKILL.md
├── 1 template.md
└── 0..* <bug>.md entries
```

`SKILL.md` defines how to decide whether a durable record belongs here and how to
research, write, verify, update, and close one. `template.md` is the directly copyable
shape for one record. Neither file is itself a bug entry.

Each `<bug>.md` entry is one durable defect record. It links at least one GitHub issue
and normally links the violated subsystem contract. When the required behavior has
not yet been incorporated into a subsystem contract, the entry identifies and links
its actual authority and records the missing contract as follow-up work. It may link
affected implementation partitions, a fixing pull request, and regression evidence.
Ordinary defects need only a GitHub issue.

## Authority and lifecycle

Bug records preserve durable diagnostic evidence; they do not own work status,
priority, assignment, or implementation scope. GitHub owns those concerns. The
subsystem contract, accepted decision, product requirement, business rule, or other
explicitly identified authority owns expected behavior.

Copied entries use `kind: bug` and one of these lifecycle values:
`reported`, `confirmed`, `fix-in-progress`, `resolved`, `not-reproducible`, or
`superseded`. The template itself uses `status: template`. A `resolved` record remains
available and names the regression evidence that supports resolution. A
`not-reproducible` record states what was tested and what uncertainty remains. A
`superseded` record links its replacement.

## Creating and reviewing an entry

1. Read [SKILL.md](SKILL.md) and confirm that the defect has lasting diagnostic or
   design value.
2. Copy [template.md](template.md) to a descriptive Markdown filename in this
   directory; do not create an entry folder.
3. Replace all placeholders, change `status: template` to the appropriate bug
   lifecycle value, and preserve one-to-one ordering between observed and expected
   behavior bullets.
4. Link evidence for observations, authority for expectations, the owning GitHub
   issue, and available fix and regression records.
5. Run the specification validator and review the record again whenever its lifecycle
   changes.
