---
title: Read-only Skill files in Langflow
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-12
applies_to: [laomedo]
supersedes: null
related: []
---

# Read-only Skill files in Langflow

Tracking: [specs #370](https://github.com/amadou-6e/specs/issues/370) and
[Laomedo #154](https://github.com/amadou-6e/laomedo/issues/154).
The owner selected implementation. The editable [interaction model](skill-files.drawio)
owns panel geometry, visible states and transitions; this page indexes it.

## Interaction index

| ID | Behavior in the diagram |
| --- | --- |
| SF01 | The selected LaomedoSkill node exposes Skill files in place of its primary Code action. Other nodes keep Code. |
| SF02 | Opening the panel captures Skill ID and exact revision; no model turn or graph execution occurs. |
| SF03 | Header displays full selected revision and Read only. Close returns to the unchanged graph. |
| SF04 | Explorer folders expand/collapse and files open tabs; default SKILL.md; closing a tab chooses another open file. |
| SF05 | Source uses locally bundled Monaco, read-only, syntax highlighting and editor search. Markdown files also offer Preview. |
| SF06 | Markdown preview skips raw HTML and remote images, renders links as text, and never executes scripts or commands. |
| SF07 | Loading has status text. Missing/invalid/corrupt or oversized revision has a fixed error and Retry. No stale file survives a changed selection. |
| SF08 | Binary files show metadata and an unsupported-preview message. No download/write/run action. |

## API and boundary

Serve GET `/api/v1/laomedo/skills/{skill_id}/{revision_id}` under the existing
Langflow current-user authentication. Require a valid supported skill ID and an
exact immutable SHA-256 revision; never resolve latest or accept a host path.
Only the configured read-only registry is visible, not agent workspaces, drafts,
provider profiles or credentials. Verify the bundle tree and individual file
hashes before returning a consistent snapshot. Reject symlinks, junctions,
hardlinks, special files and path escapes. Error responses contain fixed codes,
not filesystem paths or raw exceptions. No write API is added.

Bound reads to 128 files, 512 KiB per file, 4 MiB per bundle and 64 KiB metadata. Limit traversal to 128 directories and depth 16.
The response identifies schema, skill/revision/tree hashes and sorted relative
file paths, byte lengths, file hashes and UTF-8 text or binary metadata.
Responses use no-store. The response supplies every file for local browsing,
so tab switches do not silently fetch a newer revision.

This is the registered bundle offered to an agent; inspecting it does not prove
that the agent read it. The selected revision stays fixed until the node's
reference changes. Local single-user access follows existing Langflow login;
no second provider login or public unauthenticated skill endpoint is added.

## Implementation and verification

Use a reproducible overlay for upstream Langflow v1.12.3 rather than vendoring
upstream. Bundle Monaco and its worker locally, with no CDN loader. A backend
app factory installs the authenticated route and serves the overlay build.
Activation adds a read-only registry mount and preserves the saved graph,
SQLite volume, loopback binding, existing provider/runner credentials and
sandbox policy. This configuration requires a concrete reviewed deployment
draft and owner approval, separately from implementation.

Verify real registry bytes, revision/hash corruption, malformed identities,
link/path rejection, size limits, binary handling, authentication and no writes.
Browser checks open the real Skill node action, traverse nested files, switch
and close tabs, search source, preview Markdown safely, refuse edits, show
errors and preserve graph identity without executing it. Use credential-free
fixtures. No live model turns or GitHub publication writes are required.
