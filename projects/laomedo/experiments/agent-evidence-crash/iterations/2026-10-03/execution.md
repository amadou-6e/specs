---
title: Agent evidence crash execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

On Windows with Python 3.12.10, at Laomedo
[`9bcb64a`](https://github.com/amadou-6e/laomedo/commit/9bcb64abc62c014735dd5d054560eee0c4a2fa96),
run `python experiments/exp05/probe.py`. The parent starts seven child
processes in independent temporary SQLite databases. Each uses WAL and
`synchronous=FULL`, exits at its selected boundary, and is inspected after
a restart sweep. Raw projection is derived only from committed receipts.
The test fixture uses a synthetic provider string and synthetic event payload.
No Langflow server, Codex/Claude session, model call, network write, private
credential, or personal workspace is used.

`python -m unittest tests.test_exp05_evidence` passed 4 tests, including
identity validation and repeat sweep. The complete
`python -m unittest discover -s tests -p 'test_*.py'` passed 124 tests
at this revision. The parent probe passed all seven expected exit/status
assertions. Its first assertion version checked counts but not every exit
code; the harness was strengthened before the pinned observation was committed.
No failed post-commit attempt is hidden by that correction.
