---
title: Visible pre-thread Stop execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The [Phase F protocol](https://github.com/amadou-6e/laomedo/blob/0b3053f2029fd754eb2e9abb2f720be397ab97e3/experiments/exp22/PHASE-F-PRETHREAD-PROTOCOL.md), browser start-mode switch, host response-hold probe and task were committed before dispatch. An independent review found a late-arrival path that could release a prepared worker before cancel. Commit `0b3053f` fenced new starts and made acknowledgement release conditional on cancelling every persisted run with verified cleanup. A focused recheck cleared that blocker. A no-model disposable UI preflight opened Playground without Send; the full host suite passed 366 tests with 9 skipped. Tested source: Laomedo `0b3053f2029fd754eb2e9abb2f720be397ab97e3`.

One visible browser Send then created a prepared run in a real local runner. The test host held the runner's early HTTP acknowledgement; the worker's ordinary response gate remained closed. The browser clicked visible Stop, causing an authenticated request lookup and exact cancel before the acknowledgement was released. The runner became terminal `cancelled` with confirmation, and only then did the hold open. The shared authorization ledger moved from 5/12 to 6/12, conservatively counting the request; no native model call occurred. The runner login volume was available but no Codex stage launched. No real GitHub credential, grant or write entered the test.

The private browser, route, runner and teardown records were checked independently after the run. See [results](results.md) and [manifest](evidence/manifest.md).
