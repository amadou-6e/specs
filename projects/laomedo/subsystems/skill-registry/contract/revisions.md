---
title: Skill Revision component
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill Revision component

Status: proposed. This is the read-only skill input to a flow. Its visual
presentation and interactions need a view-owned Draw.io specification.

Implementation status, 2026-10-01: the
[local pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md) implements exact
whole-bundle registry lookup, file-hash validation, and native workspace
materialization. The saved flow embeds a frozen skill ref. A separate Skill
Revision Langflow node and isolated rule/example selection remain target work.

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

Output is `SkillSnapshotRef` from [shared contracts](../../../architecture/shared-contracts.md), plus any
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

## Runner-local Git exclusion (#79 proposal)

The local file-snapshot runner keeps full pinned skills at
`.agents/skills/<skill_id>/`. Its source is a directory beneath a host Git
repository; host `.git` metadata is deliberately not copied. An exclusion file
alone cannot make that private workspace a valid checkout.

Before materializing skills, create a private Git baseline from the copied
source bytes, with no remote, host Git configuration, credential, template or
hook inheritance. Use the existing credential-free bounded Git command helper.
A missing Git executable or failed baseline setup refuses preparation before any
agent dispatch. This baseline commit is a local implementation artifact, not the
source repository's commit identity or permission to publish.

Install only exact anchored directory rules in the run's `.git/info/exclude`,
one `/.agents/skills/<skill_id>/` per pinned skill. Never edit source, global or
personal Git configuration. Preserve an existing private exclusion file rather
than replacing unrelated entries. Record its hash with the run. Effective and
post-run workspace hashes include the new private Git metadata separately from
the unchanged source hash. Preserve CRLF skill bytes without text normalization.

Before dispatch and before accepting completed output, verify pinned skill tree
hashes, the exact selected skill-directory set, safe parent paths and the exclusion
file hash. Changed/escaped skill bytes or changed exclusions fail validation;
ordinary edits outside runner-owned paths remain visible to Git. Exclusion is a
cleanliness mechanism, not a sandbox: forced staging/cleaning and malicious Git
configuration are not prevented by ignore rules. Pinned-byte checks must not
claim those operations cannot occur.

Cleanup may clear Git's Windows read-only file bit only within a verified owned
run tree. Refuse cleanup outside that state boundary and report failed cleanup
explicitly. Tests must cover fresh checkouts, CRLF bytes, unrelated changes,
ordinary staging, skill/exclusion edits and negative cleanup controls. Shared
OpenCode preparation uses the same exclusions and must retain its existing
provider-specific pinned-skill checks. No live provider or credential claim
follows from these credential-free controls. Legacy records without this baseline
are not silently upgraded; Git-present records without matching exclusion
metadata fail closed. This is draft behavior pending independent review.
