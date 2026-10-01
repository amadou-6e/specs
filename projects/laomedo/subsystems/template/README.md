---
title: Run catalogue example
status: template
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Run catalogue example

This populated template illustrates a subsystem that stores and retrieves run
references for workflow and graph clients. Its choices are example content to
replace when creating a real entry, not accepted Laomedo requirements.

## Contained elements

```text
<subsystem>/
├── 1 README.md
├── 1 contract/
│   └── 1 README.md
├── 1 design/
│   └── 1 README.md
└── 1 validation.md
```

Each subsystem owns one overview, one observable contract, one internal design
and one validation record. Optional interfaces, configuration, extensions, guides
or migrations must have substantive content and a declared owner when added.

## Ownership and consumers

The catalogue owns the mapping from an opaque run ID to the recorded state and
artifact references. The runner owns executing the task; artifact storage owns
the bytes; the catalogue references both. Workflow clients and work-item views
can query the same run without storing competing histories.

## Example outcome and limits

A client can register run `run-001`, retrieve its last recorded state and follow
its output reference. A missing ID returns an explicit missing-record result.
The catalogue's stored state is evidence received from the runner; querying it
does not independently verify provider execution or artifact completeness.

## Reading map

- [Observable contract](contract/README.md)
- [Internal design](design/README.md)
- [Validation plan and evidence](validation.md)
