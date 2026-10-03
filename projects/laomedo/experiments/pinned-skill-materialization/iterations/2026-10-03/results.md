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
| Source Git status before/materialize/edit/cleanup | clean at all four points | clean at all four points |
| Parent-path read, unsafe ID, tampered revision | rejected | rejected |
| Runner use evidence | `offered` | `offered` |
| Native provider discovery | unverified | unverified |

LF and CRLF produced **different** source file and tree hashes, as expected
for byte-exact revisions; neither was silently normalized. The effective
copy matched each source before editing, while its post-edit hash changed
without altering the source or immutable store. A tampered stored revision
failed before an effective skill target appeared. The observed path is
`.agents/skills/exp08-sample/SKILL.md`.

These results support only deterministic materialization and cleanliness
in a disposable source tree. They do not prove Codex saw or used the skill,
Docker mount behavior, all Windows reparse-point cases, or production
session semantics. No model-backed follow-up was authorized in this attempt.
