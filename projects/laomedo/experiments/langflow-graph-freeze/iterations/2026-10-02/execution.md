---
title: Langflow graph freeze execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

Host: Windows workspace, Docker Engine 27.3.1. Langflow image digest sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0. Laomedo probe branch: feat/33. The pinned image was already local. The builder ran with network none and mounted only the fixture directory. A disposable Langflow server listened at 127.0.0.1:17863; existing pilot containers were untouched. Its auto-login token remained only in probe memory.

The first API attempt used /api/v1/run/{id} and returned 403 because that route requires an API key. Source inspection found /api/v1/run/session/{id}; the corrected probe used that session-auth route. It imported a synthetic flow, captured stored hashes, paused at the entered sentinel, patched the saved marker source and field, captured new hashes, released, and ran the saved flow again. The fixture used zero model turns and no agent dispatch. Raw synthetic output is linked in the evidence manifest. The experiment did not test concurrent database transactions, arbitrary built-in nodes or server restart.
