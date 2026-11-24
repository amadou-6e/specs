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
The pilot clones a selected repository into app-owned storage. The owner selected
remote cloning and normal shell workspace access on 2026-11-23. Diff review,
commits, pushes and publication remain deferred. Chat receives selected graph files
and the general agent-files folder, not the entire checkout or Git metadata.

## Storage selection

The authenticated local profile selects a GitHub owner/repository and display name.
Clone its default branch into a fresh profile-owned directory. An optional one-use
read token supports private repositories; never retain it in repository configuration,
settings responses, logs, or provider workspaces. Run Git with isolated host
configuration, prompting disabled, hooks/filters disabled and HTTPS-only transport;
refuse redirects, submodules and symbolic links. A failed clone creates no connection.
The pilot accepts at most 10,000 regular files. Existing absolute checkout
registration remains filesystem-only. This is a single-user local pilot, not
hosted multi-user filesystem isolation.
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
authority before file effects and response release.

On first dispatch, freeze selected UTF-8 files into the conversation's normal native
shell workspace: `/draft/project/agent-files/` and
`/draft/project/graphs/<workflow-id>.json`. Retain the initial bundle for idempotent
retries. Maximum 256 files and 256 KiB serialized JSON; reject an oversized selection
rather than truncate it. Normal shell tools can read, edit, create and delete selected
files. Resumes retain the same native workspace and selected locations. Changing
storage settings applies to new conversations, never silently retargets an old one.
MCP project file tools use the same frozen locations as the shell, including an
initially empty selection; reads observe the current repository contents.
After a completed turn, read only the verified frozen workspace and persist changed
files against their original host hashes. Reject conflicting external changes,
unknown graph paths and protected names. Failed/interrupted turns are not exported.
Write-back failures retain the native snapshot and show a recoverable error while
unlocking Send. Each replacement is atomic, but a multi-file write is not a distributed
transaction. Reconciliation can retry already-written identical contents safely.
For a conflicting file, read the current repository text through `read_project_file`
and restore that exact content in the native workspace on a subsequent turn. The
identical-content check safely updates the baseline; later edits can save normally.
Remove unsupported paths or non-UTF-8 files from the native project tree before
retrying. A preflight refusal writes no files; Send remains available and recovery
does not require a new conversation. Preserve existing CRLF when decoding text.
Shell graph-file edits do not update app graphs until explicit Load; MCP graph
proposal approvals remain unchanged. No provider receives a host path or mount.
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
- Clone a selected repository; private read credentials never reach the provider.
- Configure an agent-files folder; chat reads and writes through its normal shell.
- Resume retains files; completed shell changes persist across new conversations.
- External edits conflict without overwrite; failures unlock Send and retain history.
- Wrong-owner requests, escaping paths, links and stale writes fail safely.
- Missing checkout and write failures preserve existing app data and give recovery.
- Inspect the actual controls in the integrated browser and review exact revisions.

UI authority: [storage controls](../design/project-storage.drawio).
