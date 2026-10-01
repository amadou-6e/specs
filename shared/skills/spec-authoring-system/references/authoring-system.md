# Structural and authoring contract

## Category selection

Select from these purposes, adapting names only when the project has a reason:

| Purpose | Usual category | Shape |
| --- | --- | --- |
| Cross-subsystem relationships and shared invariants | architecture | fixed |
| Owned behavior, lifecycle, APIs, configuration | subsystems | folder collection |
| Bounded tests and their separate attempts | experiments | folder collection |
| Exploratory sources, findings, and synthesis | research | folder collection |
| Durable choices, alternatives, and consequences | decisions | document collection |
| Contributor conventions and local procedures | implementation | fixed |
| Reviewed surfaces, Draw.io, references, and captures | ui-design | folder collection |
| Durable defect knowledge | bugs | document collection |
| Non-authoritative history and replacements | legacy | document collection, with explicitly documented artifact support where necessary |

`SPECS.md` defines the chosen categories, category types, allowed growth,
authority, metadata/lifecycle, and review workflow. The root README explains
the project and gives reading paths. `spec.json` declares machine-checkable
structure. Inspect the validator rather than inventing unsupported manifest
fields or claiming checks it does not implement.

## READMEs and cardinalities

A container README defines what may exist beneath that boundary. Use `1`,
`0..1`, and `0..*` in a tree/table, name canonical owners, and explain when to
create optional elements. The template README additionally defines the
internal entry schema. A concrete entry README explains its purpose, consumers,
maturity, dependencies, and links; it need not repeat the full category schema.

Use one directly copyable `template/` for folder collections and one
`template.md` for document collections. Fixed categories do not use copy-and-
rename folder templates. Give every organizing container a README, including
fixed partitions. Support directories are defined by their owning container
unless they have an independent collection schema.

## Content depth

Subsystems normally require overview, `contract/README.md`, `design/README.md`,
and `validation.md`. Add interfaces, configuration, extensions, guides, and
migrations when they have content. Contracts own observable behavior; design
explains mechanisms. Validation maps guarantees to observed checks and gaps.
Provider adapters can share a subsystem when they share its boundary.

Experiments separate overview, protocol, and sources from iteration execution,
evidence manifest, and results. Replication has its own record when performed.
Protocols state questions, controls, metrics, decision gates, resources, and
allowed adaptations. Actual failures, budgets, deviations, and missing evidence
remain visible. Evidence manifests identify artifacts by producer, stable
revision/hash, location, and access/retention limitations. Do not copy private
raw artifacts into the specs repository.

Research separates method, characterized source records, atomic findings, and
synthesis. Findings distinguish direct observation, reported claims, inference,
and recommendations. Decisions preserve status, rationale, alternatives,
consequences, and verification. Recommendations are not accepted decisions.

Implementation contains contributor conventions and reproducible procedures,
linking the contracts it realizes. UI geometry/states/transitions retain the
repository's Draw.io authority. Templates may show a populated prose example
but must not invent a reviewed UI or fabricate verification.

## Example quality and metadata

Create coherent project-relevant examples: a real kind of interface, a bounded
test question, or a plausible choice explicitly labeled illustrative. Populate
substantive content rather than repeating instructions to 'describe' each
section. Avoid contrived code, fabricated measurements, or unnecessary optional
files. Template values clearly remain examples; copying requires replacing
identity, links, example facts, and lifecycle before registration as a real entry.

Use required repository metadata accurately. Keep document lifecycle distinct
from decision disposition, implementation maturity, experiment termination,
and GitHub work status. Register category-specific lifecycle values in the
manifest when supported. An authoring review date does not mean the underlying
experiment was executed on that date.

## Validation coverage

Check what the existing validator actually traverses. Declaring category entry
files may validate their metadata without validating nested attempts, evidence
manifests, copied-template lifecycle, anchors, or every container's cardinality.
Audit those relationships separately and disclose remaining manual checks.
Do not describe a structurally valid manifest as comprehensive enforcement of
the authoring system.
