# Decisions

Expandable document collection for durable Laomedo product choices and their
discussion trail. These records explain *why* the architecture and subsystem
contracts took their current shape; they do not replace the editable Draw.io
graphs or assert that proposed behavior has been implemented.

| Child | Cardinality | Purpose |
| --- | --- | --- |
| `README.md` | 1 | Category authority, lifecycle and index |
| `template.md` | 1 | Copyable, populated example; never an accepted choice |
| `000N-<slug>.md` | 0..* | One numbered decision record per bounded topic |

Copy `template.md`, assign the next number, replace every example fact and
change `status: template` to the real lifecycle state. A record can reconstruct
a discussion when no verbatim transcript is stored, but must name its sources,
date range and limits. Distinguish a user-confirmed choice from an inference,
proposal, unverified third-party capability or still-open question. Use `draft`
until review confirms the record; acceptance is not implied by saving it.

## Entries

- [0001 — Issue-to-agent journey](0001-issue-to-agent-journey.md): choices and
  changes behind the user-traversal graph.
- [0002 — Subsystem handoffs](0002-subsystem-handoffs.md): D01–D25 and the
  interview trail behind the subsystem graph.

The [journey graph](../architecture/user-traversal.md) and
[handoff graph](../architecture/subsystem-handoffs.md) remain the editable visual
authorities. Subsystem contract pages own proposed interface behavior; this
category owns the decision history, alternatives and unresolved choices.
