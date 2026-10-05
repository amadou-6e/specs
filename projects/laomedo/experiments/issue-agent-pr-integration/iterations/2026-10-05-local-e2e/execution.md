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

The prospective protocol was committed at specs `767c84ebf28f306ed7e04f23c275f1d13d3062f7` before live preparation. The original probe was committed at Laomedo `9f676ceb818bccccd0b08b9e737e5fdc8829a442`. Compressed Langflow JSON decoding was fixed and tested at `7697588983677739f1e8f73258345330aaaf0d98` before any submitted turn. A fresh private attempt was frozen against that revision. The earlier zero-turn attempt and its imported flow remain separate private records.

Read-only preparation selected Laomedo issue #49 from a source-complete Work Graph snapshot and checked its body and update marker against the GitHub connector. The final Langflow attempt froze work key `github:I_kwDOUu9rs88AAAABUq5QtQ`, snapshot `sha256:f679b28c033e74d4921e4130942b635f4a6e306e92ec019f0aa2b7c67c0a0a39`, saved flow digest `sha256:b675b79f6301a99ed5d71981fd98e240029da16d4852b46cc64155c94cb894b2`, and skill revision `sha256:7c7462da8d7b3b68f1d05fea75d9e4f0904a55fb81a49bb40c00e24ba46c4b59`. The final flow import ID was `2041d45d-b560-42ec-94d1-20ef356418f6`. Its exported graph retained the pinned skill, runner URL, `gpt-6-luna`, and `low` effort.

The zero-turn Docker preflight passed with image ID `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239`, Codex CLI `0.159.2`, and permission config SHA-256 `a14cd7e8abb4216b16d29e55809c2c3c9a9c33cc0196fd459fc033aaaa1ea4c4`. It listed the requested model and effort, allowed a disposable workspace write, denied protected canonical and store writes, and denied command-worker auth-file reads. The private localhost runner returned HTTP 401 without its API token. The isolated Langflow server ran on `127.0.0.1:7863`; its saved flow imported and round-tripped without a model turn.

The user granted up to six submitted turns, including timeouts, and one draft PR from `test/49` to Laomedo `develop`. The grant was recorded in private state before dispatch. Two independent Langflow attempts each reserved a durable workflow run and reached a native Codex thread, but ended `failed` after repeated native error events, without a command result or verified artifact. A third, minimal direct-runner prompt failed the same way. At **3/6**, further identical submissions stopped pending diagnosis. The exact native error payload was not published; private raw rollouts and credentials remain outside Git.

An anonymous Docker-bridge TCP connection to `chatgpt.com:443` succeeded, an anonymous TLS request received HTTP 403, and `codex login status` in the private auth volume reported a ChatGPT login. Those checks did not prove model-service authorization. A fixed-schema runner diagnostic was then implemented at Laomedo `128b57ff6ff4649bfea276bb23e9a2a65cb1dcd6`, with synthetic tests that ensure free-text error fields cannot enter the run summary. Turn 4/6, a minimal direct-runner request, failed with nine `responseStreamDisconnected` events followed by one `other` event, and no reported HTTP status. No raw message was printed.

An authenticated no-model rate-limit read initially returned RPC code `-32603`. The private Docker login file differed from the host login and predated it by two days. The private copy was replaced from the current host file in a network-disabled container, without displaying either credential. The same no-model rate-limit read then succeeded. Turn 5/6 was a minimal direct-runner turn: its native thread completed, returned exactly `READY`, and recorded zero native errors. This sequence is consistent with a stale private login copy, although service recovery at the same time cannot be excluded.

After that direct gate passed, a fresh attempt froze code `128b57f`, specs `740ab36`, graph snapshot `sha256:83ddfe08a7c6c66e279df6158a9b55bd08cef90b4295d87b4f766b3fbca200cb`, and imported flow ID `ea8ce2f9-d52f-4053-b072-ced88c66dcac`. The final turn 6/6 ran through Langflow. Native run `4c6e709f-aa19-40c3-a4e5-695f68988d00` completed with three command results (exit codes `0`, `1`, `1`) and an agent response, but its post-run snapshot had no new non-skill file and no `experiments/exp19/agent-output.md`. Workflow run `bad38e64-6558-4c91-8185-743f8527ab05` and trace `0a91d30c-78e1-461f-9575-e49f18ab0b6a` retained failed status when artifact selection rejected the missing file. A separate zero-model command under the same policy created and read that nested path, so the file absence is not explained by the tested filesystem boundary.

The cumulative ledger is **6/6 submitted turns**. No agent artifact was accepted, `test/49` was not created, and the granted draft-PR write was not used. [Laomedo #68](https://github.com/amadou-6e/laomedo/issues/68) records the subscription-login diagnostic; [Laomedo #69](https://github.com/amadou-6e/laomedo/issues/69) owns the remaining artifact-production failure. All raw native events and credentials stay private outside Git.
