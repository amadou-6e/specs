# Specification structure

This project follows the [typed and named folder hierarchy](../../shared/conventions/typed_folder_system/README.md), but its categories reflect financial-workspace ownership rather than a generic software-product layout.

## Project layout

```text
financial-workspace/
|-- README.md
|-- SPECS.md
|-- spec.json
|-- model/                    # One cross-system financial model.
|-- processes/                # Repeatable financial workflows.
|-- integrations/             # External-system contracts and examples.
|-- migrations/               # Bounded changes to live data or structure.
`-- decisions/                # Durable choices and their rationale.
```

This category set is closed. Adding or repurposing a top-level category requires updating this file and `spec.json`.

| Category | Structural type | Owns |
| --- | --- | --- |
| `model` | Typed folder collection | Object models, system representations, and mappings between them, each using the shared entry template. |
| `processes` | Expandable folder collection | One independently executable workflow per named folder, with its contract, design, validation, and supporting material. |
| `integrations` | Expandable folder collection | One external system per named folder, including identity, retrieval/publication boundaries, and representative examples. |
| `migrations` | Expandable document collection | Sequentially numbered migration contracts for bounded transitions of live data or structure. |
| `decisions` | Expandable document collection | Sequentially numbered decisions that resolve durable design or operating choices. |

## Category naming

All category identifiers follow the [shared category-naming convention](../../shared/conventions/category_naming.md). Categories name intrinsic, conventionally recognized kinds at a stable abstraction level. Workflow-specific uses belong in process relationships or roles rather than category names.

Financial Workspace examples include `cloud-file-storage`, `email-service`, `git-repository`, and `collaborative-workspace`. Product names such as Google Drive, Gmail, GitHub, and Notion identify system entries, not reusable categories.
## Category rules

- [Model](model/README.md) separates `objects/`, `systems/`, and `mappings/`. All three use `model/template/` as the copyable entry and provide an overview, structure, schema, and rules, with examples and presentation only where useful.
- [Processes](processes/README.md) uses `processes/template/` as its copyable entry. Copy it to a descriptive workflow name.
- [Integrations](integrations/README.md) uses `integrations/template/` as its copyable entry. Copy it to the external system name.
- [Migrations](migrations/README.md) uses `migrations/template.md`; real migrations use sequential names such as `0002-<slug>.md`.
- [Decisions](decisions/README.md) uses `decisions/template.md`; real decisions use sequential names such as `0001-<slug>.md`.

## Placement test

Place a document according to what owns its lifecycle:

- If it defines a financial concept or cross-system invariant, it belongs in `model/`.
- If it teaches an agent or person to perform repeatable work, it belongs in a named `processes/` entry.
- If it defines how Drive, Gmail, Notion, or another external system is addressed, it belongs in a named `integrations/` entry.
- If it describes a one-time or bounded transition, it belongs in `migrations/`.
- If it records why one durable option was selected, it belongs in `decisions/`.

Do not use `architecture/`, `features/`, `contracts/`, or `ui/` as catch-all categories for this project.

## Metadata

Every entry opens with the frontmatter required by the [typed-folder convention](../../shared/conventions/typed_folder_system/README.md#metadata-frontmatter). Allowed statuses are `draft`, `active`, `complete`, `deprecated`, `superseded`, and `template`.
