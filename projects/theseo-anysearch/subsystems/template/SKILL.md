---
name: theseo-subsystem-specification
description: Populate or revise a Theseo subsystem specification from current implementation, tests, and existing specs; use when an entry is only a migration index or its contract and validation are underspecified.
---

# Populate a Theseo subsystem specification

Use the [subsystem template](README.md) for file ownership and cardinality, and the
project [SPECS.md](../../SPECS.md) for category boundaries. This skill turns an
index of links into a self-contained, evidence-backed specification. It does not
authorize implementation changes or invent product requirements.

## Establish the evidence base

- Read the target entry, project manifest, relevant old specs, current code, tests,
  configuration examples, and any governing decisions. Check the implementation
  repository's branch and commit; record which revision the findings describe.
- Trace each important behavior through its real entry point and consumer. A name,
  comment, proposed spec, or isolated test is not by itself evidence that behavior
  is live. Distinguish implemented behavior, intended contract, historical behavior,
  and open questions.
- Treat old documentation as evidence to reconcile, not text to copy. When sources
  disagree, identify the conflict and its evidence. Do not silently choose the
  newest-sounding claim or promote an inference into a guarantee.

## Write the owned specification

- Make the target entry readable on its own. Links support concrete statements;
  they do not replace the statements. Cite source files, tests, decisions, or specs
  near consequential claims, using clickable paths from the specification file to
  the actual source, or full repository-root-relative paths with an identified
  repository and revision. Never cite only `api.py`, `service.py`, or another bare
  basename when several locations could match.
- Start **every** page with a short paragraph explaining what that page covers and
  how it relates to the subsystem. Give the reader the context before a checklist,
  numbered procedure, table, or module list.
- In the root `README.md`, define ownership, consumers, supported scope, maturity,
  limitations, and a reading map. Keep other subsystems' contracts with their owners.
- In `contract/README.md`, state observable behavior as testable guarantees and
  invariants. Cover relevant lifecycle, inputs/outputs, determinism, rejection and
  error behavior, resource limits, and unsupported cases. Give conditions and
  consequences, not just feature names.
- Put exact public surfaces in optional `contract/interfaces.md`, settings/defaults
  and identity effects in `contract/configuration.md`, and extension conformance in
  `contract/extensions.md`. Organize extensions by discovery and trust boundary,
  required interface, generated output, validation/failure semantics, and known
  limitations where applicable. Create an optional page only when there is
  substantive content for it.
- In `design/README.md`, explain the components, data flow, state ownership,
  persistence/cache, trust and failure boundaries, and meaningful trade-offs that
  realize the contract. Use `design/python.md` or `design/rust.md` only where a
  language responsibility map adds useful detail; organize mappings by role or
  execution sequence and spell out each module's full path on first mention.
- In `validation.md`, map every decision-relevant guarantee to a concrete check:
  test name/path, fixture, command or CI job, and what it proves. Separate checks
  actually run from checks merely present, and name missing coverage explicitly.
- Add guides or migrations only for real workflows or active compatibility changes.
  Begin a guide with its purpose, prerequisites, and expected result before steps.
  Show commands precisely enough to run, distinguishing syntax verified from the
  implementation from illustrative placeholders. Remove empty placeholder pages
  rather than filling the tree mechanically.

## Reconcile and finish

- Keep an explicit list of unresolved conflicts and validation gaps. Use `draft`
  status while material contract questions remain; do not imply an index is mature.
- Check that contract, interfaces, configuration, design, and validation do not
  contradict one another, and that links resolve. Do not duplicate a source's whole
  content or silently supersede it; record migrations/supersession when appropriate.
- Perform a reader pass separate from the evidence pass: can someone unfamiliar with
  the code understand what the subsystem does, follow the guide, locate each cited
  module unambiguously, and find the extension obligations without decoding a wall
  of prose or bullets? Revise any page that fails this test.
- Run the specs repository validator. Report the implementation revision inspected,
  pages changed, evidence checked, commands actually run, and remaining uncertainty.
