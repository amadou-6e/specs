# Python explainability responsibilities

This page follows the pipeline at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/rllib/explain/service.py` orchestrates a request.
`theseo_anysearch/rllib/explain/backend.py` restores supported RLModules and spaces.
`theseo_anysearch/rllib/explain/scenarios.py` and
`theseo_anysearch/rllib/explain/requests.py` validate inputs;
`theseo_anysearch/rllib/explain/traces.py` reconstructs policy-evaluation traces;
`theseo_anysearch/rllib/explain/scoring.py` implements algorithm-specific scores.
`theseo_anysearch/rllib/explain/features.py` derives groups and
`theseo_anysearch/rllib/explain/explainers.py` performs occlusion.
`theseo_anysearch/rllib/explain/reports.py` and
`theseo_anysearch/rllib/explain/models.py` serialize results.

Interactive state is handled by `theseo_anysearch/rllib/explain/ui/session.py`,
`theseo_anysearch/rllib/explain/ui/editor.py`, and
`theseo_anysearch/rllib/explain/ui/artifacts.py`.
`theseo_anysearch/rllib/explain/native_bridge.py` exposes the persistent JSONL
process used by the Rust viewer.

An unresolved compatibility question remains:
`PolicyEvaluationTraceCollector._cursor` in
`theseo_anysearch/rllib/explain/traces.py` reads
`observation["cursor_pos"]`, while the live single-agent observation contract removed
that field. Tests may use legacy fixtures and other service paths handle cursor state
separately; generic collector compatibility must not be claimed until reconciled.
