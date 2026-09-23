# Typed and named folder hierarchy

This convention explains how a project under `projects/<project>/` organizes its
specifications: a small closed set of top-level **categories**, each assigned one of
three **structural types**, and — inside an expandable category — new **entries**
created by copying that category's **template** and renaming the copy. "Typed"
refers to the structural type a category is assigned; "named" refers to the entry
created from a template.

This document describes the mechanism generically. A project's own `SPECS.md` (for
example `projects/theseo-anysearch/SPECS.md`) picks the concrete set of categories it
uses, assigns each one a structural type, and links its live templates. Different
projects may use different category subsets (compare
[theseo-anysearch/SPECS.md](../../../projects/theseo-anysearch/SPECS.md), which has
nine categories, against
[theseo-world-providers/SPECS.md](../../../projects/theseo-world-providers/SPECS.md),
which has five) — the structural-type mechanism itself does not change. This
convention is not about spec-status lifecycle
([`../spec_lifecycle.md`](../spec_lifecycle.md) covers `draft`/`review`/`accepted`/etc.
and is orthogonal to it).

A runnable, minimal instance of this system lives in [`example/`](example/) next to
this document, together with [`validate_example.py`](validate_example.py), which
checks that instance against the rules below.

## The three structural types

| Structural type | Expansion rule | Template rule |
| --- | --- | --- |
| **Fixed top-structured** | The category has one system-wide structure. Focused documents or named partitions may be added only within that declared structure — contributors do not create arbitrary new top-level partitions. | A `template.md` is optional. Fixed partitions do not use copyable templates. |
| **Expandable folder collection** | Each new entry is an independently owned, multi-file folder following one stable entry schema. | One directly copyable `<category>/template/` folder. No example-name layer beneath it — the template folder itself is copied and renamed. |
| **Expandable document collection** | Each new entry is one independently owned Markdown document. | One directly copyable `<category>/template.md`. |

A folder collection may declare one intermediate set of named `groups` in
`spec.json` when entries have different semantic roles but share one entry schema. Each
group is a container with its own `README.md` and cardinality statement. Entries remain
direct children of a declared group, and the category still has one copyable `template/`.
Groups organize entries; they are not entries themselves and cannot introduce a second
entry schema.

"Expandable" applies to entries within a category, never to the top-level category
set itself, which a project's `SPECS.md` declares closed: adding, renaming, or
repurposing a category requires revising that document and reviewing the ownership
effects it has on other categories. A template is a realistic, populated example —
not an empty file or an abstract directory tree — so copying it and filling in the
specifics is faster than writing an entry from nothing.

## Creating a new named entry

1. Copy the category's template (`<category>/template/` or `<category>/template.md`).
2. Rename the copy to the new entry's name (a folder collection entry is renamed
   directly; a document collection entry typically gets a sequential prefix, e.g.
   `decisions/0001-<slug>.md`).
3. Replace the template's `status: template` frontmatter value and its example
   content with the real entry's content. Do not nest a copied template folder
   beneath another template folder, and do not add an extra naming layer between the
   category and the entry.

## Container and entry documentation

Every directory that organizes child specification elements is a **container** and
must have a `README.md` with a `## Contained elements` section. That section contains
a fenced tree, following the form used by the worked example, and states:

- the permitted child shapes and filenames;
- the cardinality of required, optional, and repeatable elements using `1`, `0..1`,
  and `0..*`; and
- which file or folder is the copyable template where the collection is expandable.

The surrounding README also states the container's purpose, authority, and ownership
boundary. A prose sentence or an isolated cardinality token does not replace the tree.

This rule applies recursively: the project root, each category folder, and each
multi-file entry's own root are all containers and each needs this cardinality
statement. An individual entry (a leaf) does not need to restate its category's
container contract, but a template's `README.md` must state the cardinality of the
elements *inside* the entry it demonstrates, since that is the schema every copy of
it will follow.

## Recursive folder contracts

Every managed container has a `metadata.yaml` that defines only its immediate relationship level. The required fields are `schema_version`, `name`, `kind`, `purpose`, `authority`, `owner`, and a non-empty `children` list. Each child declaration begins with `1`, `0..1`, or `0..*` and then names one immediate file, folder, alternative, or placeholder class.

```yaml
schema_version: 1
name: processes
kind: folder-collection
purpose: "Repeatable financial workflows"
authority: "Process definitions"
owner: financial-workspace
children:
  - "1 README.md"
  - "1 template/"
  - "0..* <process>/ entries"
```

