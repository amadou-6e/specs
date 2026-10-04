---
title: Pinned skill materialization protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

The [EXP-08 issue](https://github.com/amadou-6e/laomedo/issues/38)
predefined the LF/CRLF, edit, cleanup, path and discovery questions. This
detailed fixture was written **after** execution, not frozen beforehand.

In a disposable Git repository, create a clean source directory. For separate
LF and CRLF `SKILL.md` byte fixtures, import an immutable whole-skill revision.
Clone that repository twice as actual agent checkouts with `core.autocrlf=true`.
First materialize into an unprotected clone and inspect `git status`, `git add
-A` and `git clean -nd`: this is the negative control for checkout pollution.
Then materialize into a second clone protected by a local Git exclude rule,
and repeat those checks; `git clean -ndx` remains an explicit force-clean
hazard. Compare source/effective bytes and hashes, and demonstrate Git's
LF-to-CRLF checkout conversion on a tracked fixture. Edit only the effective
skill, then verify canonical source and stored revision hashes are unchanged.
Reject parent-path reads, unsafe IDs and a tampered stored revision before
materialization. Remove the effective copy and inspect Git status again.

Pass the **synthetic** check only if all byte comparisons, rejection checks,
the unprotected negative control, and protected-clone clean-status checks hold.
Do not infer production runner protection or native discovery from the fixture:
the runner's `offered` field is not a read/use event. Any model-backed
discovery needs a separately authorized turn cap.
