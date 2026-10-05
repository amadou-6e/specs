---
title: EXP-19 phase-zero execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The prospective protocol was committed as specs `c073ba01069accc2713b2ab96fa45a7b2088d67d`. The tested Laomedo code was committed as `096075f31cfc88ea6dc226ab0b1deeb0af33756b` before recording. The fixture was `examples/work-graph/github-pages.json`, SHA-256 `2fa947fa24e868c2d487c4e805155000a37d9d8aa1fac4db090db03126630d13`. The probe froze the imported graph snapshot `sha256:9f16758508a72ed163d87b938e5a6ad5c492db5a205878501e55593f700b5424`, two-node flow digest `sha256:9670d89e0223c4e33ceea9d4460a105486f70d1d353dba5a741c5e8156b7a541`, fake provider/model/effort, synthetic skill digest `sha256:12381c479ed0f553a138d618e2b4d377cb19e0401ed1adb151fd2f29ee452b3d`, local checkout-only grant and zero-turn budget.

From the Laomedo root, `python -m experiments.exp19.probe --record` executed the five conditions in disposable local directories and wrote a sanitized [observation](https://github.com/amadou-6e/laomedo/blob/feat/49/experiments/exp19/observation.json). `python -m unittest discover -s tests` passed 123 tests, including three focused EXP-19 tests. The probe removed the temporary SQLite stores, snapshots and local Git checkout when it exited. The observation contains identifiers and counts, not source issue content or credentials. The recorded observation's SHA-256 is `3e8d6165da7cab38a192a26e3496e1ea003b5ec96d3ccd78e28a74c71ac0c5b1`.

This execution did not start Langflow or a real agent, call a model, contact GitHub, or create a remote PR. The local Git repository had no remote; the success candidate was only a temporary branch and commit.
