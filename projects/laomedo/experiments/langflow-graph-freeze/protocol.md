---
title: Langflow graph freeze protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

Build a Chat Input -> pause component -> marker component -> Chat Output graph using the installed 1.12.3 custom-component template API. Import it into a disposable local server. Hash the stored graph and marker source. Start a run; the pause component writes an entered sentinel and waits for a release file. While paused, patch the saved marker's field from BEFORE to AFTER and its source to prepend EDITED. Re-read and hash the saved graph and source, then release. Run again to prove the edit was effective for a new launch.

The active run passes the behavioral gate only if it returns TASK|BEFORE and the next run returns TASK|EDITED-AFTER. A full freeze claim additionally needs a durable, run-bound graph revision and component identity. If Langflow does not emit those identities, report that separately as unmet. Use one disposable server, no model turns, no agent dispatch or personal credentials. This written protocol records the executed procedure; it was not a separately reviewed preregistration.
