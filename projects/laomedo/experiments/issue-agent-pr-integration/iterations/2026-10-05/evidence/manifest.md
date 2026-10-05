---
title: EXP-19 phase-zero evidence manifest
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Planned artifact | Producer | Location and identity | Access |
| --- | --- | --- | --- |
| Sanitized five-condition observation | Credential-free probe | Pending execution and content hash | Repository after verification |
| Fixture source and snapshot ID | Existing Work Graph importer | `examples/work-graph/github-pages.json`; actual hash pending | Repository |
| Local branch and commit | Disposable Git checkout | Temporary only; hash in sanitized observation | Removed after execution |
| Run/trace and raw receipts | Temporary SQLite stores | IDs and counts in sanitized observation | Temporary stores removed |

No credential, native agent stream or GitHub PR is part of this attempt.
