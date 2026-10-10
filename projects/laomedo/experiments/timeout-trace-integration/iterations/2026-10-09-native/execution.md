---
title: Native reconciliation prospective execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Frozen execution and cleanup amendment

The original protocol and tasks were committed at
[add9661](https://github.com/amadou-6e/laomedo/commit/add96614a73f19d6dd64c321635d5100a96d5aa9)
before execution, on develop base `bd285cf`. Claude approved the production
implementation at `b2e98a0`, but refused the pre-run because a ledger-finalization
failure could skip cleanup. The prospective amendment and two fault-injection
controls were committed at [bec25c0](https://github.com/amadou-6e/laomedo/commit/bec25c0cfcd3b148acfb3caac9cd7e0c1866182d).
The same reviewer approved that focused B1 recheck before either live turn.
No task, expected result, timing or budget changed.

Both cases ran once from clean frozen head `bec25c0cfcd3b148acfb3caac9cd7e0c1866182d`. Fresh no-model native
preflight passed, and a no-model check of the existing private login returned
HTTP 200, allowed true, without requesting a refresh. The pre-run host suite
passed 294 tests with six skips. The approved private non-split Codex 0.159.2
profile and Docker permissions were unchanged. Each fresh outside-Git runner
used one `gpt-6-luna`/low turn. Shared ledger entries 11 and 12 were reserved
before dispatch; timeouts counted and no retries occurred. No GitHub credentials,
grants or writes were involved.

| Case | Host start UTC | Five-second deadline observed | Command/effect boundary after deadline | Cancel after start |
| --- | --- | --- | --- | --- |
| Before | 2026-10-10T06:21:36.323223Z | 5.031 s | 2.047 s | 7.078 s |
| During | 2026-10-10T06:22:32.952932Z | 5.016 s | 6.375 s | 11.391 s |

The production RunnerTraceBridge/RunnerAdapter performed one async HTTP start
per case. The real five-second host wait expired with an early native identity
already bound. The before task slept 30 seconds before writing FIRST. The during
task wrote FIRST, slept 30 seconds and would have appended SECOND. The host
observed each started command after timeout and cancelled that exact run. In the
during case, the host observed exact FIRST bytes and attached their hash to the
same invocation before cancellation. The named file was checked 31 seconds after
the command boundary. Host monotonic clock resolution was 0.015625 s; no
cross-machine clock subtraction was used.

Each host store was reopened in a fresh process. Raw partial events and the login
remain private. The [machine projections](evidence/manifest.md) retain identities,
receipts and selected native command/interruption events without model text or
tool output. Exact cleanup and server shutdown were verified in both cases.

After the runs, CI exposed a test-placement error: the cleanup regression was in
the installed-wheel suite, although experiment modules are not packaged. The test
was moved unchanged to `experiments/exp66/test_cleanup.py` at `d43e5ca`.
The probe, task, protocol and production code were unchanged. This was not a
model retry or a modification of the frozen observations.
