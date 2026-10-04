---
title: Pinned skill materialization results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Check | LF | CRLF |
| --- | --- | --- |
| Source versus effective skill tree hash | equal | equal |
| Post-edit skill tree hash | changed | changed |
| Source and stored revision after effective edit | unchanged | unchanged |
| Unprotected agent checkout | Skill untracked; `git add -A` stages it; ordinary `git clean -nd` would remove it | Same |
| Protected agent checkout (`.git/info/exclude`) | Git status clean; `git add -A` stages nothing; ordinary `git clean -nd` omits skill | Same |
| Force clean (`git clean -ndx`) | Would remove skill despite exclude rule | Same |
| Tracked fixture checkout with `core.autocrlf=true` | Git converts LF to CRLF | Same |
| Source Git status and post-cleanup protected checkout | clean | clean |
| Parent-path read, unsafe ID, tampered revision | rejected | rejected |
| Runner use evidence | `offered` | `offered` |
| Native provider discovery | unverified | unverified |

LF and CRLF produced **different** source file and tree hashes, as expected
for byte-exact revisions; neither was silently normalized. The effective
copy matched each source before editing, while its post-edit hash changed
without altering the source or immutable store. A tampered stored revision
failed before an effective skill target appeared. The observed path is
`.agents/skills/exp08-sample/SKILL.md`.

These results expose checkout pollution without protection and support
deterministic materialization plus cleanliness **only when the disposable
agent clone has the tested local exclude rule**. They do not show that the
production runner installs that rule, or protects against `git clean -x`.
They do not prove Codex saw or used the skill, Docker mount behavior, all
Windows reparse-point cases, or production session semantics. No model-backed
follow-up was authorized in this attempt.
