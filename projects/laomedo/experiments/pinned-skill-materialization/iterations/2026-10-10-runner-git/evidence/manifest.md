---
title: Runner Git regression pins
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Pins and access

- Develop base: `44f628e775bad90d9cd25c6a0a0e50a0072c6de7`.
- Initial implementation: `f5b4a1085d55a5fcfab5c059c5001eda4d3220db`.
- Production behavior: laomedo/workspace_skills.py, local_runner.py and
  opencode_runner.py. Controls: tests/test_workspace_skill_git.py.
- Final source/test pin: `177242e656bd3dd546b18ffebed76ed054a4ce89`; final suite result is recorded in results.md.
- Producer: implementation author, Windows host regression suite; independent
  reviewer has not accepted the change yet.
- Fixtures and expected assertions are committed code; local logs contain
  generated temporary paths and stay ignored. No secrets or raw agent transcripts
  exist in this test evidence. No persistent test workspace is published.

Earlier EXP-08 evidence remains unchanged. Structural validation does not prove
runtime behavior, and host Git cleanliness is not a sandbox guarantee.
