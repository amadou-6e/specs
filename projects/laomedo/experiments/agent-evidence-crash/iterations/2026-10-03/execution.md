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
[`e274903`](https://github.com/amadou-6e/laomedo/commit/e274903242a4f1724fc598ba50de9cff4f433690),
run `python experiments/exp05/probe.py`. The parent starts seven child
processes in independent temporary SQLite databases. Each uses WAL and
`synchronous=FULL`, exits at its selected boundary, and is inspected after
a restart sweep. Raw projection is derived only from committed receipts.
The test fixture uses a synthetic provider string and synthetic event payload.
No Langflow server, Codex/Claude session, model call, network write, private
credential, or personal workspace is used.

`python -m unittest experiments.exp05.test_evidence` passed 4 tests,
including identity validation and repeat sweep. The main
`python -m unittest discover -s tests -p 'test_*.py'` suite passed 120
tests locally at this revision. CI invokes that suite against the installed
wheel and runs source-only experiment tests separately. The parent probe passed
all seven expected exit/status
assertions. Its first assertion version checked counts but not every exit
code; the harness was strengthened before the pinned observation was committed.
An initial CI run at `9bcb64a` failed because a wheel-only test attempted
to import an uninstalled `experiments` module. The test was moved to the
experiment directory and given a separate checkout-based CI step in
`e274903`; the prior failure is not treated as a passing check.
