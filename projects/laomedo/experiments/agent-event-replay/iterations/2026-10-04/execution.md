---
title: Agent-event replay execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

On Windows with Python 3.12.10, Laomedo source
[`3115d5b`](https://github.com/amadou-6e/laomedo/commit/3115d5bec3f15f250f5b1605873185e537cbe3d4)
ran the source-only synthetic probe. The prospective protocol was already
committed at `c3b46f9` before that run. `python -m experiments.exp09.probe
--record` wrote the sanitized LF observation once; normal probe/test commands
do not rewrite it. The test checks a fresh deterministic observation against
the committed file.

`python -m unittest experiments.exp09.test_probe -v` passed 5 tests;
`python -m experiments.exp09.probe` passed; the main `python -m unittest
discover -s tests -p 'test_*.py'` suite passed 120; combined EXP-05/08/09
tests passed 10. Laomedo CI at this source revision passed Python 3.10 and
3.13 wheel tests plus checkout-based synthetic probes. `git diff --check`
passed locally. The fixture used temporary SQLite WAL databases, with
`synchronous=FULL`, and only synthetic payloads. No provider session, model
turn, Langflow server, Docker or network replay was invoked by the probe.

The code reopens the SQLite store object for a synthetic reconnect, not a
native or network connection. The crash case invokes EXP-05's restart sweep;
it does not kill a real backend. These are validity boundaries, not passing
evidence for those omitted mechanisms.

After the first run, an inspectability correction exposed the synthetic
`tool_call_id` in the sanitized readback and asserted that matching IDs remain
visible across reordered events and separate invocations. The prospective
cases and pass/fail threshold did not change. The tests and observation were
rerun at `3115d5b`; the original `ff743ce` result is superseded as the
evidence pin, not silently treated as the final artifact.
