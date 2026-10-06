---
title: EXP-16 execution
status: complete
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The prospective protocol was committed at specs `1df9f000f702e43bd1429682d451160f6adc6115`. The six synthetic source variants and 20 hand-written decisions were committed in Laomedo at `716baeb` and `a776578` before the probe ran. The probe was committed at `6495714b0c9bce4a319dc74609b589f93e91c381` before its first execution. Laomedo's merged `develop` product baseline was `d3be94acf05b9720d55e4b9844067f073052846d`; the intervening commits add experiment files only. The contract baseline was specs `ddb99c6d4aef61679df91229b668d0a87714e8bf`. Connector `github-gh-v1`, schema `1`, package `0.1.0` and fixed clock `2026-10-05T10:00:00+00:00` were used.

On Windows, `uv 0.12.13` built a wheel offline with existing Python 3.10.21 and setuptools 84.0.0. The wheel was installed with `uv pip install --no-index` into a fresh disposable virtual environment outside Git. The probe ran from the checkout via installed Python in isolated mode; its recorded package path resolved to that environment's `site-packages`. Each case used a separate SQLite store and snapshot directory under a fresh outside-Git output directory. The commands were:

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'laomedo-exp16-20261005\uv-cache'
uv build --wheel --no-build-isolation --offline --python '<local Python 3.10 with setuptools>' --out-dir (Join-Path $env:TEMP 'laomedo-exp16-20261005\dist')
uv venv --python '<same Python 3.10>' (Join-Path $env:TEMP 'laomedo-exp16-20261005\venv')
uv pip install --python (Join-Path $env:TEMP 'laomedo-exp16-20261005\venv\Scripts\python.exe') --no-index (Join-Path $env:TEMP 'laomedo-exp16-20261005\dist\laomedo-0.1.0-py3-none-any.whl')
& (Join-Path $env:TEMP 'laomedo-exp16-20261005\venv\Scripts\python.exe') -I experiments\exp16\probe.py --output-dir (Join-Path $env:TEMP 'laomedo-exp16-20261005\run')
```

The existing `test_work_graph.py`, `test_workflow_run_store.py` and `test_exp19_probe.py` suites passed separately: 12, 3 and 3 tests. The experiment used zero model turns, no GitHub requests or writes, no real stage launch and no production grant. The [published result](https://github.com/amadou-6e/laomedo/blob/1906f8b3440c4beef0f9325bf2cb452a3351e418/experiments/exp16/result.json) replaces only the disposable installed-package path with a placeholder; raw SQLite and wheel artifacts remain outside Git.

The probe's `corpus_sha256` is the local Windows working-tree byte hash, including CRLF line endings. The Git blob uses LF bytes; both hashes are in the [manifest](evidence/manifest.md). The committed source revision and parsed synthetic response pages, rather than platform-specific line endings, anchor reproduction of the decisions.
