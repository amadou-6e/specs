---
title: Long-call timeout execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

On Windows with Python 3.12.10 and Docker 27.3.1, the pinned Langflow 1.12.3
image ran in one disposable container published only on `127.0.0.1:17870`.
The synthetic runner listened only on loopback **inside** that container,
used a synthetic token, and wrote one entry/effect record per request to a
temporary named volume. The volume and container were removed after capture.
No model turn, real agent runner, GitHub write or personal credential was used.

The source [protocol](../../protocol.md) was committed at `e4f4685` before
execution. The first start failed on fresh-volume permissions (image UID 1000);
the second reached Langflow but failed flow creation because the copied
example's fixed ID collided. Both stopped **before any case dispatched**.
The fixture initialized volume ownership and omitted the copied flow ID.
The valid third start ran the four frozen calls once each, on 2026-10-05
09:53 UTC, with no retry of a potentially active call. Its verbose live
response was manually condensed for the first committed observation at
`dee05c2`; that file does not prove the final capture code produced its own
compact shape. A prospective [amendment](../../protocol.md) was committed at
`8ceb50d` before a separate four-call replication at 10:13 UTC. The current
compact observation at `1fc002a` was written directly by the probe, not
manually edited. Both valid runs retain one entry/effect per case and the same
qualitative outcome; first-run data remains pinned in Git history.

Effective v2 server timeout was read back as **3 seconds** before calls.
`python -m experiments.exp10.probe --record` produced the compact
[replication observation](evidence/manifest.md) at Laomedo `1fc002a`.
`python -m unittest experiments.exp10.test_probe -v` passed four checks,
including mutations that remove a late effect or fabricate a safe/timely
response. The main `python -m unittest discover -s tests -p 'test_*.py'`
suite passed 120 tests; `python -m compileall -q experiments/exp10` and
`git diff --check` passed. These are local checks, not native provider tests.
