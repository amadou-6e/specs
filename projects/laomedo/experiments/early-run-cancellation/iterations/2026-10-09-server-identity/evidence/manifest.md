---
title: Pinned Langflow server identity evidence
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Artifact | Pin and access |
| --- | --- |
| Protocol and in-process identity test | [Laomedo `e52194a`](https://github.com/amadou-6e/laomedo/commit/e52194a); pinned Langflow image `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` |
| Server probe, inspector and result | [Laomedo `4f12370`](https://github.com/amadou-6e/laomedo/commit/4f12370) |
| Sanitized identity summary | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-g-identity-20261009-d/identity-summary.json`; SHA-256 `7a395f6bf4317d282c833ea18d3ade16379600cc251a41e6a46524ea1bf5b38b` |
| Read-only SQLite inspection | Private `identity-locations.json`; SHA-256 `fdff56155e90aa63870fe940513b2cadb8a86e4f5f42d254eff8107f4db2821a` |
| SQLite snapshot | Private `langflow-snapshot.db`; SHA-256 `1d809a0632814d7e16e5891b4adc6d5adac07d58c2056650aa19149800685e9d` |
| Teardown | Private `teardown.json`; SHA-256 `e9dfbaed41efca2752c3df2f551899796c1b08377ea34f3c61e782990d6b8f61`; disposable container absent and fake runner stopped |
| Authorization ledger | Private `%LOCALAPPDATA%/Laomedo/exp22-phase-c-turns.json`; unchanged at 6/12, with zero model calls for this iteration |

The private snapshot may contain the disposable Langflow API key or its hash;
it and the fake runner token are not committed. The sanitized summary and
teardown were checked for the fake runner token; neither contained it. The
table/column inspector reports only match counts, not row values.
