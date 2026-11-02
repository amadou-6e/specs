---
title: Skill workspace in Langflow
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-12
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill workspace in Langflow

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
| SF05 | Source uses locally bundled Monaco, read-only, syntax highlighting; SH08 owns workspace search. Markdown files also offer Preview. |
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

## Navigation disclosure (SH02 / SH07)

Find, Files and Commits use their own chevrons, without redundant action menus. The
single SKILL menu offers **Collapse all** only when all three sections and every
folder are open. Otherwise it offers **Open all**, including mixed disclosure
states. The action changes all three sections and all folders; it preserves the
selected file, tabs, commit, scroll and pinned current revision. Individual
chevrons still work. Hide navigation and Reset navigation width remain separate
menu actions, with existing keyboard, Escape/outside dismissal and focus rules.
The diagram records all-open, mixed, all-closed and hidden-column states.

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

SH07 owns the compact uppercase Files and Commits headers (SH08 adds Find) and their disclosure
chevrons, without per-section action menus. Open sections share the available column
height; when one closes, the others fill the remaining height. Keep section and
folder bodies mounted while hidden so file, tab, commit and scroll state survive.
The SKILL menu owns the single state-aware Collapse all / Open all action,
including folders nested inside closed sections. With no folders, all three sections
open counts as all open. Hide navigation and Reset navigation width remain
separate. The selected source/comparison stays visible when all sections close.
After the bulk action flips its label, close the menu and return focus to its
trigger. Reset disclosure only when the selected Skill/revision changes.

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


Action disclosures close on Escape and outside pointer interaction; Escape
returns focus to their trigger without closing the Skill files dialog. Leaving
the actions with keyboard focus also dismisses them. Restoring the hidden
column returns focus to its persistent separator. Menu text uses foreground
contrast and sizes to its action labels.

Only the internal skill's Agent instructions are inserted into the authoring
task, in a clearly delimited trusted block. Omit the skill's YAML metadata and
host integration documentation. Restate the single-JSON-object operation
contract after the snapshot. The Agent proposes content and never invokes host
prepare/apply or supplies provenance. Apply must leave a meaningful description,
including when an edit would otherwise remove an existing one.


## Workspace Find and full-page viewing (SH08 / SH09)

The diagram's fourth page owns these controls and states. Find is a third
collapsible section in the Skill sidebar, initially closed. It searches the
pinned current snapshot's text files locally, with literal case-insensitive
matching and an Aa case toggle. Group matching lines by file, showing line
numbers and bounded highlighted snippets. Empty queries prompt for text; no
matches are explicit. Limit displayed matching lines to 500 and disclose
truncation. Binary and historical-only files are excluded. Result selection
returns to current source, opens the file and selects/reveals its match.
Repeated selection works. Collapse/reopen retains the query and results.
Ctrl/Cmd+F opens and focuses Find; Escape inside Find collapses it and returns
focus to the header. Remove the old Find in file button and editor find widget.
The SKILL bulk action includes Find as well as Files, Commits and folders.

Full page and Restore window resize the same accessible dialog within the
browser viewport. Preserve file, tabs, commit, search, disclosure and navigation
width; do not navigate away or use the browser fullscreen API. Retain close,
Escape, focus trapping and resizing. Snapshot/history loading and failure/Retry
states remain distinct from an empty search. These controls are read-only and
never dispatch a graph, model, edit or external resource request.

Acceptance covers cross-file/nested matches, case/no-match/empty states, result
selection after history comparison, repeated selection, collapse/reopen and
keyboard focus, full-page/restore with preserved state at normal/small
viewports, and existing real failure/Retry paths. Proposed design is not
implementation or owner acceptance.


## Explorer type icons and disclosure (SH10)

The fifth Draw.io page owns the explorer row geometry. Place a locally bundled
16 px file-type logo immediately before each filename, with a generic fallback
for unknown names/extensions; known names such as Dockerfile may use their
type logo. Use the installed VS Code Codicon chevron-right/down for
folders and section headers instead of filled text triangles. SH10 supersedes
the older state diagrams' filled-arrow glyphs. Reserve a
chevron slot on file rows to align root and nested filenames consistently.
Icons are decorative; retain filename-only accessible names, folder
aria-expanded and the existing read-only selection/keyboard/disclosure rules.
Long names may truncate visually; expose their full relative path on hover.
No remote icon assets, dependencies or file reads are introduced.

Acceptance checks real file icons, folder open/closed chevrons, keyboard and
bulk actions, selection retention, normal/full-page/small viewports and
light/dark contrast. Extension/fallback mappings use internal regression
controls; do not manufacture file types or history for a live demonstration.


## Manual workspace and registry publication (SH11–SH13)

