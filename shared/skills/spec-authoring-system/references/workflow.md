# Specification authoring: an end-to-end overview

This is the operational reading path for a contributor who has not used the
system before. It summarizes the current shared convention and the Laomedo
trial; it does not introduce a new schema or override repository guidance.
Project-specific requirements live in that project's `SPECS.md`, `spec.json`,
and container READMEs. The [typed-folder convention](../../../conventions/typed_folder_system/README.md)
defines the structural rules; the [validator](../../../../tools/validate_specs.py)
implements only part of them. If these sources disagree, record the discrepancy
and resolve it through review rather than inventing a rule.

## 1. Choose the owner before choosing the file

A specification records intended behavior and how it can be checked. Research
records what sources suggest; experiments record what a bounded test observed.
Neither automatically authorizes implementation.

| What you need to document | Canonical destination | What belongs elsewhere |
| --- | --- | --- |
| Shared identities, relationships, cross-subsystem invariants | architecture | A subsystem's private mechanism |
| One owned capability's behavior, interfaces and failure semantics | subsystems | Research conclusions presented as requirements |
| A test question, protocol, separate executions and outcomes | experiments | Unbounded source exploration |
| Sources, inspection method, findings and uncertainty | research | An accepted product decision |
| A user-confirmed product choice, its rationale, alternatives and open questions | decisions (when the project declares it) | The behavior it requires, which belongs to the owning contract |
| Contributor procedures and implementation conventions | implementation | The public behavior those procedures realize |
| Historical material no longer governing current behavior | Project's declared archive/deprecated category | A second active contract |

For example, Laomedo's snapshot-bound resume behavior belongs to agent execution;
the algorithm implementing restoration belongs to its design; a four-turn pilot
belongs to experiments; an interpretation of earlier feasibility reports belongs
to research. The validation page links those observations back to the guarantee.

Optional decision, bug, or UI collections are created only when the project
declares them. Where `decisions` exists, it is the first place to read before
asking an owner a product question and the place to record the answer; a
"brief" is not a separate owner. See [owner-interview](../../owner-interview/SKILL.md). UI geometry, states and transitions are owned by the relevant
Draw.io, not invented in Markdown. Compatibility folders contain pointers only.

## 2. Understand the structure and manifest

The top-level category set is closed. Creating another entry is routine;
adding or repurposing a category requires a reviewed change to `SPECS.md` and
`spec.json` together. There are three category types:

| `type` value | Expansion | Starting point |
| --- | --- | --- |
| `fixed` | Documents/partitions within its declared structure | Existing structure; no folder-copy template |
| `folder-collection` | One directly named folder per multi-file entry | Copy `template/` to a kebab-case peer |
| `document-collection` | One Markdown file per entry | Copy `template.md`; numbered entries use `0001-name.md` |

A manifest has required `name`, `slug`, `source_repository`, and project
`status` (`active`, `paused`, or `archived`). `slug` matches the project directory.
`categories` opts into typed-category checks. This small example is valid schema,
not a replacement for the full Laomedo manifest:

```json
{
  "name": "Laomedo",
  "slug": "laomedo",
  "source_repository": "https://github.com/amadou-6e/laomedo",
  "status": "active",
  "categories": {
    "architecture": {"type": "fixed"},
    "subsystems": {
      "type": "folder-collection",
      "entry_files": ["README.md", "contract/README.md", "design/README.md", "validation.md"]
    }
  }
}
```

For folder collections, `entry_files` lists required paths per entry (default:
`README.md`); it does not express the entire nested schema. Document collections
default to numbered names; `numbered: false` permits plain kebab-case filenames.
Optional `statuses` declares a nonempty category-specific vocabulary. Without it,
the generic entry statuses below apply. Do not add unsupported fields expecting
the validator to enforce them.

Every organizing container has a README defining purpose, permitted children,
authority and cardinalities: `1` required once, `0..1` optional once, `0..*`
repeatable. These human-readable contracts supplement the manifest. A folder
entry's README is both its overview and the entry point to its owned documents.

## 3. Fill metadata and keep different kinds of status separate

Entry pages begin with frontmatter. This is a real-entry shape with illustrative
values, not an assertion that the example has been implemented:

```yaml
---
title: Snapshot-bound resume
status: draft
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---
```

| Field | Meaning / author action |
| --- | --- |
| `title` | Human-readable identity of this document |
| `status` | Document lifecycle, not implementation or experiment success |
| `kind` | Document role, e.g. subsystem, experiment-protocol, research-source; use the owning template's role |
| `owners` | Accountable people or accurate team roles, as a list |
| `last_reviewed` | Actual content-review date; not the date a referenced test ran |
| `applies_to` | Projects/systems to which the document applies, as a list |
| `supersedes` | Replaced entry identity when supported, otherwise `null` |
| `related` | Related declared entry identities, otherwise `[]`; ordinary document links go in prose |

The validator requires the first six fields to exist. The convention and Laomedo
templates also carry `supersedes` and `related`. Presence checks are not a full
semantic/type/date validation. Bare container indexes need not have entry metadata;
required entry READMEs in folder collections do.

The generic typed-entry vocabulary is `draft` (proposal), `active` (currently
governing document), `complete` (recording finished), `deprecated` (retained but
no longer recommended), and `superseded` (replaced; name the replacement).
`template` is reserved for examples and must be replaced in every copied entry
page. These descriptions do not establish an automatic transition or approval.
Review governs changes; do not erase historical evidence when a document changes.

