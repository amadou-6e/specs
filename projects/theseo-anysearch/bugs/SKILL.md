---
name: theseo-bug-record
description: Create or revise a durable Theseo bug record from verified evidence, the violated contract, and linked GitHub work; use for defects with lasting diagnostic or design value, not ordinary issue tracking.
---

# Maintain a Theseo bug record

Use [template.md](template.md) for the document shape and the project
[SPECS.md](../SPECS.md) for category ownership. A bug record preserves verified
defect knowledge that will remain useful after the fixing issue closes. GitHub remains
authoritative for assignment, priority, implementation progress, and closure.

## Decide whether a record belongs here

Create a specification record only when the defect has durable value: it is difficult
to diagnose, likely to recur, platform- or environment-specific, capable of silently
invalidating results, associated with an important workaround, or exposes a meaningful
contract or design lesson. Ordinary defects need only a GitHub issue.

Before writing, identify:

- the observable system behavior and the conditions that produce it;
- the evidence that demonstrates that behavior;
- the authoritative requirement or subsystem contract it violates; and
- the GitHub issue that owns the work.

Give each record the standard metadata block with `kind: bug`. The source template
uses `status: template`; a copied record must replace it. Use only the
bug-specific lifecycle values `reported`, `confirmed`, `fix-in-progress`, `resolved`,
`not-reproducible`, or `superseded`; do not use the generic lifecycle vocabulary.

Do not convert suspicion, an unexpected metric, a failing assertion, or a conflicting
fixture label into a confirmed defect without establishing which behavior is actually
required. Record insufficient evidence as an open question in the linked issue rather
than manufacturing certainty in the bug record.

## Frame the record

- In **To Do**, list only work required to make the durable record complete, such as
  collecting missing evidence or adding a regression reference. Do not duplicate the
  fixing issue's implementation checklist or live project status.
- In **Description**, briefly state what the defect is, where it occurs, the affected
  conditions, and why it matters. Include a verified root cause and useful workaround
  when known; label hypotheses and unverified workarounds explicitly.
- Use the worked intent-attribution examples in [template.md](template.md) when claims
  from fixtures, reports, users, or other sources conflict with the required behavior.

## Write evidence-backed behavior pairs

- Keep the system behavior as the subject. Logs, screenshots, test fixtures, reports,
  and user statements are evidence or claims unless one of those artifacts is itself
  defective.
- In **Observed behavior**, state only what is demonstrably happening. Identify the
  source of each consequential observation and the conditions under which it occurs.
- In **Expected behavior**, state the required behavior and attribute it to its
  authority: a subsystem contract, accepted decision, product requirement, business
  rule, or explicitly established invariant. Another source containing a different
  value does not by itself make that value correct.
- Give every observed-behavior bullet exactly one expected-behavior bullet in the
  same order. Each pair must concern the same behavior under the same conditions.
  Split compound claims until this correspondence is unambiguous.
- Separate verified facts from interpretations, assumptions, and unresolved
  questions. Do not hide disagreement between sources by presenting one source's
  claim as a neutral expectation.
- Explain impact only to the extent supported by evidence. Distinguish a reproduced
  impact from a plausible risk.

## Link authority and active work

- Link at least one GitHub issue under **Linked work items**. Link the fixing pull
  request and regression evidence when they exist, without copying their live status.
- Link the violated subsystem contract near the expected behavior it supports. If the
  authoritative behavior has not yet been written into a subsystem contract, link the
  actual authority, add the missing contract to **To Do**, and do not present the bug
  record itself as the contract. This is the documented fallback to the container's
  normal contract-link requirement.
- Link implementation, experiment, or research documents only as supporting evidence.
  A bug record does not redefine their conclusions or own their content.
- When a fix changes the intended contract rather than restoring it, require the
  owning subsystem or decision record to change; do not silently rewrite expected
  behavior to match the implementation.

## Close the durable record

- Complete checklist items only from concrete verification. Name the reproduction or
  regression check, the affected environments actually exercised, and any remaining
  caveats.
- Use `resolved` only when named verification shows that the defect can no longer be
  reproduced under the affected conditions. Use `not-reproducible` when the available
  checks cannot establish the observation, and state their limits. A lifecycle label
  never substitutes for the linked evidence.
- Preserve useful root-cause, workaround, and resolution knowledge through concise
  links or additions when available, but keep current workflow state in GitHub.
- Check whether the defect revealed a durable diagnostic, platform, compatibility, or
  operational lesson. Route that lesson into the owning subsystem guide or
  `implementation/` guidance and link the resulting update from the record.
- If later evidence disproves the defect, correct the record and link the evidence;
  do not preserve a false claim merely because a ticket once existed.
- Check that observed and expected bullets remain one-to-one, links resolve, and the
  record is understandable without reconstructing the entire issue discussion.
- Run the specs repository validator and report the evidence reviewed, checks actually
  run, and unresolved uncertainty.
