---
title: Results and artifacts
status: draft
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results and artifacts

Owns the retained run summary, artifact inventory, PR reference, optional
selected findings, unsuccessful-run report and follow-up context. It records
where outputs are and their known save/publish state; it does not assume all
files belong inside a run directory or move them automatically. The actual
artifact destination policy is still an open experiment.

Consumes run context from [Langflow integration](../langflow-integration/README.md),
outputs from [agent execution](../agent-execution/README.md) and trace links
from [run traces](../run-traces/README.md). Supplies a reviewed issue draft to
[issue integration](../issue-integration/README.md) and follow-up run context
to Langflow integration. This boundary is proposed, not implemented.

Read the [contract](contract/README.md), [design](design/README.md) and
[validation](validation.md). Entry schema: those pages plus this overview
(1 each); focused contract/design pages (0..*).
