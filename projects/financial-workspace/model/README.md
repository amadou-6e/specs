# Financial models

Cardinality: README.md 1, objects/ 1, systems/ 1, mappings/ 1, template/ 1.

The model is divided by semantic role. Objects define financial meaning, systems define concrete representations, and mappings connect identities and facts across those systems. Use [template](template/README.md) and its [skill](template/SKILL.md) inside any of the three catalogues.

```text
model/
|-- objects/            # System-independent financial concepts and semantics.
|   |-- accounts/
|   |-- transactions/
|   |-- procurement/
|   |-- recurring-expenses/
|   |-- everyday-spending/
|   |-- travel/
|   |-- matters/
|   |-- tax/
|   |-- financial-position/
|   |-- evidence/
|   `-- reconciliation/
|-- systems/            # Representations owned by concrete storage or operating systems.
|   |-- repository/
|   |-- google-drive/
|   |-- gmail/
|   `-- notion/
|-- mappings/           # Identities, authority, and transformations spanning boundaries.
|   `-- cross-system/
`-- template/           # Shared structure for an entry in any catalogue.
```

Every entry uses `README.md`, `structure.md`, `schema.md`, and `rules.md`. Examples and presentation are optional. Start with a file and expand it into a folder only when several independently useful documents justify it.

Cite evidence and observation dates beside supported claims or in the owning document's Basis section. Validation procedures and historical check records belong to the relevant process or integration and are linked from the model.

## Current catalogues

| Catalogue | Entry | Owned boundary |
| --- | --- | --- |
| Objects | [Financial object domains](objects/README.md) | Accounts, transactions, procurement, recurring expenses, everyday spending, travel, matters, tax, financial position, evidence, and reconciliation. |
| Systems | [Repository](systems/repository/README.md) | Canonical data, code, cache, process workspaces, and generated run artifacts. |
| Systems | [Google Drive](systems/google-drive/README.md) | Original documents, Drive identity, folder semantics, and evidence access. |
| Systems | [Gmail](systems/gmail/README.md) | Correspondence, message and attachment identity, retrieval, and evidence semantics. |
| Systems | [Notion](systems/notion/README.md) | Operational databases, presentation, baselines, and controlled publication. |
| Mappings | [Cross-system](mappings/cross-system/README.md) | Shared identities, authority boundaries, handoffs, and mappings between objects and systems. |