---
title: OpenCode authenticated verification sources
status: complete
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- Implementation PR [#31](https://github.com/amadou-6e/laomedo/pull/31), including
  examples/opencode-agent/direct_cli.py, flow_acceptance.py, cancel_acceptance.py
  and live-success-evidence.json.
- OpenCode CLI 1.18.33, pinned controller image
  sha256:73313fbaf91940471244ff0efb2442a333de119389875765a63bc168fec181fd.
- Existing command-worker image sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239.
- Langflow 1.12.3. Exact model: opencode-go/gpt-6-luna; variant default.
- Account and protocol source references are owned by the provider contract.

Private Console credentials, organization identifiers, raw messages and full native
worker events are not repository evidence. Default legacy auth-list output did not
describe the Console login; resolved debug config redacted its credential.
