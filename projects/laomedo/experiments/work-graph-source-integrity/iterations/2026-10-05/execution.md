---
title: EXP-01 execution
status: complete
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The prospective protocol was committed in specs at `bf9dc494b20d8a9d683791b9e07630fe1a06d21f`. The response corpus, handwritten oracle, and probe were then committed in Laomedo at `7597c89d4dd2b305522f011240223079fd547ac9`. The oracle was not generated from Work Graph output. The wheel was built from that Laomedo revision; Work Graph connector `github-gh-v1`, schema `1`, package `0.1.0`.

On Windows, `uv 0.12.13` built the wheel using an existing Python 3.10.21 interpreter and local setuptools 84.0.0 with `--no-build-isolation --offline`. The first isolated-build attempt could not fetch setuptools because the tool sandbox blocked PyPI; it spent no model turn and changed no source. The wheel was installed with `uv pip install --no-index` into a fresh disposable virtual environment outside Git. The probe ran via that environment's Python with `-I`, so the import resolved to its `site-packages`, not the source checkout. The complete command pattern was:

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'laomedo-exp01-20261005\uv-cache'
uv build --wheel --no-build-isolation --offline --python '<local Python 3.10 with setuptools>' --out-dir (Join-Path $env:TEMP 'laomedo-exp01-20261005\dist')
uv venv --python '<same Python 3.10>' (Join-Path $env:TEMP 'laomedo-exp01-20261005\venv')
uv pip install --python (Join-Path $env:TEMP 'laomedo-exp01-20261005\venv\Scripts\python.exe') --no-index (Join-Path $env:TEMP 'laomedo-exp01-20261005\dist\laomedo-0.1.0-py3-none-any.whl')
& (Join-Path $env:TEMP 'laomedo-exp01-20261005\venv\Scripts\python.exe') -I experiments\exp01\probe.py --output-dir (Join-Path $env:TEMP 'laomedo-exp01-20261005\run')
```

The run used zero model turns, no credentials, no GitHub API calls, and no issue or PR mutations. Temporary wheel, environment, and saved snapshots remain outside Git. A copy of the probe result with its private host path replaced by a placeholder is published in the Laomedo experiment directory.

## Filtered-readiness amendment

The original eight-case artifact was retained. Review identified the missing projected-readiness assertion. The nine-case corpus, handwritten oracle and updated probe were committed at Laomedo `de32cc8` before rerun, and the [amendment plan](amendment-plan.md) was committed at specs `b3a0462` before rerun. The fresh wheel was built from `de32cc8` with the same offline `uv` command pattern above, installed in a new disposable environment under `laomedo-exp01-amend-20261005`, and probed with `-I` into its own `run` directory. The published [sanitized amendment result](https://github.com/amadou-6e/laomedo/blob/b2648e1b0f5803c149c12d45550ff44fd43eb9ed/experiments/exp01/result-amendment.json) is separate from the first result. No product Work Graph implementation file changed between the two runs.
