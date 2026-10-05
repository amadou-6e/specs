---
title: Work Graph source integrity experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Work Graph source integrity

[EXP-01 #50](https://github.com/amadou-6e/laomedo/issues/50) independently checks the installed read-only Work Graph connector against an adversarial, hand-checked GitHub response corpus. It is a verification gate for [EXP-16](https://github.com/amadou-6e/laomedo/issues/46) and [EXP-17](https://github.com/amadou-6e/laomedo/issues/47), not UI work or a live issue mutation.

Read the [prospective protocol](protocol.md), [sources](sources.md), and [attempt index](iterations/README.md). The protocol is frozen before executing the corpus; a result will be added as a dated attempt without rewriting the prospective criteria.
