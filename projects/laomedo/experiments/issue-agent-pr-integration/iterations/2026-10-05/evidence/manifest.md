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

| Artifact | Producer | Location and identity | Access |
| --- | --- | --- | --- |
| Sanitized five-condition observation | Credential-free probe at Laomedo `af87e6ccd91876f510789afece1cf7dc8cd8c033` | [observation.json](https://github.com/amadou-6e/laomedo/blob/d9e9a4c/experiments/exp19/observation.json), SHA-256 `814e3526d5405da8c015784ad08386c992b5ddf1aeae257b477ad3606780c9c9` | Repository |
| Fixture source and snapshot ID | Existing Work Graph importer | `examples/work-graph/github-pages.json`, SHA-256 `2fa947fa24e868c2d487c4e805155000a37d9d8aa1fac4db090db03126630d13`; graph `sha256:9f16758508a72ed163d87b938e5a6ad5c492db5a205878501e55593f700b5424` | Repository |
| Local branch and commit | Disposable Git checkout | `exp19/023574e1-3868-4246-9edf-2dd417b83326`, commit `a119e3da725aac78dd378bf22e9bd4a868006998` | Removed after execution |
| Run/trace and raw receipts | Temporary SQLite stores | Success run `023574e1-3868-4246-9edf-2dd417b83326`, trace `3df10b69-74a8-4fdc-b6ab-b6a98a3eb15e`; IDs and counts in observation | Temporary stores removed |

No credential, native agent stream or GitHub PR is part of this attempt.
