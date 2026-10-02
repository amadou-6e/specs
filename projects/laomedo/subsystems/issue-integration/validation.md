---
title: Issue integration validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue integration validation

No product test was run for this new boundary. Proposed acceptance checks:

| Interface | Check before acceptance | Evidence status |
| --- | --- | --- |
| IF-01 | Selected issue reference reaches run setup; the agent fetches current GitHub content and reports a related PR without targeting it automatically | Not executed |
| IF-12 | An unreviewed draft cannot publish; a reviewed draft yields one issue reference or a visible failure | Not executed |

The [handoff graph](../../architecture/subsystem-handoffs.md) is design evidence,
not a runtime result. Pin implementation and API versions when these checks run.
