---
name: model-garden-legacy-specification
description: Create or revise non-authoritative Model Garden legacy records that preserve historical protocols, evidence, formats, or artifact provenance while directing readers to current owners.
---

# Maintain Model Garden legacy records

Use [template.md](template.md) for a normal archive entry and [README.md](README.md)
for category ownership. Legacy records preserve evidence; they do not define current
behavior, revive a superseded protocol, or replace an active experiment migration.

## Establish provenance

- Inspect the original document, linked reports and artifacts, relevant experiment,
  and current subsystem or architecture owner before editing an archive record.
- Preserve historically identity-bearing paths, hashes, revisions, commands, and
  quoted outcomes. Do not rewrite them to resemble the current repository layout.
- Distinguish original claims from later interpretation. If provenance is incomplete,
  say so rather than reconstructing missing facts.

## Write an archive record

- Start with the standard metadata block and an explicit notice that the entry is
  historical and non-authoritative.
- Identify what was archived, its former scope, why its authority ended, and the date,
  release, experiment gate, or decision that ended it when known.
- Link the active replacement: normally a structured experiment, subsystem contract,
  implementation rule, or architecture page. Keep actionable migration instructions
  with that current owner.
- Explain the record's continuing evidential value, such as interpreting old
  checkpoints, frozen protocols, reports, or artifact identities.
- Do not mechanically split an identity-bearing historical document. A structured
  experiment may cite it in place until substantive migration preserves its meaning.

## Review and validate

- Verify that no archive page presents itself as current guidance and that every
  claimed replacement resolves to a canonical owner.
- Check historical paths and identifiers against the original evidence; do not
  normalize them merely for consistency.
- Run the specs validator and report changed records, evidence inspected, unresolved
  provenance, and validation actually performed.
