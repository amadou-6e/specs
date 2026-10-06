---
title: EXP-19 local end-to-end attempt
status: draft
kind: experiment-iteration
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Local end-to-end attempt

This attempt follows the [prospective local protocol](../../protocol.md#local-authenticated-end-to-end-attempt) and the updated [EXP-19 issue](https://github.com/amadou-6e/laomedo/issues/49). It uses the existing single-user subscription-backed runner without first building the later browser-auth flow. [Execution](execution.md), [results](results.md), and the [evidence manifest](evidence/manifest.md) record the frozen inputs, six submitted turns, a successful minimal direct-runner gate after a private login refresh, a completed Langflow agent turn with no output artifact, and an unused draft-PR grant. [Laomedo #69](https://github.com/amadou-6e/laomedo/issues/69) owns the remaining artifact failure.
