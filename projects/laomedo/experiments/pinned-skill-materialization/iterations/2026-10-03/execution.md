---
title: Pinned skill materialization execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

On Windows/Python 3.12.10 at Laomedo
[`1b6c1c6`](https://github.com/amadou-6e/laomedo/commit/1b6c1c6d1aee3f4e223900cf975ce7bc8e246bc0),
`python -m experiments.exp08.probe` passed and wrote the sanitized
observation. `python -m unittest experiments.exp08.test_probe` passed one
LF/CRLF invariant test. The main local
`python -m unittest discover -s tests -p 'test_*.py'` suite passed 120
tests. A separate CI checkout-based step runs the experiment while the
existing installed-wheel suite remains outside the checkout; CI results
must be checked on the PR.

The fixture created temporary Git repositories, skill stores, runner state
and effective workspaces. It used `LocalRunner._materialize` directly,
with Docker checking disabled and a zero model-turn cap. No Codex/Claude
session, native skill-discovery event, private credential or network write
was involved. All temporary state was removed after readback.
