---
title: Prompt and skill library validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Prompt and skill library validation

No product test was run for this proposed catalog boundary. Existing skill
registry evidence does not validate prompt storage or GitHub publication.

| Interface | Check before acceptance | Evidence status |
| --- | --- | --- |
| IF-02 | Resolve `latest` and a pin to exact refs; prove a run keeps the original refs after a later library edit | Not executed |
| IF-03/IF-14 | Resolve a skill and submit an edit as a new draft/revision without mutating bytes referenced by an active run | Not executed for library path |
| Publication | Verify user/agent GitHub PR default and explicit direct-edit mode against configured permissions | Not executed |

Record actual backend and registry revisions with later evidence.
