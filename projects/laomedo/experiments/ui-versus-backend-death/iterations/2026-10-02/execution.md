---
title: UI versus backend-death execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

Windows host, Docker Engine 27.3.1, pinned Langflow 1.12.3 image digest sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0. The disposable server listened only on 127.0.0.1:17866. A named volume held only synthetic run data and the server's temporary auto-login state. It was removed after evidence capture. The Laomedo package and experiment fixture were mounted read-only. The startup wrapper swept nonterminal Laomedo runs before starting Langflow.

The first startup failed because the non-root image user could not write the new volume. The disposable volume owner was changed to UID 1000, and startup succeeded. The probe then imported two synthetic flows; closed one HTTP client socket while its stage waited; read the saved flow through a new session; released the stage; started the second run; hard-killed the server container; restarted it with the same volume; and inspected the run record. The read-only mounts exposed only test code, no personal credentials. The fixed component source marker and one-node graph descriptor are synthetic IDs, not a full production flow/code attestation.
