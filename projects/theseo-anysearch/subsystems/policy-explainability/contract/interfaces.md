# Policy explainability interfaces

This page describes the CLI, request/report objects, and native bridge at product
revision `72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/cli/commands/explain.py` exposes non-interactive explanation, while
`theseo_anysearch/cli/commands/explain_ui.py` launches the interactive workflow.
`theseo_anysearch/rllib/explain/requests.py` validates requests and
`theseo_anysearch/rllib/explain/scenarios.py` defines environment/fictional scenario
inputs. Reports and serialized models live in
`theseo_anysearch/rllib/explain/reports.py` and
`theseo_anysearch/rllib/explain/models.py`.

The Python service emits reproducible artifacts containing identities, source
provenance, scores, grouped effects, backgrounds, and limitations. The persistent
JSONL protocol in `theseo_anysearch/rllib/explain/native_bridge.py` supports the native
viewer. It accepts strict JSON/NPY/NPZ/PB/TENSOR input shapes and optionally imports
TensorFlow TensorProto support; optional format support must not relax shape checks.

The native consumer in `theseo_anysearch/core/src/replay/explain.rs` and
`theseo_anysearch/core/src/bin/voxel_replay.rs` derives controls from schema metadata
rather than hard-coding observation fields.
