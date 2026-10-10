# Interview a project owner and record their intent

Use this procedure when a specification is drafted from conversation with the
person who owns the product intent: defining a new project, a new capability,
a release scope, or a user experience. Its output is recorded decisions and
owned specification text, not a chat transcript. It replaces the unmerged
`define-project-spec` skill (#153) and addresses its observed failures (#326):
depth-first drift, repeated questions, answers kept only in chat, and
unexplained references.

## 1. Inventory before asking

Before the first question, read what the owner has already decided:

- the project's `decisions/` records (when the project declares that category),
  including their open questions;
- the contracts, decision-readiness tables and validation pages of every
  subsystem the topic touches;
- open specification issues and PRs on the same topic.

Prefill the session from these sources. Never ask the owner to repeat a recorded
choice: cite it (for example "D09 already says `latest` by default, pinned
optional") and ask only whether it still holds when the new topic genuinely
challenges it. Distinguish user-confirmed intent, documented proposals,
implemented behavior and open questions. A merged feasibility report or a
reviewer's recommendation is not the owner's decision.

Repeat this check immediately before each question, not only at the start:
long sessions are summarized, and a choice read hours earlier may no longer be
in context. If the answer is already recorded, do not ask.

## 2. Agree the goal, then compile a question map

State in one or two sentences what this interview must produce: for example,
"the interfaces between subsystems" or "release scope for the two packages".
Name the deliverable files. Then compile a question map before asking anything:

- Group questions by area (subsystem, user scenario step, package).
- For each question record what it unblocks: the document, interface, decision
  or acceptance check that cannot be written without the answer.
- Mark questions already answered by the inventory as prefilled, with a source.
- Order areas breadth-first, starting with the choices other answers depend on.

Show the map to the owner in a compact form and let them prune, reorder, or add
areas before the first question. Their edits to the map are themselves intent.

## 3. Persist the map and answers in the owning record

Write the goal, the map and each answer to a file as they happen, not at the end.
When the project declares `decisions/`, create or update the topic's decision
record (status `draft`) and keep the map in its open-questions section; otherwise
use the location the project's `SPECS.md` assigns to unresolved decisions. For
each answer record the question, the owner's words or a faithful paraphrase,
the date, and what it unblocks. Tick the map entry.

The file is the source of truth for progress. It survives context compaction,
lets the next agent resume, and makes repeated questions detectable.

## 4. Ask one useful question at a time

Before each question, apply a relevance gate: name what it unblocks for the
agreed goal. If it unblocks nothing in this session's deliverable, park it in a
"later" list in the record instead of asking. A detail can be important and still
belong to a later session.

- **Breadth before depth.** Cover each area at its top level before refining it.
  Allow at most three consecutive follow-ups on one thread, then return to the
  map. Note deeper questions there rather than chasing them.
- **Position marker.** Prefix each question with its place in the map, for
  example `Issue integration · 2/5 · unblocks IF-01`. Drift becomes visible to
  both sides immediately.
- **One decision per question,** or a small group of tightly related choices.
  Offer the realistic options, the product consequence of each, and a
  recommendation when you have a reasoned one. Prefer a structured
  multiple-choice prompt when the interface supports it.
- **Plain language.** Define a term the first time it is used. Do not refer to
  identifiers, earlier messages or documents the owner cannot see or resolve;
  quote or explain them.
- **Clarify ambiguity before recording.** If an answer redefines the question
  (for example, what "stage" means), restate the corrected understanding and
  confirm it once. Do not silently record your own interpretation.
- While waiting for an answer, continue independent inventory and drafting, but
  leave the dependent choice open. A generic "yes" or "go ahead" settles only the
  question asked, not neighboring decisions.

## 5. Checkpoint

After about eight answers, or when an area is complete, summarize briefly:
what is now decided, what remains on the map, and anything parked. Ask whether
to continue, reorder, or stop. If the owner redirects the session ("we are getting
off course"), treat that as a correction to the map: record the redirection,
re-rank the remaining questions against the goal, and resume from the map, not
from the last answer.

## 6. Route the results to their owners

At the end of each area, reconcile answers into the documents that own them:

| Result | Owner |
| --- | --- |
| A user-confirmed product choice and its rationale | The project's decision record |
| Observable behavior, interfaces, failure semantics | The owning subsystem `contract/` |
| How a mechanism realizes a contract | The owning subsystem `design/` |
| A question needing sources or a test | `research/` or a planned experiment, kept open |
| UI geometry, states and transitions | The owning Draw.io under the repository's UI rules |
| An unanswered or parked question | The decision record's open questions |

Link from other pages rather than duplicating the rule. Mark proposals and
recommendations you added as proposals, never as the owner's choice. Do not label
a page `design` because it is a "brief"; choose the owner by what the text asserts.

## 7. Hand off

Report the decisions recorded (with file links), the documents updated, the
remaining map and the parked list, and the next question. Validate as the
repository requires. Follow the repository's issue/branch/PR workflow; drafting
on `main` or in an auxiliary checkout is not a substitute. Using this procedure
does not authorize implementing the recorded behavior, contacting third parties
or changing issue state.
