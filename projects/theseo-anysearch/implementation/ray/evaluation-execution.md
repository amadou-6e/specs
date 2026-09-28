---
title: Ray evaluation execution
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray evaluation execution

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. Pinned-revision Ray integration tests were read, not run. Evaluation semantics belong to [training and tuning](../../subsystems/training-and-tuning/README.md); this page concerns execution location.

The evaluation helper uses healthy remote evaluation runners, if available, with per-episode seed assignment and sorted results; otherwise it falls back to local collection, including a vector-collection path. Weight synchronization is optional, and the callback is serialized without retaining an `Algorithm` reference. Thus `parallel_evaluation=True` is not proof that an episode ran remotely; runner availability determines the branch. See [`parallel.py` callback](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L18-L66) and [collection branches](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L276-L386).

Run both remote and fallback paths with a real policy; verify weight synchronization and episode identity before claiming execution parity. RLlib evaluation configuration belongs in [environment integration](../rllib/environment-integration.md); evaluation-runner reservations belong in [resources and placement](resources-and-placement.md).
