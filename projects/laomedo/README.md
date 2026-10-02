# Laomedo specifications

Laomedo is a proposed environment for composing versioned skills and agent workflows.
Current evidence supports a bounded single-user Langflow-to-Codex pilot tested 2026-10-01.
This repository records target behavior and observed limitations separately.

## Reading paths

- Authors: [structure and workflow](SPECS.md), then a category template.
- Implementers: [architecture](architecture/README.md), [shared records](architecture/shared-contracts.md), then [owned subsystems](subsystems/README.md).
- Capability reviewers: [pilot](experiments/local-skill-agent-pilot/README.md), original results and subsystem validation.
- Investigators: [feasibility synthesis](research/runner-feasibility/README.md), sources and atomic findings.
- UI authors: [historical AGENTVIZ workshop](deprecated/ui/README.md), which defines no new Laomedo behavior.
- Work Graph authors: [owned contract](subsystems/work-graph/contract/work-graph.md) and [validation](subsystems/work-graph/validation.md).

| Root child | Cardinality | Responsibility |
| --- | --- | --- |
| README.md, SPECS.md, spec.json | 1 each | Navigation, authoring policy, structural declarations |
| architecture/, implementation/ | 1 each | Shared relationships and contributor procedures |
| subsystems/, experiments/, research/ | 1 each | Contracts, bounded trials, exploratory knowledge |
| deprecated/ | 1 | Existing non-authoritative historical assets |
| capabilities/, components/, feasibility/, monitoring/, sandboxing/ | 1 each | Fixed compatibility pointers preserving published paths; no new specifications |

The pilot retains existing Docker permissions and a private single-user login. Hosted
identity, Claude parity, browser interaction and full monitoring remain unverified.
The saved Langflow node starts fresh runs; resume was verified through the runner API.
