---
title: Google Drive financial evidence integration
status: draft
kind: integration
owners:
  - amadou-6e
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related:
  - model/mappings/cross-system
---

# Google Drive integration

Google Drive is authoritative for original statements, receipts, contracts, certificates, and native workspace navigation documents. Repository records refer to Drive content through stable file IDs, links, metadata, expected hashes, and documented coverage.

```text
google-drive/
|-- README.md  1
`-- example/   0..1
```

The [example](example/README.md) illustrates the Drive hierarchy with representative files. It is not a cache or source of truth. A runtime cache belongs in the financial repository and must remain reproducible from the Drive index.
