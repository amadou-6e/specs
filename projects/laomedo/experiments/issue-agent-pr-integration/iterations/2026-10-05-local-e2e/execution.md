---
title: EXP-19 local end-to-end execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The prospective protocol was committed at specs `767c84ebf28f306ed7e04f23c275f1d13d3062f7` before any live preparation. The probe code was committed at Laomedo `9f676ceb818bccccd0b08b9e737e5fdc8829a442`. No model turn or GitHub write has occurred.

Read-only GitHub preparation fetched a source-complete Work Graph snapshot for `amadou-6e/laomedo`, selected issue #49, and checked that the issue context and GraphQL source body/update marker agree. It froze work key `github:I_kwDOUu9rs88AAAABUq5QtQ`, snapshot `sha256:e55b3b5bde7d8049a0f86ea055f18201ac831a687d88334b4bf93faab87cecb2`, saved flow digest `sha256:b675b79f6301a99ed5d71981fd98e240029da16d4852b46cc64155c94cb894b2`, and skill revision `sha256:7c7462da8d7b3b68f1d05fea75d9e4f0904a55fb81a49bb40c00e24ba46c4b59` in private state outside Git.

The zero-turn Docker runner preflight passed against the existing private subscription-login volume, pinned image ID `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239`, Codex CLI `0.159.2`, and permission config SHA-256 `a14cd7e8abb4216b16d29e55809c2c3c9a9c33cc0196fd459fc033aaaa1ea4c4`. It listed `gpt-6-luna` with `low` effort. The disposable workspace write exited 0; writes to canonical and store mounts exited 2, and a command-worker read of the auth file exited 1. A localhost runner with a zero-turn cap then returned HTTP 401 for an unauthenticated status request.

Next: import and round-trip the saved flow on the isolated Langflow server, then record the explicit submitted-turn cap and exact draft-PR write grant. Until those steps complete, model dispatch and publication remain pending. Credential and native raw-event files stay in private state outside Git.
