---
name: financial-model-specification
description: Create or reorganize Financial Workspace data models using concrete structure, schema, rules, examples, and optional presentation while preserving existing specifications.
---

# Maintain a financial model

Use [the model template](README.md). This skill covers local specifications; it does not authorize remote mutations.

## Establish scope

Read the entry, existing specifications, relevant process and integration documents, and available schema captures. Describe the Financial Workspace use of the system. Include provider mechanics only when they affect our data. Do not create generic platform manuals or redundant deployment nesting.

Choose the catalogue before editing:

- `objects/` owns system-independent financial concepts and semantics;
- `systems/` owns concrete repository, Drive, Gmail, Notion, or other representations;
- `mappings/` owns crosswalks, authority, and transformations spanning entries.

Do not place these three meanings as peer entries in one flat catalogue. A system may reference the object model but cannot redefine it; a mapping may connect both but cannot absorb either endpoint.

## Preserve existing content

Before restructuring, inventory concrete hierarchies, schemas, identifiers, options, formulas, filing decisions, examples, presentation configuration, sources, and unresolved gaps. Assign each a destination. Do not replace a concrete structure with abstract identity or synchronization rules. Preserve dated remote observations separately from proposed targets. Missing evidence stays explicitly unknown.

For each moved document, preserve substantive content and repair inbound and outbound links. At completion compare the source inventory with the resulting documents. Link validation is necessary but cannot prove content preservation.

## Classify documents

- README.md: purpose, ownership, consumers, maturity, limitations, reading map.
- structure.md: components, containment, relationships, cardinalities, concrete topology.
- schema.md: records, attributes, exact types, keys, options, formulas and computed fields.
- rules.md: required meaning, consistency, filing and lifecycle constraints.
- examples/: real or explicitly illustrative examples, only where useful.
- presentation/: configured displays such as Notion boards, tables, charts and filters. These are distinct from the stored schema.

Begin with files. Expand a subject into a named folder with README.md when several useful documents exist. Do not require identical file counts or create placeholder collections. Avoid contract/, views/, native-model/, or deployments/ as generic wrappers.

## Preserve semantics

Keep provider IDs distinct from names, paths and display labels. Preserve many-to-many relationships and monetary allocations. Distinguish order, travel, service, payment, posting and observation dates; retain currency with amount and unknown values separately from zero. Expected events do not become observed transactions through presentation. Record native property types only when supported by schema evidence.

Financial meaning belongs to `objects/financial-domain`; cross-system mappings to `mappings/cross-system`; each concrete representation belongs under `systems/`. Operational procedures belong in processes, connector mechanics in integrations, bounded changes in migrations, and durable rationale in decisions.

## Evidence and checking

Place sources, stable references and observation dates beside claims or in a Basis section. Preserve existing source inventories during moves. Keep validation procedures and historical check records under the relevant integration or process; link them from rules. Do not turn absent current inspection into a false current-state claim.

## Finish

Check content preservation against the initial inventory, exact IDs and options, current/target separation, category ownership, and links. Run the specs validator. Report what changed and any remaining gaps. Do not expand a documentation task into remote verification or mutation unless needed and authorized.
