# Legacy

Legacy is an expandable collection of single-document historical entries. Every entry
is explicitly non-authoritative and exists only while it retains evidential value.

## Contained elements

```text
legacy/
├── 1 README.md
├── 1 template.md
└── 0..* <historical-topic>.md entries
```

Each entry identifies what it formerly described, when its authority ended, and one
or more active replacements. Active migration instructions remain in the owning
subsystem rather than only in this archive.

Copy [template.md](template.md) to create an entry. The template itself is not a legacy
record.
