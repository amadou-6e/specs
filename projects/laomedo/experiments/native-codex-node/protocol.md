---
title: Native Codex node acceptance protocol
status: complete
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol and authorization

The prospective sequence was recorded in implementation commit 6596ddd before
the first model turn: installed catalog/flow round trip, invalid-input checks,
fresh marker write/read, restart/resume, independent fresh run, and cancellation
after a native command-start event. Cap: four submitted turns, including timeouts.
Existing private Docker login and permissions were reused; no new auth copy.

This page is a retrospective index of that plan and its execution, not a claim
that every verifier line was frozen. Windows UTF-8 trace reading, the expectation
of unchanged post-resume hash, and streaming-output detection were corrected
after observations. Preserve those deviations in the attempt.

Acceptance gates: the actual installed catalog exposes the component; imported
flow emits answer/run identity; native tool evidence supports reads/writes;
resume binds the exact input snapshot and same native thread after restart;
fresh host workspace is independent; invalid/missing state and exhausted caps
consume no turns; explicit native cancellation retains partial evidence.

A native completed turn or an assistant claim does not prove tool completion,
task success, cancellation or sandbox denial. Raw traces stay outside Git.
An additional turn requires explicit authorization and retained ledger; do not
reset the four-turn attempt. UI Stop propagation is excluded and tracked in #22.

The user subsequently authorized two additional submissions, increasing the same
ledger cap to six without resetting its prior count. The corrected command-start
cancellation trigger and explicit fresh fixture paths were announced before
execution and are recorded as a [separate retry](iterations/2026-10-01-retry/README.md).
The original four-turn attempt remains unchanged; this retrospective extension
record does not claim an immutable prospective verifier.

