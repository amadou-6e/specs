---
title: Runner Git regression results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded regression results

The eleven focused controls pass: two fresh clean checkouts with exact CRLF
skill bytes/ref/hash, unrelated changes visible, ordinary git add -A omitting the
skill, pre-dispatch skill/exclusion tamper refusal, fake-agent skill/exclusion
edits refusing completed snapshots, external Git directory refusal, linked skill
parent/Git-root refusal, missing Git refusal, read-only owned cleanup and explicit
cleanup-failure reporting. The initial full suite passed 302 tests, six skipped;
the final committed-source suite at `177242e656bd3dd546b18ffebed76ed054a4ce89` passed 303 tests, six skipped. Installed-wheel CI must pass before merge. Independent Claude review is also required and is currently pending.

No source/global exclude file was installed or changed, and source status stayed
clean through materialization and teardown. Only selected anchored skill rules
were added to private run metadata. Failed cleanup retained private files and
returned run_preparation_cleanup_unverified instead of claiming success.

This is credential-free host regression evidence. Fake-agent edits prove result
validation rejects changed bytes; they do not prove an OS write denial or live
provider behavior. Ignore rules do not prevent force-add or git clean -x. The new
baseline is not the source repository's history, native git/gh publication or a
run grant. Docker permissions and credentials are unchanged. No model turn,
GitHub acceptance write, issue edit/closure or deployment activation occurred.