Keep four axes explicit: document lifecycle; implementation maturity; test outcome
(pass/fail/inconclusive/not run); GitHub issue/PR state. A complete pilot can report
failure. An active contract can have unimplemented guarantees. A merged PR does
not prove a production capability or authorize a model-backed experiment.

The older [spec lifecycle guide](../../../conventions/spec_lifecycle.md) uses
`discovery/review/accepted/implemented/archived` for specification approval stages.
These are not default typed-entry status values. Describe approval/maturity in
prose, or adopt a reviewed category-specific `statuses` vocabulary before using
them as frontmatter. Do not silently substitute one vocabulary for the other.

## 4. Copy the right template and replace its contents

Copy directly to a peer folder/file; do not create `new-name/template/`.
Replace identity, example facts, dates, status and links throughout the copy.
Index it in the owning README. Leave unknown facts explicitly unknown; copying
an illustrative finding does not turn it into observed evidence.

Laomedo's current folder templates have these internal contracts:

```text
subsystems/<capability>/
  README.md                 # 1: users, boundary, scope, dependencies, maturity
  contract/README.md        # 1: observable behavior and failure guarantees
  contract/<detail>.md      # 0..*: substantive interface/configuration details
  design/README.md          # 1: mechanisms realizing the contract
  design/<detail>.md        # 0..*: substantive mechanism details
  validation.md             # 1: guarantee -> check -> dated evidence -> gap

experiments/<question>/
  README.md                 # 1: question, scope, entry links, current disposition
  protocol.md               # 1: controls, metrics, gates, budget, allowed changes
  sources.md                # 1: inputs, governing specs and implementation pins
  iterations/README.md      # 1: index of distinct attempts
  iterations/<attempt>/     # 0..*: one independently identified execution
    README.md               # 1: identity, status and protocol link
    execution.md            # 1: commands, versions, actual actions/deviations/usage
    results.md              # 1: outcomes against gates, limitations, disposition
    evidence/manifest.md    # 1: producer, hash/revision, location, access/retention
  replication.md            # 0..1: only when an actual replication is recorded

research/<question>/
  README.md                 # 1: question, scope and synthesis with uncertainty
  method.md                 # 1: source selection, inspection and limitations
  sources/README.md         # 1: source index
  sources/<source>.md       # 0..*: provenance, revision, access, reported claims
  findings/README.md        # 1: finding index
  findings/<finding>.md     # 0..*: atomic claim, source links, confidence/limits
```

These are the Laomedo trial's choices, not mandatory filenames for every project.
Use its live [subsystem](../../../../projects/laomedo/subsystems/template/README.md),
[experiment](../../../../projects/laomedo/experiments/template/README.md) and
[research](../../../../projects/laomedo/research/template/README.md) examples for
copying. A planned attempt may say not run; remove its illustrative initial attempt
if no attempt is intended. Never fill a results table with fabricated success.

## 5. Connect intent to evidence and review

Work proceeds as: tracking issue -> typed issue branch -> owned contract/research
or protocol -> validation/evidence -> specification PR -> review -> merge.
When the intent itself is still being gathered from the owner, interview them
with [owner-interview](../../owner-interview/SKILL.md) on that issue branch and record
answers in the owning decision record as they arrive, before drafting contracts.
Only execute experiments within their separate authorization and budget.
Freeze prospective protocols and source identities before execution. Label any
post-result reconstruction retrospective; changed protocols need recorded
deviations and fresh attempt identities rather than overwritten history.

Contracts state what must happen; designs explain how; validation states what
was actually checked. Link evidence with exact revisions/hashes and distinguish
direct observation, reported claims, inference and recommendations. Preserve
negative findings and access limitations. Private transcripts, credentials and
sessions do not belong in the specs repository.

For each implementation PR, declare a spec update, exact existing coverage, or
a justified no-impact statement. Behavior, interfaces, defaults, persistence,
identity, permissions and failure semantics need authoritative coverage. In the
Laomedo policy, affected specs merge first; implementation pins that merged specs
SHA. Review can be stacked, but branch content is not yet a merged contract.
Writing this policy does not activate CI or branch protection.

For migrations, map old paths to canonical owners, repair local links, audit
published consumers, and retain short pointers where old links are relied upon.
Pointers preserve document access, not automatic HTTP or section-fragment redirects.

## 6. Know what validation proves

Run from the specs repository root:

```text
python tools/validate_specs.py
git diff --check
```

The validator checks manifest basics, declared category shapes/names, required
entry files, frontmatter presence/status, reference resolution and local file
links. It recursively inspects fixed-category Markdown leaves, excluding container
READMEs and SKILL.md; folder collections chiefly validate declared entry files.
It does not fully enforce nested attempt metadata, README cardinalities, closed
taxonomy, anchors, source truth, lifecycle semantics, dates or merge ordering.
Manually review those, walk a copied template, and check each guarantee's evidence
and gaps. Passing validation is not acceptance of product behavior.

The handoff names changed owners, exact source pins, checks/results, unresolved
claims, migration compatibility, and whether enforcement is merely authored,
locally tested, or active. Commit and push the specs issue branch and open its PR;
do not leave the result only in an ignored implementation checkout.
