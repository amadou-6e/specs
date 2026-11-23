---
title: Repository storage pilot
status: draft
kind: contract
owners: [laomedo-maintainers]
last_reviewed: 2026-11-23
applies_to: [laomedo]
supersedes: null
related: []
---

# Repository storage pilot

Owner request: [Laomedo #309](https://github.com/amadou-6e/laomedo/issues/309).
The pilot connects existing local Git checkouts. Remote cloning, synchronization,
diff review, commits, pushes and publication are deferred. A connection grants no
access to the entire checkout: chat sees only selected graph files and the selected
agent-files directory through authenticated Laomedo MCP tools.

## Storage selection

The authenticated local profile registers an absolute checkout path and a display
name. Require an existing Git checkout; do not execute repository code or Git hooks.
Persist connections per profile. Each saved graph can independently select a
connection and relative JSON filename. A profile selects one general agent-files
directory within one connection. Selecting another location does not move/delete
existing files. Configuration never comes from model tool arguments.

## Graph files

Provide explicit Save graph file and Load graph file actions in the pilot. Editor
autosave still updates the app database; show that file synchronization is explicit.
Save a portable graph definition using the existing authoring projection, with name,
workflow identity, original node identity map and format version. Never export native component code or secret
fields. Refuse unsupported/oversized graphs rather than silently truncating them;
disclose omitted app-managed settings. Import structurally validates the portable
definition with the installed component catalog and preserves app-managed settings
on the existing graph. Loading does not execute the graph. Reject stale app/file
revisions rather than overwriting concurrent edits. A failed operation preserves
the existing graph and file; incomplete synchronization is reported, never success.

## Agent files and chat

Provide bounded list/read/write MCP tools. Graph files are read-only through these
file tools; graph edits continue using the existing graph approval path. Agent files
are ordinary persistent text files available across conversations and restarts.
Writes require the observed file hash, or an explicit absent-file condition. Reject
path traversal, absolute child paths, symlinks/junctions, Git metadata, environment
files and credential/private-state locations. Credentials and operational databases
are not copied or mounted into provider containers. Chat receives relative paths,
not unrestricted host filesystem access. Enforce current profile/session/attempt
authority before file effects and response release. Native shell workspace remains
isolated; repository access is through the MCP tools, not an unrestricted mount.

## Acceptance

- Two graphs retain independent file locations across service restart.
- Save/load a supported graph without execution or loss of app-managed secrets.
- Configure an agent-files folder; chat reads and writes a text file there.
- Wrong-owner requests, escaping paths, links and stale writes fail safely.
- Missing checkout and write failures preserve existing app data and give recovery.
- Inspect the actual controls in the integrated browser and review exact revisions.

UI authority: [storage controls](../design/project-storage.drawio).
