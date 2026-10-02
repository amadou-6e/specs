---
title: Langflow integration
status: draft
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration

Owns the Laomedo boundary to the embedded Langflow editor/runtime: saved
configuration selection, launch correlation, agent-stage adaptation, workflow
events and follow-up run requests. Langflow owns graph definitions and
sequencing. A single agent is configured through a simpler form but runs as a
one-agent Langflow workflow. This subsystem does not duplicate Langflow's
general component graph.

Consumers: issue integration, prompt and skill library, agent execution, run
traces and results. This is a target boundary; Langflow API feasibility and
durable workflow-state ownership remain open.

Read the [contract](contract/README.md), [design](design/README.md) and
[validation](validation.md). Entry schema: those pages plus this overview
(1 each); focused contract/design pages (0..*).

The [decision-readiness triage](design/decision-readiness.md) records which
questions can be specified now and which require a user choice, source
research or a bounded experiment. It is not accepted runtime behavior.
