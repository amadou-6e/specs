---
title: Prompt and skill library design
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Prompt and skill library design

Candidate shape: a catalog entry points to a prompt revision or an immutable
skill registry revision; the UI and chat API use the same selection and edit
operations. This permits recommended items and a user-curated library without
copying skill bundle bytes into every saved workflow.

The native/GitHub backend boundary, prompt version store and publication
conflict policy are not chosen. Observable behavior belongs to
[interfaces](../contract/interfaces.md). Design container: README.md (1),
focused mechanism pages (0..*).
