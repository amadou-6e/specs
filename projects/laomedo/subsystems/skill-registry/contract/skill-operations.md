---
title: Skill operations and commit history
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-16
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill operations and commit history

Selected work: [implementation #176](https://github.com/amadou-6e/laomedo/issues/176),
[specs #386](https://github.com/amadou-6e/specs/issues/386). User selected registry
history first, Git publishing later. Graph and implementation review pending.
This extends the [reference node](langflow-node.md) and [draft lifecycle](drafts.md).

## Operations

The existing Skill node accepts an ordinary Operation input or direct feedback
from its Task-consuming original Codex Agent: Skill Task → Agent Task, Agent
Answer → same Skill Operation. Independent read-only Skill outputs may also connect to Agent Skill References;
the isolated body includes those dependencies (at most sixteen Skill nodes).
Those nodes have no incoming edges, no Operation and an empty Edit Request.
The current bounded executor resolves each dependency in the outer graph and
again in the isolated body; linked sources may therefore be read twice. Both
reads must resolve the pinned immutable revision. A run started from one of
these Skills is normalized to the controller; playing only that Skill remains
read-only and must not invoke the Agent.
Other Agent inputs, mutating Skill dependencies, ambiguous returns, indirect
cycles and multiple feedback controllers refuse before dispatch.

A proposal contains exactly `action: modify`, a nonempty `message`, and `files`:
a list of file edits. Existing `{path, content}` carries complete UTF-8 text or
null for deletion. Additive `{path, content, encoding: base64}` carries canonical
base64 binary bytes; invalid encodings and more than 512 KiB decoded content
refuse. `{path, source_path}` copies exact bytes from a path in the same immutable
base revision; it cannot reference a host path or another Skill/revision. These
forms are mutually exclusive; omitted encoding retains the existing wire shape.
Source copies resolve before the batch applies any deletions. Binary changes
require explicit asset permission and an admitted asset suffix as well as the
existing exact-path, size and addition/deletion policy. Text/SKILL requirements
and protection against execution remain unchanged.
Several replacements/additions/deletions form one atomic revision. Reject unsafe
or duplicate/case-alias paths, missing SKILL.md, policy violations and no-change
bundles. No script or validation command executes because a proposal asks for it.

Host configuration maps skill IDs to versioned edit policies. Before dispatch
reserve a five-minute capability bound to exact skill, base commit and policy.
It stays backend-only. The Agent supplies content, never authority or provenance.
Apply rechecks policy and head. Identical replay returns the existing result while
the capability is valid; changed proposals conflict. A fresh explicit run is a new
operation. No automatic redispatch after cancellation or uncertain transport.
Record adapter-retained completed-run provenance; missing native turn IDs remain
unknown. These references are asserted by trusted Langflow component code, not
independently verified against runner records by the service. Edited graph code
can forge assertions; the viewer labels this provenance basis. Real acceptance
compares references independently with actual runner receipts. Ordinary operations identify the trusted operator backend, not a verified
human. Per-user ownership remains outside this trusted single-user service.

## Commit history and promotion

Tree SHA-256 identifies bytes. Separate commit SHA-256 covers parent commit, tree,
timestamp, message, paths, diff, editor provenance, policy, draft ID and a unique
nonce. Reverting to older bytes creates a distinct commit. An imported root and
each successful batch enter one transactional compare-and-swap history chain.

Freeze candidate bundles without moving canonical latest. Return the immutable
Skill Reference and an Operation Result with commit/diff. Old pinned flows retain
their bytes. Promotion is separately reviewed under the existing draft contract;
multi-commit candidate promotion must compare with canonical latest explicitly.
No source write, Git commit or GitHub publication occurs.
Operation Result exposes failed before apply and conservative unknown after an
apply transport failure. Never infer canonical publication from either status.
Failed/unknown operations stop Skill Reference and Task branches, so downstream
consumers cannot silently use the unchanged base. Operation Result retains the
diagnostic status. Invalid reference-only selections fail visibly at the Skill node.

Empty Base Commit is permitted only at the imported root. Later edits require
the exact commit and revision; a stale initial node remains stale after a revert.
With Source empty, Skill and Revision accept typed exact registry IDs/hashes, so
the operator can select a candidate from history. Linked-source discovery remains
restricted to its discovered choices and never writes candidates back to source.
Authenticated history returns 100 commits per page with older-page navigation.
Per-commit diff retrieval verifies commit identity and recomputes differences from
exact parent/current bundles. Selecting a commit in the viewer instead compares
its entire snapshot to the immutable current revision selected on the Skill node
when the panel opened. This is cumulative across all intervening commits, not
just the selected commit's patch. The same revision has no differences. Display
the currently selected file as a read-only visual editor comparison, with the
selected revision compared to pinned-current contents in one inline editor. Show
full file contents with additions/deletions highlighted, never a combined raw
patch or patch headers. Use one index when an unchanged line has the same old/current number. Show
both old/current indexes whenever they differ, including unchanged lines after
an insertion/deletion. Changed rows also show two explicit index cells; leave
the absent side of an addition/deletion blank. Render + and minus markers in a dedicated 24 px
column with bold 18 px high-contrast glyphs. A horizontal header rule and a
thin divider distinguish the number columns. Number gutters fit the file digit count with a 4 px
gap and a thin divider between the index columns. The selected revision hash is
abbreviated, with its full identity on hover. Added/deleted files have an empty absent side; binary
files show change metadata only. Unchanged files show their contents. Verify both
snapshots, keep comparison direction explicit, and reject stale/mismatched replies.
The file tree and parent-linked commit graph share one navigation pane, with the
commit graph below the files. Clicking a file changes the compared file while
retaining the selected commit. Include historical-only files so deletions remain
inspectable. Current source exits comparison without changing the pinned revision.
Find, Files and Commits have chevrons without per-section action menus. The single
SKILL menu offers Collapse all when Find, Files, Commits and every folder are open,
otherwise Open all; it changes disclosure without changing selected content.
Keep hide/reset-width actions and existing keyboard/focus behavior.
Find searches current text files locally, including unsaved working text while
editing, and opens a matching current source line. Searching does not save edits
or change the Skill revision. Full page/Restore window
resize the same dialog while preserving selection and search state. SH08/SH09
in the interaction model own these controls and transitions.
No Files/History mode buttons. A draggable, keyboard-operable vertical separator
controls navigation width within bounds that preserve usable content space.
A collapsible skill overview sits above the file/history workspace, anchored to
the same pinned current revision. It shows one sentence by default and can open
full revision-local documentation with bundled images/workflow diagrams; see
[overview authoring and media boundaries](../design/skill-files.md#skill-overview).
The Skill files panel follows the operations/history
page of its [editable interaction model](../design/skill-files.drawio).

SQLite and registry are private trusted host state, not a signed or tamper-proof
audit trail. No pruning is introduced. Interrupted precommit writes may leave
unreferenced frozen drafts/bundles but cannot advance history or canonical latest.
Expired capabilities refuse even after prior success; reconcile history rather
than rerunning an unknown operation. Binary editing and arbitrary graph cycles
remain unsupported. Model content quality is not guaranteed by mediation.

## Acceptance

- A real original-Agent graph edits two or more files atomically; canonical/source
  bytes remain unchanged and the exact candidate can be inspected.
- History exposes parent, timestamp, message, changed paths, policy and real Agent
  run references; each revision diff matches stored parent/current bytes.
- One invalid file refuses the entire batch. Additions and deletions obey policy.
- Replay adds no commit, stale edits conflict, and a revert has distinct history.
- Unsafe paths, model-authored authority, stale selection and cancellation before
  apply cannot silently modify canonical bytes.
- The user inspects the working graph and history before implementation merge.

Internal fixtures establish deterministic controls only. Real integration
acceptance is pending until recorded with inspected implementation revisions.


## Manual edits and registry publication

User-selected extension, 2026-11-02: Publish promotes the registry revision; Git
publishing remains deferred. SH11–SH13 in the editable interaction model own UI.
The authenticated viewer may edit text files at the exact journal head only,
under explicitly configured manual edit permission and the existing versioned
policy. A missing grant is read-only. Manual requests cannot assert agent identity,
run IDs, authority, policy or filesystem paths. Backend provenance is operator,
not a separately verified human account. All changed files and the commit message
are admitted together through the existing atomic proposal path.

A browser-generated UUID identifies one save. The service durably binds it to the
exact skill/base/commit/proposal before applying. Identical replay reconciles its
existing receipt; reuse with changed bytes conflicts. Tickets remain backend-only.
Stale heads, malformed batches, revoked policy, forbidden paths and missing
summary refuse without partially committing. Working buffers remain available
after a refusal; an uncertain response exposes Check result with the same request.

Publish requires an additional explicit host grant. One explicit action saves the
changed-file batch and then promotes its exact candidate commit against the
captured canonical current revision. Revalidate the whole cumulative
diff against that policy, stage/freeze from canonical current, then use the existing
registry CAS promotion and durable publication receipt. A concurrent canonical
change refuses; never silently rebase or retry against a new base. Identical
publication replay returns its original confirmed receipt even after later history
changes. Failed publication never implies canonical success. An interrupted
publication reconciles its retained frozen draft before a fresh attempt.

Old immutable revisions, journal history, source trees and saved graph pins remain
unchanged. No Git operation or agent request is performed. Local unsaved buffers
have no crash persistence guarantee. Acceptance exercises real browser two-file
save and promotion from one Publish action, exact replay, stale base,
policy denial/revocation, invalid batch, network failure/recovery and unsaved-close
protection; internal controls are not a substitute for these live stories.


Manual UI scope (SH14): edit existing text, upload text/binary files, rename,
move and delete through the explorer working copy. Folder changes apply to all
descendant files; empty directory identity is unsupported. Required SKILL.md
cannot be renamed, moved or deleted. No implicit overwrites, directory imports
or binary content editing are provided. Context-menu copy uses the Skill-relative
path, never an absolute host path. Limits, collisions and invalid paths refuse the
entire working operation. The service independently enforces the complete policy
and exact head at Publish; a UI change never grants authority. Text editing is available immediately when
authorised. The viewer opens the journal head without altering saved graph pins.
Skill ID and short SHA share one compact header line. Publish and Discard appear
at the bottom right only after a file changes; an optional message uses a generated
default when empty. No separate Edit, Review publication or Open latest control is
shown. A saved candidate remains pending publication after a definitive promotion
failure; retry requires another explicit Publish action. That action may use the
newly confirmed registry base; uncertain writes always reconcile their original
identity first. Discard reloads the journal head and never deletes saved commits or
changes registry current. The file editor remains the content region.
Window controls contain icons only,
with Full page and Restore window as tooltips and accessible names.

### Manual failure catalogue

These stable public categories use the shared error presenter and safe technical
details. Never forward exception bodies, file contents, tickets or credentials.

| Code | Meaning | Actual recovery control |
| --- | --- | --- |
| `skill_manual_controls_unavailable` | Read-only control/permission lookup failed; no edit requested | Retry edit controls |
| `skill_manual_comparison_unavailable` | Cumulative footer comparison failed; Publish disabled | Retry comparison |
| `skill_manual_not_authorized` | Required host grant or policy is absent/revoked | Preserve text; inspect local permission configuration |
| `skill_manual_stale` | Head or registry base changed | Keep or copy working text; Discard reloads the head after confirmation. Retry Publish explicitly only when the selected head remains current. |
| `skill_manual_invalid` | Malformed request or invalid bundle shape | Correct message/files; preserve working buffers |
| `skill_manual_request_conflict` | Same save UUID has different content | Inspect existing history before a new save |
| `skill_manual_policy_denied` | Batch violates configured editing rules/required summary | Correct working text; Publish again |
| `skill_manual_save_expired` | No retained result; unused edit capability expired | Refresh current head, then save preserved edits as a new request |
| `skill_manual_unavailable` | Write outcome is unknown | Check result with the same exact request |
| `skill_manual_nothing_to_publish` | Candidate bytes are already registry current | Discard the working state; immutable history is retained |

Publication receipts record confirmation time, not an invented original publication
time after crash recovery. A confirmed durable receipt remains a read of the same
effect; new publication never silently replaces its reviewed base.


A stale-head failure retains working text. Discard opens the unsaved-changes
confirmation; Keep editing preserves the text, while Discard changes reloads the
newer head. Copy wanted text first; no automatic merge or export is implied.
Revoked grants disable Publish while preserving buffers; Retry edit controls
refreshes restored permission. Before any Publish, a compact footer disclosure
counts all changed files against the exact registry base, including saved commits
ahead of current. It lists those paths and opens the selected file's cumulative
diff in the editor; no separate review mode or confirmation step is required.
Publish is disabled while this comparison is unavailable. A new explicit attempt
after a definitive stale-base failure uses the newly loaded cumulative comparison;
an uncertain attempt always retains its original base. The optional message
defaults to `Update Skill files`; backend provenance remains `operator`.
Native unload warning, unsaved-close, saved-candidate failure, grant restoration
and cumulative disclosure are observable browser acceptance paths.
Completed exact receipts remain readable after
write-grant revocation/policy change; only an uncompleted/new effect requires
current write authority. A blocked close during an uncertain write visibly says
to wait for confirmation or use Check result, rather than silently ignoring it.


### Explorer file failures

SH14 uses the shared catalogue and dialog-owned presenter; no file bytes, browser
exception messages, host paths or base64 appear in diagnostics.

| Code | Meaning | Recovery |
| --- | --- | --- |
| `skill_manual_file_invalid` | Unsafe/reserved name, forbidden core-file operation or unsupported directory import | Use a portable name; select files rather than directories; keep SKILL.md at root |
| `skill_manual_file_conflict` | Destination, case alias or file/folder prefix collides | Choose a different name/destination; no overwrite occurs |
| `skill_manual_file_limit` | File, bundle, count or request bound exceeded | Choose fewer/smaller files; working tree is unchanged |
| `skill_manual_file_read_failed` | Browser could not read every selected local file | Re-select accessible files; no partial import |
| `skill_manual_clipboard_unavailable` | Browser refused copying a relative path | Use the selectable Relative path field for manual copying, or allow clipboard access and repeat Copy relative path |

Acceptance covers real multi-file picker and drop imports including an existing
binary asset, pointer drag moves, rename/delete confirmations and cancellation,
copy, collisions and invalid paths, batch limits, read-only/busy gating,
Publish/Discard, exact stored bytes and immutable per-revision differences. User
inspection of the final workflow remains required before merge.

Explorer binary hashes use a bundled pinned pure-JavaScript implementation; they
do not require WebCrypto or a secure origin. The service recomputes authoritative
hashes from raw bytes. Equivalent base64 uploads and immutable source copies have
the same byte/tree identity. Source references must exist in the reserved base,
not in same-batch additions. Executable modes are never imported. The fixed inert
binary suffixes are `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.ico`, `.pdf`.
SVG remains text under explicit policy and is never rendered as an image.
New file actions refuse dot-directories and secret names `.env*`, `auth.json`,
`credentials.json`, `credentials`, `.netrc`, `token`, `tokens`, `token.json`,
`tokens.json`, `id_rsa`, `id_ed25519`, `*.pem`, `*.key`. These restrictions do not
change existing immutable bundles; save and promotion recheck policy and the
resulting bundle. Pending exact replay may retain up to the existing 4 MiB request
bound in memory. Copy is allowed without edit rights; other actions show a reason
when disabled. Shift+F10/ContextMenu opens the menu and Move to provides keyboard
parity; closing/cancelling returns focus to the target or surviving root.

The 4MiB encoded-request limit can refuse a new binary batch smaller than the
4MiB bundle bound: base64 allows roughly3MiB before envelope overhead. Text uploads
and moved paths still require script/dependency permission where applicable.
Clipboard refusal exposes a selectable Relative path field for manual copying.


### Working explorer behavior (SH15)

The open editor retains empty folders after moving/deleting their final file.
Folders with no files are marked empty and not saved. Registry revisions continue
to identify file bytes only; folder-only actions do not enable Publish. Publish
keeps local empty folders in the open workspace; closing/reopening reconstructs
folders from saved files. Discard restores saved folder structure. No placeholder
file is silently created.

Rename replaces the row filename with one blue-bordered input, preserving the
icon/indent. Enter/blur commits; Escape cancels; invalid/colliding names stay
editable with the shared descriptive error. Delete immediately stages removal.
Files-focused Ctrl+Z restores deleted files/subtrees, including unsaved text;
Ctrl+Y/Ctrl+Shift+Z reapplies. Move/rename/upload are also reversible; unrelated
editor buffers are preserved. New file actions clear redo. Confirmed save/discard
clears prior tree undo; definitive refusal/unknown save retains it and busy/pending
blocks mutations. Editor/input undo remains native.

The context menu has Upload, Rename, Delete and Copy relative path, without Move
to or confirmation cards. Pointer drag/drop uses grey target-row highlighting
only; Ctrl+X/Ctrl+V on Files provides the keyboard move alternative. Root SKILL.md
protection, grants, admission, bounds and publication controls remain unchanged.

Authenticated inspection may opt into bounded binary_base64 from verified revision
bytes; ordinary inspection/operation wire projections remain unchanged. The viewer
previews magic-identified PNG/JPEG/GIF/WebP/ICO only as inert images and otherwise
shows paged hex/ASCII bytes. Staged imports use the same preview. Decode failures
fall back to bytes. No SVG/HTML/PDF document execution or external content load.


SH16 refines presentation: binary previews occupy the available editor pane without a byte/hash row; images fit with preserved aspect ratio. A renamed row has no focus outline or border; keyboard focus uses a contrasting blue background. Discard and dirty workspace dismissal open one modal confirmation. Keep editing, popup Escape and outside dismissal preserve exact working buffers; explicit confirmation reloads saved head and retains history. Dirty-close confirmation also closes the workspace. Busy, pending and import holds remain unchanged.
