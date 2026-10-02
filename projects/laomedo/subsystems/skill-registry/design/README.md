---
title: Skill registry and drafts design
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill registry and drafts design

Content-addressed bundles supply pinned bytes. Drafts carry independent policy hashes, patches and validation. Candidate materialization is separate from raw workspace inventory; promotion must compare the current canonical base separately.

Reconstructed from local specs and evidence reports; implementation was not re-executed
or independently verified by this migration. [Validation](../validation.md) pins the
observation boundary. Public behavior belongs to [contract](../contract/README.md).
Design container: README.md (1), focused mechanism pages (0..*). No language partitions
are needed for currently inspected material.

[Decision readiness](decision-readiness.md) classifies first-slice rules,
unsettled policy choices, GitHub research, and pending crash experiments. It
does not replace the target contracts or validate crash behavior.
