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

**Open owner decisions after independent review:** local-checkout-only connection
and MCP-only rather than native shell workspace access are implementation proposals,
not recorded owner approvals. The owner has been asked whether the pilot must clone
a selected repository and expose selected files in the normal shell workspace.
Resolve these questions before claiming the pilot fulfills the selected scope.

## Storage selection

The authenticated local profile registers an absolute checkout path and a display
name. Verify the checkout through filesystem inspection only; never invoke Git,
repository configuration, filters, hooks or repository code during registration.
This is a single-user local pilot: selecting a host checkout is an explicit profile
grant to its chosen subtrees, not hosted multi-user filesystem isolation.
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
on the existing graph. Match by original node identity and unchanged component type;
new nodes or changed component types receive installed defaults, never another
node's private settings. Deleted nodes lose their settings in the loaded graph;
files targeting a different workflow are refused. Loading does not execute the graph.
Use the complete saved Flow digest as the app revision and SHA-256 of current file
bytes as the file revision. Refresh observes external file changes; saving a new
location requires absence. Reject stale app/file revisions rather than overwriting
concurrent edits. Each successful load creates a new opaque editor epoch. Existing
editors cannot save data with an older/missing epoch over that graph. Reload obtains
the new epoch; subsequent editor saves preserve it. Metadata-only updates remain
supported. File and database are separate stores: a metadata/DB failure after a file
write reports incomplete synchronization; it does not claim the file write was undone.

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
Prompt text and ordinary graph values are exported; secret-field filtering is not
content classification. Agent files and graph definitions may be committed by the
user and this is disclosed. The app never commits them automatically. Maximums:
30 connections, 40 graph nodes, 100 edges, 256 KiB per readable file, 65,536 text
characters per agent write, 1,000 directory entries per listing. Existing links and
junctions are refused. Host processes that maliciously mutate directory ancestry
concurrently are outside this local pilot's filesystem-isolation claims.

## Acceptance

- Two graphs retain independent file locations across service restart.
- Save/load a supported graph without execution or loss of app-managed secrets.
- Configure an agent-files folder; chat reads and writes a text file there.
- Wrong-owner requests, escaping paths, links and stale writes fail safely.
- Missing checkout and write failures preserve existing app data and give recovery.
- Inspect the actual controls in the integrated browser and review exact revisions.

UI authority: [storage controls](../design/project-storage.drawio).
