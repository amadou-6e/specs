# Skill Revision component

Status: proposed. This is the read-only skill input to a flow. Its visual
presentation and interactions need a view-owned Draw.io specification.

## Purpose

Select and inspect an exact skill revision. The component exposes isolated
rules and few-shot examples without losing their source paths or implying
that the entire skill was used. It supplies an immutable skill reference to
an agent run. It does not edit source files.

## Input and output

| Input | Requirement |
| --- | --- |
| `skill_id` | Registry identity, not an arbitrary filesystem path |
| `revision` | Explicit revision or a `latest` alias resolved once before dispatch |
| `selection` | `full_bundle` or listed rule/example IDs |
| `read_request` | Optional file or item IDs to return for inspection |

Output is `SkillSnapshotRef` from [shared contracts](contracts.md), plus any
requested `SkillItem` records: `item_id`, kind (`rule` or `example`), relative
path, exact content, file hash, bundle revision, and provenance. A few-shot
example may include parsed input and expected output if the format declares
them; the original bytes remain accessible. The component never returns a
secret or a path outside the registered bundle.

## Bundle model

A skill is a directory rooted at `SKILL.md` with any referenced rules,
examples, scripts, and assets. Snapshot the full declared dependency closure
and record a hash for every file plus a canonical tree hash. Git commit IDs
provide human change history, while the tree hash identifies exact bytes in
committed and draft revisions. A version history exposes parent revision,
author or agent run when known, timestamp, changed paths, and diff ref.

The registry must define an item manifest or parsing rule for stable rule and
example IDs. It must reject duplicate IDs, missing referenced files, invalid
relative paths, and references escaping the bundle. Merely splitting
`SKILL.md` by headings is insufficient if rules or examples live in other
files. The exact manifest format remains open; a pilot should test it on real
skills before fixing a schema.

## Execution behavior

1. Resolve `skill_id` and requested revision and atomically freeze the bundle.
2. Validate manifest, selected IDs, dependency closure, and file hashes.
3. Emit the immutable ref and requested item content. Record whether the agent
   is offered the full bundle or a selected subset.
4. Materialize only that frozen content in the isolated runner workspace and
   capture an effective workspace hash after materialization. For
   Codex and Claude, use each runtime's native skill discovery path when the
   full selected bundle is compatible. If a subset is supplied as direct
   context instead, label the delivery mode; do not call it a native skill
   invocation.

Reading an item for inspection does not mean the agent consumed it. Monitoring
records the offered set and separately records observed reads or invocations.
If the native trace cannot prove consumption, the latter remains unknown.

## Failures and acceptance

Resolution fails closed for a missing revision, stale alias resolution,
duplicate item ID, missing dependency, hash mismatch, or unsafe path. No
agent starts with a partly loaded skill. A registry update after resolution
does not change an in-flight run.

- Selecting the same revision twice yields the same tree hash and file hashes.
- A rule or example can be read alone with its path, hash, and revision.
- A changed rule produces a new revision and a diff; past runs retain the old
  ref and content.
- A selected subset records exactly what was offered, including dependencies.
- A missing script or escaped path blocks dispatch with a specific error.
