---
title: Evidence rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Evidence rules

- Filenames, paths, titles, senders, and hashes are attributes, not source identity.
- A browser link is a locator and does not prove retrieval or completeness.
- Missing evidence, inferred values, and planned values are explicit states.
- Hash mismatch fails closed; transformations retain input identities and versions.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Admissible source artifacts

Any supported Drive file, Gmail message or attachment, Notion record, provider statement, or repository artifact may become an Evidence source. Links are locators; hashes are recorded only after bytes are acquired and verified. Every checked-in example records the source-system identity and limitations; raw source bytes remain external or in ignored temporary storage.
