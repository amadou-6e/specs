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
| Sanitized five-condition observation | Credential-free probe at Laomedo `096075f31cfc88ea6dc226ab0b1deeb0af33756b` | [observation.json](https://github.com/amadou-6e/laomedo/blob/feat/49/experiments/exp19/observation.json), SHA-256 `3e8d6165da7cab38a192a26e3496e1ea003b5ec96d3ccd78e28a74c71ac0c5b1` | Repository |
| Fixture source and snapshot ID | Existing Work Graph importer | `examples/work-graph/github-pages.json`, SHA-256 `2fa947fa24e868c2d487c4e805155000a37d9d8aa1fac4db090db03126630d13`; graph `sha256:9f16758508a72ed163d87b938e5a6ad5c492db5a205878501e55593f700b5424` | Repository |
| Local branch and commit | Disposable Git checkout | `exp19/78d2b738-679c-43c6-8fd0-aab739dfaaf2`, commit `61a47d71ff7c0bb50dfa2d3fc5eccc4eac78f8aa` | Removed after execution |
| Run/trace and raw receipts | Temporary SQLite stores | Success run `78d2b738-679c-43c6-8fd0-aab739dfaaf2`, trace `7caa2763-63b1-415d-954c-ee36316e859b`; IDs and counts in observation | Temporary stores removed |

No credential, native agent stream or GitHub PR is part of this attempt.
