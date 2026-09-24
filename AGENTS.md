# Agent guidance

This repository contains specifications, not product implementation. Prefer changes
that make intent, behavior, constraints, and verification clearer.

## Working rules

- Read the project manifest and nearby specifications before editing.
- Preserve project-specific organization unless a migration is explicitly requested.
- Do not overwrite user-authored Draw.io changes. Inspect the current Git diff before
  editing and use branches and commits for design history; do not create backup copies.
- Keep reference screenshots beside their Draw.io workshop when they are used for
  fidelity comparison.
- Keep view-specific components under `projects/<slug>/views/<view>/ui/components/`.
  Use `projects/<slug>/ui/shared/` only for components with no single view owner.
- Keep live screenshots in `references/` and superseded multi-view studies in
  `ui/archive/`. Do not track Draw.io exports; generate them temporarily for visual
  inspection and discard them after review.
- Use editable geometry for UI proposals; screenshots are references, not substitutes.
- Treat each view's Draw.io as the sole authority for UI geometry, component states,
  interaction IDs, and transitions. Markdown, screenshots, and test plans are derived
  indexes or evidence and must not introduce behavior absent from the Draw.io.
- When an implementation issue needs a new UI control, state, or transition, update and
  review the owning Draw.io before implementation or in a stacked specification PR.
- Visually inspect Draw.io changes at component level and at full-page scale.
- Record unresolved decisions explicitly instead of inventing product behavior.
- Never add credentials, browser profiles, cookies, tokens, or captured login URLs.
- Do not vendor generated caches, virtual environments, model weights, dependency
  trees, or cloned upstream repositories.
- Run `python tools/validate_specs.py` before committing.
- Treat this repository as the system of record for specifications. Completed changes
  to specifications and their evidence must be committed on the issue branch and
  pushed to this repository; do not leave specification work only in an ignored
  checkout or in an implementation repository.

## Change workflow

Problem or feedback -> specification issue -> typed issue branch -> spec and evidence
-> validation -> pull request -> review -> merge.

Use `<type>/<issue-number>` branches, for example `feat/12`, `fix/18`, `docs/21`, or
`chore/24`. Pull requests should link the issue and identify the specifications whose
status or behavior changed.

## Stable nomenclature in conversation and specifications

Use the same established name for the same concept across messages, diagrams,
metadata and schemas. Do not switch between synonyms for stylistic variety.
Check the relevant catalogue before describing an object as existing.

Distinguish an existing object, a field on an object, a proposed object and an
implemented change. A discussion or diagram does not create an object in the
repository. Preserve that distinction in every follow-up. If a rename or promotion
is useful, state the old name, proposed name and reason explicitly; update affected
references consistently when the change is authorized.

Use the user's agreed notation consistently. In relationship trees, preserve
[parent cardinality : child cardinality] and do not substitute vague relationship
verbs or imply ownership through a navigation path.

### Examples from the financial-model discussion

**Example 1: A field is not an existing object**

User: "I don't see an Agreement term object."

Avoid: "Agreement term is another object in the model."

Use: "Agreement term is not an object in the catalogue. Recurring-payment agreement
currently contains a terms field. Promoting it to an Agreement term object is a
proposal, not an implemented change."

**Example 2: Keep distinct item types distinct**

User: "A procurement has procurement items; a receipt has receipt items."

Avoid: Calling both concepts "items" interchangeably or implying that Procurement
item already covers Receipt item.

Use: "Procurement item exists. Receipt item is a separate proposed object and has
not yet been added. A Procurement item describes the purchase; a Receipt item
describes a line on its document."

**Example 3: Keep the established object name**

Avoid: Switching among "Transaction statement", "Statement" and "transaction
sheet" as if they were different or newly named objects.

Use: "Transaction statement" consistently for the established object. If the user
uses a synonym, acknowledge its correspondence once and retain the agreed name.

**Example 4: Preserve cardinality notation**

User: "Despite using cardinalities, can you represent it as a tree?"

Avoid: Replacing the agreed links with "has", "records" or "provides" in the next
message.

Use: "Recurring-payment agreement -> [1 : 0..*] Recurring-payment occurrence".
Mark any additional Agreement term branch as proposed until it is implemented.
