---
title: Prompt and skill library
status: draft
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Prompt and skill library

Owns user-facing curation, selection and publication of prompt templates and
skills in a native or GitHub-backed library. It provides version selections to
run setup. The existing [skill registry](../skill-registry/README.md) remains
the owner of immutable skill bundle bytes, hashes and drafts; this library
references those revisions instead of duplicating them. Prompt revision
storage and native/GitHub synchronization are proposed, not implemented.

Consumer: [Langflow integration](../langflow-integration/README.md).
Dependencies: skill registry and external GitHub when that backend is selected.

Read the [contract](contract/README.md), [design](design/README.md) and
[validation](validation.md). Entry schema: those pages plus this overview
(1 each); focused contract/design pages (0..*).
