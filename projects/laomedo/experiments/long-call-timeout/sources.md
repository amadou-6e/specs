---
title: Long-call timeout sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [Laomedo EXP-10 #40](https://github.com/amadou-6e/laomedo/issues/40)
  defines the long synchronous call and late-effect question, with zero model
  turns and a first-slice gate.
- The governing draft was [Langflow integration Q11/E03](../../subsystems/langflow-integration/design/decision-readiness.md)
  at specs `447c4d5044a5b33f59420c1f95ec103979ad5abf`. It did not claim the
  behavior was implemented or already observed.
- Laomedo base was [`a365238`](https://github.com/amadou-6e/laomedo/commit/a36523845a1e718fb79fb40d42002a03c0cb4861),
  including EXP-04's durable-run prototype. The frozen protocol is
  [`e4f4685`](https://github.com/amadou-6e/laomedo/commit/e4f4685e0a58d3825ab6c6c7175e57fff3ca116a),
  and the first-run probe/tests/observation are at
  [`dee05c2`](https://github.com/amadou-6e/laomedo/commit/dee05c2532de264796cccdc0543b658b0770d966).
  The prospective amendment is at
  [`8ceb50d`](https://github.com/amadou-6e/laomedo/commit/8ceb50de3c9e820b04268543bba9410dd82c31f1),
  and the direct-capture replication is at
  [`1fc002a`](https://github.com/amadou-6e/laomedo/commit/1fc002a2837dc8e4c86c6c6c1cddf2e48c578bb8).
  At experiment time this was issue branch `feat/40`, not a merged product
  capability.
- The runtime image was `langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`
  (Langflow 1.12.3). The source inspection verified that
  `LANGFLOW_WORKFLOW_EXECUTION_TIMEOUT=3` resolves to 3 seconds for the v2
  synchronous route; the native Codex component's HTTP timeout is separately
  configured as 2 or 8 seconds in the fixture.
