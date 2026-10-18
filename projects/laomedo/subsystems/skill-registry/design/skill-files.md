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
| SF03 | Header displays the shortened current revision (full hash on hover) and Read only. Close returns to the unchanged graph. |
| SF04 | Explorer folders expand/collapse and files open tabs; default SKILL.md; closing a tab chooses another open file. |
| SF05 | Source uses locally bundled Monaco, read-only, syntax highlighting and editor search. Markdown files also offer Preview. |
| SF06 | Markdown preview skips raw HTML and remote images, renders links as text, and never executes scripts or commands. |
| SF07 | Loading has status text. Missing/invalid/corrupt or oversized revision has a fixed error and Retry. No stale file survives a changed selection. |
| SF08 | Binary source files show metadata and an unsupported-preview message. No download/write/run action. |
| SH06 | Between skill identity and the file workspace, horizontal dividers surround the complete summary/description. No card frame or separate heading. The summary remains visible; clicking its disclosure row expands/collapses the full documentation, initially collapsed, including local images/workflow diagrams. |

The operations/history page of the same Draw.io adds SO01–SO03 (ordinary or
two-node feedback proposals), SH01 (one combined files/history workspace), SH02
(parent-linked commit graph below the file tree), SH03 (cumulative selected-revision
to pinned-current visual diff of the selected file, with file switching retaining
the commit, and explicitly backend-asserted Agent provenance), SH04
(loading, empty and fixed error/retry states), and SH05 (draggable and keyboard
resizable navigation/content separator), plus SH06 (collapsible summary and full
revision-local documentation). Its public
contract is [Skill operations](../contract/skill-operations.md). File browsing
stays read-only; the graph's Operation input creates candidates separately.

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
Recognized PNG/JPEG/GIF/WebP bytes may include an optional `image_data_url`
(base64 data URL) in their file entry, generated only after complete tree/hash
verification under the same read limits. Other binary contents remain metadata. Image embedding is opt-in for viewer
reads only; operation preparation and Agent snapshots never include inline image
data and retain binary metadata only.
SVG remains UTF-8 text and is sanitized in the overview before use as an inert
image; no inline SVG markup or remote resource loading is allowed.
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

## Skill overview

The summary shows the complete normalized current pinned `SKILL.md`
frontmatter description (quoted scalars and folded/literal blocks supported),
or its first prose paragraph. Never truncate at punctuation or abbreviations;
long descriptions wrap fully. No model call generates or changes it.
The complete summary is the first visible line, wrapping when needed, between
top and bottom dividers without a card frame. All detailed documentation starts
collapsed. Clicking the summary row or activating it with Enter/Space toggles
the bounded-height article; the sentence and file/commit selection remain visible. The overview always describes the pinned
current revision, including while comparing a historical commit.

Authors may put human-oriented purpose, usage, limitations and workflow
illustrations in optional root `OVERVIEW.md`. Otherwise the full view renders
`SKILL.md` without frontmatter. Both are versioned and diffable bundle files.
Local Markdown links navigate documents within the same snapshot, with Back to
overview. Images resolve relative to the displayed document and only to files
in that snapshot. Bundled raster images and sanitized SVG workflow diagrams
are supported; remote URLs, host paths, scripts, embedded HTML and external
SVG resources are not rendered. Unsupported/missing media shows an explicit
placeholder. The existing source/preview and immutable history remain available.


### Missing summary authoring

The internal `laomedo/resources/skills/skill-summary/SKILL.md` in the implementation repository
guides an authoring Agent to fill a missing or blank `SKILL.md` frontmatter
`description` with one grounded, self-contained purpose sentence. Preserve
existing user descriptions unless rewriting is explicitly requested. Unclear
purpose needs clarification rather than invented capabilities. Registry edits
use normal host-validated Skill Operations with an exact parent, immutable diff
and execution provenance. This authoring skill is not invoked by viewing a
skill; automatic runtime dispatch is not introduced by this UI change.


## Collapsible navigation

SH07 in the navigation-states Draw.io page owns two independently collapsible
sections, Files and Commits, with compact uppercase headers, disclosure chevrons
and three-dot action disclosures. Both start expanded and share the available
height. Collapse either to let the other use all remaining height beneath both
headers. Keep bodies mounted so file, commit, scroll and pagination state survive.
Section actions expand only that section or expand both. The column header
three-dot actions hide navigation or reset its width.

SH05 accepts widths 0 or 180-600 px, further bounded to retain editor space.
Dragging below 90 px snaps closed; dragging right past that threshold restores
a visible width. Keep a grabbable divider at width 0 and a Show navigation button
that restores the previous visible width. Double-click toggles; Home collapses,
End maximizes, and ArrowRight from collapsed restores. ArrowLeft at minimum
collapses. Restore neither resets selection nor reloads history.

## Automatic missing-summary authoring

Preparing an authorized edit of a pinned skill with no meaningful frontmatter
description adds the packaged internal summary skill to the trusted authoring
instructions. The existing Agent performs the requested edit and supplies one
grounded summary sentence in the same operation. The host rejects a still-empty
description on apply and records the accepted edit with its existing parent,
diff and backend provenance. Existing descriptions do not trigger this addition.
Unknown nonempty YAML values are preserved conservatively. This does not dispatch
a model from import, discovery or viewer reads, and does not promote canonical
latest. Runtime generation requires the ordinary authorized authoring graph.
