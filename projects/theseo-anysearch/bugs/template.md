---
title: Concise description of the incorrect behavior
status: template
kind: bug
owners: [theseo-team]
last_reviewed: YYYY-MM-DD
applies_to: [theseo-anysearch]
supersedes: null
related: []
---

# [Concise description of the incorrect behavior]

<!--
Specific Instructions

- After copying this template, replace `status: template` with exactly one of
  `reported`, `confirmed`, `fix-in-progress`, `resolved`, `not-reproducible`, or
  `superseded`. Replace every other placeholder as well.

- Describe the defect from the perspective of the team reporting or fixing it.
- In "Observed behavior", state only what the system demonstrably does and identify
  the evidence or source of the observation.
- In "Expected behavior", state the behavior we require based on the applicable
  product requirement, business rule, or technical contract.
- Do not label a value or behavior as expected merely because another source contains
  it. Attribute conflicting claims to their actual source and state which behavior we
  consider correct.
- Separate verified facts, interpretations, assumptions, and open questions.
  Insufficient evidence is an open question, not a confirmed defect.
- Keep the system behavior as the subject of the bug. Test data, logs, reports, and
  other artifacts are evidence unless the artifact itself is defective.
- Give every bullet in "Observed behavior" exactly one corresponding bullet in
  "Expected behavior", in the same order. Each pair must describe the current and
  required states of the same behavior under the same conditions.

Intent-attribution examples:

- Wrong: "The classification is expected to be `order_status`, but the pipeline
  returns `other`." This hides who owns the expectation.
- Correct: "The stored test case labels the conversation as `order_status`. Based on
  the documented classification rule, we expect `other`; the pipeline returns
  `other`. The stored test label is incorrect."
- Wrong: "The field should remain nullable." This does not identify whether the
  statement is our requirement or an external claim.
- Correct: "The reporting contract requires the field to remain nullable; therefore,
  we expect schema migrations to preserve nullability."
- Wrong: "They expect the deployment to run at 08:00." The subject is ambiguous.
- Correct: "The operations team requires the deployment to finish before the 08:00
  processing window; we expect the deployment workflow to enforce that deadline."

One-to-one behavior example:

- Observed 1: "The API returns HTTP 200 when validation fails."
- Expected 1: "The API returns HTTP 400 when the same validation fails."
- Observed 2: "The rejected payload is persisted."
- Expected 2: "The same rejected payload is not persisted."

Classification-attribution example:

Bad:

Four conversations expected `order_status` or `order_cancellation` but were classified
as `other`.

What went wrong:

- The sentence omits who or what assigned the expected classifications. An LLM can
  therefore interpret `order_status` and `order_cancellation` as the ticket author's
  required behavior rather than values stored in a fixture.
- It combines an external source's labels with the observed pipeline result without
  distinguishing their authority or correctness.
- It does not state our intended behavior, so the reader cannot determine whether the
  pipeline output or the stored labels should change.

Good:

**Observed behavior:**

- Four conversations are classified as `other`, while the stored fixture labels them
  as `order_status` or `order_cancellation`.

**Expected behavior:**

- The four conversations should be classified as `other` because the available
  conversation evidence does not support `order_status` or `order_cancellation`. The
  stored fixture labels should be corrected.
-->

## To Do

[List only missing work needed to complete this durable record. Keep implementation
status and the fixing checklist in the linked GitHub issue. Write `None` when the
record itself is complete.]

## Description

[Briefly explain the defect, where it occurs, the affected conditions, and why it
matters. Include a verified root cause and useful workaround when known; label
hypotheses and unverified workarounds explicitly. Distinguish demonstrated impact
from plausible risk.]

## Observed behavior

- [Observed behavior 1 under its stated conditions; link or identify the evidence.]
- [Observed behavior 2 under its stated conditions; link or identify the evidence.]
- [Observed behavior 3 under its stated conditions; link or identify the evidence.]

## Expected behavior

- [Expected behavior 1 under the same conditions; link its governing authority.]
- [Expected behavior 2 under the same conditions; link its governing authority.]
- [Expected behavior 3 under the same conditions; link its governing authority.]

## Linked work items

- [Required GitHub issue: title]
- [Fixing pull request, when one exists]
- [Regression evidence, when it exists]
- [Owning contract or other authority; if absent, add writing it to To Do]

## Checklist

- [ ] Every observation is supported by identified evidence.
- [ ] Every expectation names its authority and pairs with exactly one observation.
- [ ] The reproduction or regression check is named, including environments tested.
- [ ] Existing affected data or behavior has been validated where applicable.
- [ ] Root cause, workaround, remaining caveats, and resolution evidence are recorded
      or explicitly identified as unknown or not applicable.
- [ ] Durable lessons are linked from the owning subsystem or implementation guide,
      or explicitly identified as not applicable.
