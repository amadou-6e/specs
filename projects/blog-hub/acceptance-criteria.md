# Acceptance Criteria

Source: extracted and expanded from `.planning/core_feature_functioning_and_ui_samples.md` Section 8.

These are end-to-end product acceptance criteria, distinct from per-view UI test specs.
A release is not shippable until all items below are verified on a real environment.

---

## AC-1: Generation

User can generate a draft from a prompt and selected skills in under 60 seconds on a warm provider connection.

Verified by:
- Start timer at "Generate" click
- Stop timer when editor content is populated and generation overlay is dismissed
- Measure across 5 representative prompts of 50–200 characters

---

## AC-2: Agent patch flow

User can add a comment, request an AI fix, and accept the patch without losing any manual edits made before or after the comment was created.

Verified by:
- User makes 3 manual edits
- User adds a comment on a different section
- User requests AI fix
- User accepts patch
- All 3 manual edits and the patch content are present in the saved article

---

## AC-3: Inspection gate

Rich text conversion report shows pass/warn/fail per destination with at least these checks: code blocks, images, sections, tail.

Verified by:
- Push a test article with 3 code blocks, 2 images, 4 headings, and a conclusion
- Run inspection on Medium and Hashnode
- Report shows correct counts for each check
- A deliberately broken draft (tail removed) triggers a fail result

---

## AC-4: Destination state visibility

Destination tab shows real-time or near-real-time state for each connected platform after any state-changing action (push, inspect, publish).

Verified by:
- Push draft to Medium
- Within 10 seconds: overview card and editor destinations panel reflect the new state
- No manual refresh required

---

## AC-5: Multi-platform overview

Articles overview shows all articles with per-destination status visible without opening any individual article.

Verified by:
- 10+ articles with mixed states across 3 platforms
- All status pills visible and correct on the overview without clicking
- Filtering by platform and status returns correct subsets

---

## AC-6: Scheduling

User can schedule a publish for a future date/time on at least one platform and the publish executes within 2 minutes of the scheduled time.

Verified by:
- Schedule a publish for 3 minutes in the future
- Verify job runs and platform shows published state
- Verify published URL is accessible

---

## AC-7: Error recoverability

A failed push or publish on one platform does not block or corrupt the state of other platforms in the same article.

Verified by:
- Simulate a Medium auth failure during a 3-platform push
- Verify Hashnode and Dev.to drafts are created correctly
- Verify Medium shows sync_error with the correct reason
- Verify retry on Medium succeeds independently

---

## AC-8: No data loss on edit conflict

If two sessions edit the same article simultaneously, the conflict is surfaced to the user with explicit keep/discard options. Neither version is silently overwritten.

Verified by:
- Open article in two browser sessions
- Edit and save in session A
- Edit and save in session B
- Verify session B sees a conflict banner with both options

---

## MVP Scope (ordered)

Ship in this order. Each item is a gate for the next.

1. Articles overview + create wizard + editor
2. Comments + agent diff patch flow
3. Inspection gate (per-platform checks + artifacts)
4. Destination states and draft links
5. Scheduling and publish
6. Settings: platform connect + provider config
