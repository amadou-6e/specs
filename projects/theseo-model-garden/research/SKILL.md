---
name: model-garden-research-specification
description: Create or revise a Model Garden research topic through reproducible discovery, individually characterized sources, bounded evidence-linked findings, transparent synthesis, and non-normative recommendations.
---

# Maintain a Model Garden research specification

Use the [research template](template/README.md) for file ownership and relationships,
and the project [SPECS.md](../SPECS.md) for category boundaries. Research is
exploratory and informative. It may motivate an experiment or decision, but it does
not establish product behavior, approve a dependency, or change a subsystem contract.

## Bound the investigation

- Define the questions the topic can answer, why they matter to Theseo, the comparison
  dimensions, and explicit non-questions before collecting conclusions.
- Check existing research, experiments, decisions, subsystem specifications, and peer
  Model Garden projects first. Extend the canonical topic when the question is already owned;
  do not create a competing synthesis merely because the new investigation started
  from another conversation.
- Put provider acquisition, source datasets, and routing assets in the peer Theseo
  World Providers project. Keep Model Garden research focused on representation data,
  encoder architectures, pretraining, qualification, transfer, registry compatibility,
  and artifact consumption questions.
- Record the search and inspection method in `method.md`: dates, repositories or
  databases, queries and browsing paths, inclusion and exclusion criteria, access and
  language constraints, evidence classes, confidence criteria, and known bias. Give
  its limitations section explicit treatment of incomplete access, uninspected
  artifacts, temporal limits, selection bias, and questions the method cannot resolve.
- Give the topic root the standard metadata block and generic lifecycle status.

## Characterize sources individually

- Create one `sources/<source>.md` record for every material item used. Prefer stable,
  primary sources for technical claims: official documentation, source code at a
  pinned revision, standards, papers, benchmark artifacts, or authoritative datasets.
  Use secondary sources when they add analysis or discovery value and label them.
- Record the canonical link or repository location, owner, publication date, version
  or revision, access date, source type, evidence class, rights status when relevant,
  and a content hash for retained local artifacts when practical.
- State exactly what was inspected. Distinguish reading an abstract or documentation
  page from inspecting code, downloading data, running commands, reproducing a result,
  or measuring behavior directly.
- List only claims actually used by this topic and explain the source's authority and
  limitations for those claims. A project describing its own design is authoritative
  for that design, not automatically for comparative performance or suitability to
  Theseo.
- Preserve inaccessible, partial, or changing-source limitations. Do not cite a search
  result, generated summary, or repository name as though the underlying material was
  inspected.
- Add or update the source's row in `sources/README.md` in the same change, including
  ID, material, type, evidence class, and access date. Maintain its **Related findings**
  backlinks whenever a finding starts or stops using that source.

## Register bounded findings

- Give each finding a stable identifier and make it one reviewable claim. Split claims
  that rely on different evidence, confidence, or applicability.
- Classify the finding accurately, for example as an externally reported claim,
  directly verified fact, cross-source synthesis, project-specific inference, or
  recommendation. Record its support status and confidence separately from rhetorical
  certainty.
- Link every finding to one or more characterized source records. Explain what the
  evidence establishes, how it supports or contradicts the claim, and what it does not
  establish. One source may relate to many findings and one finding may require many
  sources.
- Keep project applicability explicit. A technique working in another engine,
  benchmark, scale, hardware environment, or data distribution does not establish that
  it works in Theseo. Identify the assumptions needed for transfer.
- Include limitations, counterevidence, unresolved disagreement, and plausible
  alternative explanations. Do not average incompatible sources into a false consensus.
- State consequences proportionally: a finding may justify further research, a
  feasibility prototype, an experiment, or a decision proposal. It does not itself
  authorize implementation.
- Add or update the finding's row in `findings/README.md` in the same change,
  including ID, finding, classification, status, and confidence.

## Synthesize without losing provenance

- In the topic `README.md`, summarize the registered findings while preserving their
  identifiers, classification, confidence, and disagreements. Do not introduce a
  substantive claim that has no finding record.
- Use comparison matrices only when candidates share meaningful dimensions. Every
  substantive cell must trace to a finding or source record; distinguish `not found`,
  `not inspected`, `not supported`, and `not applicable`.
- Separate eligibility criteria from observed conclusions, and current facts from
  forecasts. Verify temporally unstable facts at the time of the update and record the
  access date.
- Explain which findings transfer to Theseo, which do not, and why. Make recommendations
  conditional on evidence strength and name the experiment or decision needed next.
- Keep open questions visible. Lack of evidence is not evidence of absence, and a
  promising adjacent implementation is not proof of feasibility in this codebase.

## Reconcile existing material

- Treat prior specs and notes as sources to inspect, not prose to copy. Recover their
  citations and claims, then move each supported claim into an appropriate finding.
- When old and new sources conflict, preserve both characterizations and register the
  disagreement explicitly. Do not silently prefer the newer, more detailed, or more
  convenient source.
- Mark inferred or reconstructed provenance. Do not fabricate search queries, access
  dates, inspected sections, hashes, or reproduction work for historical research.
- Migrate old single-document research only when it is substantively reviewed; avoid
  mechanical restructuring that gives unsupported notes the appearance of rigor.

## Review and validate

- Check that every synthesized claim resolves to a finding, every finding resolves to
  inspected sources, reciprocal source/finding links agree, and classifications and
  confidence match the actual inspection depth.
- Check that the findings and sources registry tables contain every record exactly
  once and agree with the current record metadata and reciprocal links.
- Check links, revisions, dates, hashes, rights notes, terminology, and project
  ownership. Confirm recommendations remain non-normative and do not contradict an
  accepted decision without identifying that conflict.
- Perform a skeptical-reader pass: another contributor should be able to reproduce the
  search boundary, understand what was actually inspected, distinguish fact from
  inference, and locate counterevidence without relying on chat history.
- Run the specs repository validator. Report sources added or rechecked, searches and
  commands actually performed, unavailable material, and remaining uncertainty.