A collection does not define the files inside an entry. Its `template/metadata.yaml` defines that entry relationship level. Each nested folder named by the template defines its own children in its own `metadata.yaml`. Real entry folders inherit the template contract; they do not copy and then independently drift from it. The complete hierarchy is composed recursively from these local contracts:

```text
financial-workspace/metadata.yaml
└── processes/metadata.yaml
    ├── template/metadata.yaml          # shape inherited by each <process>/ entry
    └── <process>/
        └── model-validation/metadata.yaml
```

A folder may opt out of recursive type checking only when it is a temporary data dump. Its `metadata.yaml` must declare all three markers: `type_check: exclude`, `kind: tmp-data-dump`, and `temporary: true`. Excluded dumps may contain arbitrary transient files and do not require a README or `children` contract. Project roots, declared categories, groups, and templates cannot be excluded. Permanent evidence, fixtures, examples, archives, and ordinary working folders must use normal recursive metadata rather than this exception.

```yaml
schema_version: 1
name: parser-scratch
authority: "None; disposable diagnostic output"
kind: tmp-data-dump
purpose: "Temporary parser diagnostics"
owner: financial-workspace
type_check: exclude
temporary: true
```

The repository validator renders each local contract into its folder's README between protected markers. Placeholder entry classes remain summarized as many; the generator does not enumerate their current instances.

``~~~~markdown
<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
processes/
├── 1 README.md
├── 1 template/
└── 0..* <process>/ entries
```
<!-- END GENERATED: contained-elements -->
~~~~``

`python tools/validate_specs.py` synchronizes generated sections and then validates the result. `python tools/validate_specs.py --check` performs the same validation without writing and fails when a generated section is stale. Authors edit `metadata.yaml`, not the protected Markdown region.
## Metadata frontmatter

Every entry (not bare containers) opens with a short YAML frontmatter block, using
only fields the document can keep accurate:

```yaml
---
title: Example title
status: draft
kind: subsystem
owners:
  - project-team
last_reviewed: YYYY-MM-DD
applies_to:
  - project
supersedes: null
related: []
---
```

`status` is one of `draft`, `active`, `complete`, `deprecated`, `superseded`, or the
sentinel `template` reserved for template copies so they can never be mistaken for an
active specification. A category may define a more specific lifecycle vocabulary for
its own entries (for example, bug records use `reported`, `confirmed`,
`fix-in-progress`, `resolved`, `not-reproducible`, `superseded`) as long as that
vocabulary is documented in the category's own container `README.md`. An enforced
category declares that vocabulary in `spec.json` through `statuses`; the validator
always permits `template` for the category's template entry and applies the declared
values to real entries:

```json
"bugs": {
  "type": "document-collection",
  "numbered": false,
  "statuses": [
    "reported",
    "confirmed",
    "fix-in-progress",
    "resolved",
    "not-reproducible",
    "superseded"
  ]
}
```

When `statuses` is omitted, the generic lifecycle vocabulary applies.

## Worked example

[`example/projects/example-project/`](example/projects/example-project/) is a
minimal project that instantiates all three structural types:

```text
example-project/
├── README.md
├── SPECS.md          # declares the category set and their structural types
├── spec.json          # project manifest (name, slug, source_repository, status)
├── architecture/      # fixed top-structured
│   └── README.md
├── subsystems/        # expandable folder collection
│   ├── README.md
│   ├── template/       # copyable template entry
│   └── widget-store/    # a named entry copied from template/ and filled in
└── decisions/          # expandable document collection
    ├── README.md
    ├── template.md
    └── 0001-use-sqlite-for-cache.md   # a named entry copied from template.md
```

Run the validator from the specs repository root:

```bash
python shared/conventions/typed_folder_system/validate_example.py
```

It checks, for the bundled example, that:

- the project manifest and root documents exist and are well-formed;
- the fixed category has its required structure without a template;
- the folder-collection category has a `template/` entry whose `README.md` declares
  the entry's internal cardinality, and every other entry follows the same required
  file set with non-template frontmatter;
- the document-collection category has a `template.md`, and every other entry
  follows the sequential-numbering naming convention with non-template frontmatter;
  and
- every entry's frontmatter carries the required fields and an allowed `status`.

Breaking any of these rules in `example/` (renaming `template/`, deleting a required
file, leaving `status: template` on a real entry, misnumbering a decision) should
make the corresponding check in `validate_example.py` fail — that correspondence is
what makes the example useful as a teaching fixture, not just documentation prose.
