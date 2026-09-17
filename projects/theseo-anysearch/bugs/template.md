# [Concise description of the incorrect behavior]

<!--
Specific Instructions

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

## Description

[Briefly explain the defect, where it occurs, and why it matters.]

## Observed behavior

- [Describe what currently happens and cite its evidence or source.]
- [Describe the conditions under which it happens.]
- [Describe the demonstrable user-facing or data impact.]

## Expected behavior

- [Describe the required behavior under the same conditions as observed behavior 1.]
- [Describe the required behavior under the same conditions as observed behavior 2.]
- [Describe the required user-facing or data state corresponding to observed behavior 3.]

## Linked work items

- [TICKET-ID: Linked work item title]

## Checklist

- [ ] [The defect can no longer be reproduced.]
- [ ] [Existing affected data or behavior has been validated.]
- [ ] [Regression checks pass in the required environments.]
