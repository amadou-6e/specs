---
name: theseo-architecture-specification
description: Populate or revise Theseo's project-wide architecture map and focused cross-subsystem architecture documents from current implementation, subsystem contracts, decisions, tests, and existing specs.
---

# Maintain the Theseo architecture specification

Use the project [SPECS.md](../SPECS.md) for category ownership and
[template.md](template.md) for focused-document structure. Architecture describes
the current system across subsystem boundaries. It does not own subsystem behavior,
repeat interface details, or replace decision records with retrospective rationale.

## Establish the architecture evidence

- Read the project overview, glossary, affected subsystem contracts and designs,
  accepted decisions, implementation guidance, and relevant tests before changing
  the architecture map. Inspect the current implementation when documentation does
  not establish a relationship or execution path conclusively.
- Trace important paths end to end through their actual entry points and consumers.
  Confirm process, language, persistence, cache, extension, and trust boundaries
  rather than inferring them from package names or intended designs.
- Record the implementation repository and revision the inspection describes.
  Separate current behavior, accepted but unimplemented design, historical behavior,
  and unresolved questions. Do not promote a proposal or experiment result into the
  current architecture without an accepted decision or implemented evidence.

## Maintain the system map

- Keep `architecture/README.md` as the project-wide navigation and relationship map.
  It has two simultaneous responsibilities: retain the category's contained-elements
  and authority contract, and orient a reader to major components, subsystem
  dependencies, principal data and control flows, cross-language/process boundaries,
  and focused architecture documents. If it contains only the container description,
  treat the system map as incomplete rather than interpreting that stub as the target.
- Give the system map an explicit system-context section identifying external actors,
  external systems, and the project boundary before internal component detail. Use a
  boundary diagram when it materially clarifies those relationships.
- Add or revise a focused document only when a relationship spans multiple
  subsystems or establishes a system-wide invariant. Use descriptive filenames beside
  `README.md`; architecture is not a collection of entry folders.
- Give focused documents the standard metadata block and generic lifecycle status.
  Existing `cli.md` and `configuration.md` predate the focused architecture template
  and are migration inputs, not alternative templates. Preserve their useful current
  versus proposed distinctions, but route single-subsystem interface and configuration
  reference material to the owning subsystem contract when revising them.
- For each component, identify its responsibility and state ownership. For each edge,
  state what crosses it, in which direction, through which interface, and under whose
  contract. Link the owning subsystem specification rather than restating its full
  API or configuration schema.
- Describe relevant construction, reset, runtime, persistence, recovery, and failure
  flows in execution order. Make blocking, asynchronous work, caching, identity,
  versioning, compatibility, determinism, and resource boundaries explicit where
  they affect more than one subsystem.
- Describe failure boundaries explicitly: where failures originate, how they cross or
  are contained by component boundaries, and which contract owns their presentation.
- Use diagrams when they clarify relationships that prose cannot show compactly.
  Keep editable diagram sources in `architecture/`, name every boundary and flow,
  and ensure the surrounding text remains sufficient to interpret the diagram.

## Preserve ownership boundaries

- Put observable guarantees and interfaces in the owning subsystem's `contract/`.
  Put internal single-subsystem structure in that subsystem's `design/`.
- Put the rationale, alternatives, and consequences of a durable choice in
  `decisions/`. Architecture may summarize the resulting constraint and link to the
  decision, but must not become a second decision record.
- Treat experiments and research as evidence, not architectural authority. Link them
  only when they explain validation, uncertainty, or an open question.
- Put contributor rules and runbooks in `implementation/`, visual interaction details
  in `ui-design/`, and historical material in `legacy/`.
- Do not manufacture a subsystem boundary merely to make a diagram tidy. When sources
  disagree about ownership or behavior, document the conflict and leave the page in
  `draft` until the authoritative contract or decision resolves it.

## Review and validate

- Check that every named subsystem and interface resolves to a canonical owner, every
  system-wide invariant is consistent with the linked contracts, and focused pages do
  not contradict the root architecture map.
- Verify links, metadata, terminology, and diagrams. Use glossary terms consistently
  and identify compatibility or migration effects rather than silently describing
  only the newest path.
- Perform a reader pass: a contributor unfamiliar with the repository should be able
  to locate responsibility, follow the principal flows, identify failure boundaries,
  and know where authoritative detail lives.
- Run the specs repository validator. Report the implementation revision inspected,
  documents changed, evidence checked, validation actually run, and remaining open
  questions.
