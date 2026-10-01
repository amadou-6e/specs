---
name: define-project-spec
description: Guide a project owner through defining or reorganizing a project specification using the typed folder system, with focused questions, explicit ownership, populated entry templates and recorded decisions. Use for collaborative specification authoring and category design.
---

# Define a project specification together

Produce a specification the owner can understand, refine and use to direct
implementation. Read the repository guidance, project manifest, landing page,
existing SPECS.md and the
[typed folder convention](../../conventions/typed_folder_system/README.md).
Inspect existing category templates and related work before creating a new skill
or structure. The convention defines the mechanism; the project's SPECS.md chooses
its categories, entry shapes and ownership.

## Start from the user's work

Establish the product's intended users, the outcome they want, and one concrete
start-to-finish scenario. Use the conversation and current specs to prefill what
is already known. Distinguish user-confirmed intent, documented proposals,
implemented behavior and open questions. Do not treat a merged feasibility report
as acceptance of its recommended product or architecture.

Ask one focused decision at a time, or a small group of closely related questions.
Explain the consequence in product terms and offer a reasoned recommendation when
helpful. Avoid asking the user to choose a folder taxonomy before explaining the
underlying ownership choices. Continue independent inventory and drafting while an
answer is pending, but leave the dependent choice open. Record material answers in
the owning spec, not only in chat. A generic agreement does not settle unrelated
product decisions.

For each scenario, clarify inputs, output, state ownership, failure/recovery and
what observable evidence would demonstrate success. Use gaps in that scenario to
choose the next question. Keep a concise list of unresolved decisions and the
next question in the project specification while it is being drafted.

## Choose ownership and structure

Map stable behavioral responsibilities to candidate subsystems, then identify
cross-subsystem architecture and shared terminology. A package, provider, screen,
class or cross-cutting quality is not automatically a subsystem. Give each
behavior one canonical owner; link from other pages.

Read [template selection](references/template-selection.md) when choosing
categories or authoring their templates. Propose only categories the project
needs. For each category, record its structural type, authority, permitted child
shapes and cardinality. Fixed partitions must be declared explicitly rather than
copied from another project's technology stack.

Draft SPECS.md and the root reading map together. Align spec.json categories with
the agreed structure when the corresponding entries and templates actually exist.
For an existing project, first inventory old paths and classify their authority;
write a source-to-owner migration map. Preserve unresolved pages and references
until a reviewed migration establishes their replacement. Do not enable validation
in a way that disguises legacy documents as conforming entries.

## Develop one useful template and entry

Start with the category needed for the next scenario. Copy its canonical template
directly and rename it to the entry slug; replace its sentinel metadata and example
content. Adapt a Theseo template only after checking its cardinality and language
assumptions. Keep optional pages only when they own substantive content.

A new category template must be a populated illustrative example with
`status: template`, internal cardinalities, meaningful sample content and resolving
links. It must demonstrate how to write a real entry, not merely supply headings.
Its example choices do not become project requirements. Develop one actual draft
alongside it so gaps in the template become visible.

For a subsystem, separate observable contract, internal design and validation.
Write conditions and consequences rather than feature labels. State whether each
check is planned, present in code or actually executed. Exact interfaces,
configuration and migrations belong in optional pages when needed. For a new UI,
follow the repository's owning Draw.io path and review rules; prose cannot supply
missing visual states or transitions.

## Finish each conversation increment

Reconcile the owner's answer into the relevant documents, link supporting evidence
and mark remaining proposals as draft. Review ownership, links, cardinalities,
template metadata and spec.json agreement. Run the repository validator and, when
the skill changes, its skill validator. Report the concrete documents and next
unresolved decision. Follow the repository issue/branch/PR workflow; do not merge
or implement proposed product behavior merely because the drafting skill was used.
