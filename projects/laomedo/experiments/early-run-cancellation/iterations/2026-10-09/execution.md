---
title: Installed Langflow graph cancellation execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The Phase D protocol, task and probes were committed at Laomedo `21cb611` before the turn. A credential-free pinned-Langflow graph test against a fake runner passed with one start, matching lookup and cancel, and no late synthetic effect or runner-token output. A separate no-model readiness check found the existing private provider-login volume, pinned Codex image, model/effort and pilot skill. The host suite passed 354 tests with 9 skipped. An independent Claude review blocked on failure-path teardown. The exact-cleanup and route-audit fix was committed at `bda5a6b`; its focused recheck gave a go. The full host suite then passed 358 tests with 9 skipped.

One final model submission was made through the installed Langflow 1.12.3 graph and a fresh one-turn local Codex runner using `gpt-6-luna` at low effort. The shared private four-turn ledger moved from 3/4 to 4/4. The provider-login copy was mounted in the Codex stage under the approved local boundary; no real GitHub credential, grant or write entered the test. The host signalled graph cancellation after the native long-command start. The machine result and independent teardown check are summarized in [results](results.md), with private artifact pins in the [manifest](evidence/manifest.md).