The sixth Draw.io page owns icon window controls, nested search results and the
manual editing/publication states. SH11 supersedes SH09's textual window toggle
and SH10's generic Markdown logo with the exact VS Code Seti glyph. SH12 search
groups use folders, files and match rows with independent disclosure, counts and
the existing Codicon arrows. Search includes unsaved current text during editing;
historical comparisons remain immutable. Global disclosure includes search groups.

SH13 extends the viewer with always-on text editing at the journal head when
local host grants and the existing versioned edit policy permit it. Opening the
viewer selects that head automatically without changing the graph's pinned
revision. Skill ID and short SHA share one compact line; no generic viewer description paragraph,
Edit, Review publication or Open latest editable revision control is shown.

The existing SH06 Skill summary/overview stays visible; only the generic viewer
description paragraph is removed.

Markdown text uses one icon toggle fixed at the right of the scrollable file tabs.
Its tooltip and accessible name describe the destination: Preview Markdown or Show
source; pressed means preview is active. Pointer, Enter and Space switch views
without losing unsaved text. Preview renders the working copy. There is no separate
Source/Preview/bytes bar, including its byte count. SH13 supersedes the earlier
toolbar drawings. Other file types retain their source or binary view. Show source
also applies to read-only text. Selecting a Find result or pressing Ctrl+F while
previewing returns to source so the match can be selected.

Publish and Discard appear at the bottom right only after a file changes, with an
additional retained state when this session saved a candidate but promotion failed.
On a fresh open with only earlier unpublished commits, the footer stays hidden
until a new file edit, as requested; existing history remains inspectable.
The message is an
optional commit message (default `Update Skill files`, backend `operator`
provenance). A compact footer disclosure counts and lists the cumulative changed
files against registry current, explicitly including earlier saved changes. A path
opens that file's working-copy-to-registry diff in the main editor. Publish waits
for this exact comparison; Retry comparison recovers failure. There is no separate
review mode. Publish is one explicit action: save all changed files
as one immutable commit, then promote that exact candidate against the captured
registry current by compare-and-swap. Each stage retains its exact replay identity
when its outcome is uncertain; Check result reconciles that stage. A definitive
publication failure retains the saved candidate and supports retry or further
edits. Discard clears working edits and reloads the journal head; it never deletes
a saved commit or changes registry current. Closing with unsaved work requires
confirmation; in-flight or uncertain writes must be reconciled before closing.
Historical comparisons remain available without altering the working buffers.

Defaults deny writes. Failures use the shared descriptive presenter and retain
working edits or saved candidates. This is a trusted single-user local service,
not per-user access control or a signed audit. Binary editing and durable recovery
of unsaved buffers after browser crash are unsupported; browser unload warns while
edits remain. No model run, Git publication, source write or automatic graph-pin
update occurs.


Manual failure cards remain within the active Skill dialog's interaction boundary
while appearing at the bottom-right of the screen. Dismiss, Copy and Escape must
work with pointer and keyboard; dismissing a card preserves the viewer and its
working buffers. Window resizing and full-page mode never move a card outside the
visible screen. The implementation uses a dialog-owned top-layer stack where
supported rather than an inert body-level sibling of a modal dialog.

While a modal is open, background global notifications retain state but remain
hidden outside its focus boundary. They reappear after closing; modal error cards
remain reachable and cannot hide Publish behind an unrelated notification.

The authenticated application owns the open workspace above transient canvas
toolbars. Refresh and reconnection retain its exact selection, buffers and pending
identity; a new toolbar request cannot replace it. Leaving the authenticated
application releases in-memory state; reload/crash restoration remains unsupported.


## SH14 - File actions

The Skill explorer file actions page owns context-menu Upload files, Rename,
Delete and Copy relative path, internal drag-and-drop moves, and external file
imports. It defines target selection, inline confirmation/forms, immutable batch
publication, working-copy Discard and protected SKILL.md. Binary files are accepted
only under explicit asset/path policy; their editor remains metadata-only.
Empty folders and importing directories are unsupported. The drawing defines
collision/limit refusal, read-only/busy gating and error recovery.

Keyboard opens the context menu using Shift+F10 or the ContextMenu key; Move to
provides the drag equivalent. Focus returns to the surviving/new row or root.
The diagram enumerates root/folder/file/required-entrypoint menus, visible disabled
reasons and an in-dialog portal boundary. It also fixes the exact inert suffixes,
secret-path refusals and unchanged byte identity independent of wire encoding.

The root context/drop target covers the entire Files pane, including blank space.
New destination restrictions do not prevent unrelated actions after text edits at
existing legacy paths; whole-tree collisions and limits still apply.
