---
name: research
description: Coordinate a two-agent research-to-writing workflow for specifications or other evidence-backed documents, with a separate researcher, writer, and inspectable claim handoff. Use when a task calls for researching a topic and writing the result, especially when the roles must be independent.
---

# Research and write with separate agents

Use two distinct agents for the substantive work: a **researcher** establishes
what the evidence supports; a **writer** turns that handoff into the requested
document. Run them sequentially. The writer must not inherit the researcher's
unrecorded context or treat a chat summary as evidence.

Follow the target repository's issue, branch, review, and validation rules. Read
the target document's governing category or project skill, if one exists. This
skill coordinates roles; it does not replace a research-topic schema, subsystem
contract, source-citation rule, or permission boundary.

For an AnySearch research-topic document, also follow its
[research-specification skill](../../../projects/theseo-anysearch/research/SKILL.md).
That skill owns the topic's source/finding files, reciprocal indexes, and
non-normative research status. The quality checks below apply more broadly,
including implementation investigations that do not belong in a research topic.

## Scope the assignment

The coordinating agent gives both workers the same bounded question, target
document and authority level, intended audience, governing conventions, and
stopping condition. Name what is out of scope. Pin repository revisions and
record access dates for changing external sources. Keep research work separate
from drafting so the writer can challenge gaps rather than inherit conclusions.

## Researcher: produce an evidence handoff

Assign one agent to inspect the relevant primary sources, code, tests, data, and
existing specifications. Its deliverable is a durable handoff in the task's
agreed workspace, or a complete structured handoff to the coordinator if no
artifact location is authorized. The handoff contains:

- question and search/inspection boundary, including what was not inspected;
- reproducible discovery method: when and where the agent searched, inclusion
  and exclusion criteria, access constraints, and likely selection bias;
- each material source's location, owner, exact version/revision or access date,
  inspected portion, evidence class, authority for the specific claim, and
  limitations; prefer primary sources for technical claims;
- atomic findings linked to those source records, with direct evidence,
  counterevidence, applicability limits, confidence, and a classification such
  as **directly verified**, **externally reported**, **inferred**, or
  **unverified**; distinguish classification from confidence;
- commands/tests actually run and their results, distinguished from tests merely
  read or proposed;
- contradictions, open questions, and recommendations for additional checks;
- the owning document or contract for each behavioral claim, if the task spans
  multiple specification categories.

The researcher does not write the final specification. A source file's existence,
registration entry, passing mock test, or old specification is not proof that a
runtime path works. Say precisely what each item establishes. Do not cite a
search result or generated summary as if the underlying material was inspected,
and do not transfer an external result to this project without naming the
assumptions required.

## Handoff gate

Before assigning the writer, the coordinator checks that every proposed claim
has inspectable support, that the search boundary can be reproduced, and that
unresolved or conflicting claims are marked. Keep **not found**, **not
inspected**, **not supported**, and **not applicable** distinct; none is a
synonym for evidence of absence.
Return an inadequate handoff to the researcher with specific questions. Do not
silently fill evidence gaps by drafting plausible prose.

## Writer: draft from the handoff

Give a different agent the approved handoff, target document, and governing
conventions. The writer may inspect cited material to understand or verify the
handoff, but must not silently perform a second, undocumented investigation.
It should:

- place each claim in the document that owns it and link, rather than duplicate,
  behavior owned elsewhere;
- distinguish accepted guidance from provisional findings and unsupported ideas;
- cite exact sources/revisions near substantive claims and preserve uncertainty,
  negative evidence, disagreements, applicability assumptions, and version
  limits; make recommendations conditional on evidence strength;
- report any missing, contradictory, or unsuitable evidence back to the
  coordinator instead of inventing a resolution;
- produce a claim-to-evidence map or equivalent reviewable trace with the draft.

The writer's prose is a synthesis, not independent validation. If the researcher
supplies a new fact after drafting starts, update the handoff first, then revise
the draft against that version.

## Review and repeat

The coordinator reviews the draft against the handoff and governing structure,
checks links and actual validation output, and returns factual gaps to the
researcher or presentation/ownership problems to the writer. Repeat those two
bounded steps until the document meets its acceptance criteria or report the
remaining blocker. Do not label a draft authoritative merely because it is
well-written. Preserve the handoff and validation evidence with the task record
when the repository workflow calls for it.

If two distinct agents cannot be assigned, state that the required separation
cannot be met and ask for a different workflow; do not impersonate both roles.
