---
title: Visible Playground Stop execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The user extended the private shared EXP-22 ledger by eight submitted turns, from cap 4 to cap 12, preserving all four prior entries. The Laomedo Phase E protocol, task, browser probe and host probe were committed before the first Phase E submission. An independent Claude review found that a browser disconnect might be mistaken for Stop propagation. Commit `84c1b29` added click, authenticated-cancel, terminal-observation and context-close timing; a focused recheck cleared the blocker. A later review found two turn-waste risks, so commit `19e726a` isolated the live task from the fake-preflight environment switch and made the host compare both embedded flow components with their source byte for byte. The frozen tested source was Laomedo `35a7d3c3f5518e5479b18b9d78a2f67c9b9394ac`.

Credential-free gates first opened the disposable server's Playground without Send, then ran the same saved flow against a fake runner. The visible Stop produced one matching lookup and cancel with no synthetic effect after its six-second effect window. The final real-runner preflight checked the pinned images, model/effort, existing private login volume, skill, flow import and Playground availability. The host suite passed 362 tests with 9 skipped, including targeted tests for ledger preservation, code mismatch and disconnect attribution.

One model submission then ran through the disposable Langflow 1.12.3 server and a fresh one-turn local Codex runner with `gpt-6-luna` at low effort. The browser clicked visible Stop after native long-command start. The shared ledger moved from 4/12 to 5/12; no retry occurred. The provider-login copy remained mounted in the Codex stage under the approved local boundary; it was not mounted in Langflow. No real GitHub credential, grant or write was used. The private result, route audit and teardown were checked after the run. See [results](results.md) and the [manifest](evidence/manifest.md).
