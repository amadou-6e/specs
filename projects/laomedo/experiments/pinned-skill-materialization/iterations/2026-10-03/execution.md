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
[`0ed7dfac`](https://github.com/amadou-6e/laomedo/commit/0ed7dfac634b8c650b7022edcfb390e35b8c40e1),
`python -m experiments.exp08.probe` passed without modifying evidence;
`python -m experiments.exp08.probe --record` wrote the LF-only sanitized
observation. `python -m unittest experiments.exp08.test_probe` passed one
LF/CRLF invariant test. The main local
`python -m unittest discover -s tests -p 'test_*.py'` suite passed 120
tests. A separate CI checkout-based step runs the experiment while the
existing installed-wheel suite remains outside the checkout; CI results
must be checked on the PR.

The revised fixture created an actual source Git repository and two disposable
agent clones. The unprotected clone showed pollution under status/add-all/clean;
the clone with `.git/info/exclude` stayed clean under ordinary Git commands.
It also checked tracked-file LF-to-CRLF conversion and the force-clean hazard.
The fixture used `LocalRunner._materialize` directly,
with Docker checking disabled and a zero model-turn cap. No Codex/Claude
session, native skill-discovery event, private credential or network write
was involved. All temporary state was removed after readback. This revision
corrects the first fixture's invalid Git-cleanliness inference: its materialized
skill was outside any Git checkout.
