# Financial integrations

## Contained elements

```text
integrations/
├── 1 README.md
├── 1 template/
└── 0..* <integration>/ entries
```
Structural type: expandable folder collection.

Each child folder specifies one external system's identity model, access boundary, source-of-truth role, retrieval or publication behavior, and local-cache representation.

```text
integrations/
|-- README.md      1
|-- template/      1
`-- <integration>/ 0..*
```

Every integration entry contains one `README.md`; it may also contain an `example/` folder with representative, non-authoritative material. Current entry: [google-drive](google-drive/README.md). Gmail and Notion entries should be added when their contracts are specified rather than inferred from incidental scripts.
