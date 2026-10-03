---
title: Pinned skill materialization protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The [EXP-08 issue](https://github.com/amadou-6e/laomedo/issues/38)
predefined the LF/CRLF, edit, cleanup, path and discovery questions. This
detailed fixture was written **after** execution, not frozen beforehand.

In a disposable Git repository, create a clean source directory. For separate
LF and CRLF `SKILL.md` byte fixtures, import an immutable whole-skill
revision, ask the existing runner materializer to write it into a separate
effective workspace, and compare source/effective file bytes and tree hashes.
Record source, effective and post-edit workspace hashes. Edit only the
effective skill copy, then verify canonical source/revision hashes and source
Git status remain unchanged. Reject parent-path reads, unsafe IDs and a
tampered stored revision before it reaches the effective workspace. Remove
the effective copy and inspect Git status again.

Pass the **synthetic** check only if all byte comparisons, rejection checks,
and clean-status checks hold. Do not infer native discovery from the path:
the runner's `offered` field is not a read/use event. Any model-backed
discovery needs a separately authorized turn cap.
