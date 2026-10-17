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
Other Agent inputs, mutating Skill dependencies, ambiguous returns, indirect
cycles and multiple feedback controllers refuse before dispatch.

A proposal contains exactly `action: modify`, a nonempty `message`, and `files`:
a list of `{path, content}`. Content is complete UTF-8 text or null for deletion.
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
No Files/History mode buttons. A draggable, keyboard-operable vertical separator
controls navigation width within bounds that preserve usable content space.
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
