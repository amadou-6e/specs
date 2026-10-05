---
title: EXP-01 evidence manifest
status: complete
kind: experiment-evidence
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

| Artifact | Revision or SHA-256 |
| --- | --- |
| Governing Work Graph contract baseline | specs `7f6760e22cbdd0128e608a6591a1c94bdfd685bf` |
| Prospective protocol | specs `bf9dc494b20d8a9d683791b9e07630fe1a06d21f` |
| Independent corpus, oracle, probe and built source | Laomedo `7597c89d4dd2b305522f011240223079fd547ac9` |
| Installed wheel `laomedo-0.1.0-py3-none-any.whl` | `7c2a129fb23c023c0d9f6f8c823a6ce4f64fe80335ec618cd8a1eb3ca34a770f` |
| [Frozen corpus](https://github.com/amadou-6e/laomedo/blob/7597c89d4dd2b305522f011240223079fd547ac9/experiments/exp01/corpus.json) | `019c59cec9d128179ec0f335db495ddeb12ab3fad72fef2fac6b23496f48797c` |
| [Hand-checked oracle](https://github.com/amadou-6e/laomedo/blob/7597c89d4dd2b305522f011240223079fd547ac9/experiments/exp01/oracle.json) | `1d6b1addd6513f961acbc219cdb3a28520c1387e1b241a10916f83000098c53e` |
| [Published sanitized result](https://github.com/amadou-6e/laomedo/blob/test/50/experiments/exp01/result.json) | `ffdb212dc8cdd63448282c1199703bfbb9d6522092286e1d8d8b822838cb831f` |

The result file contains each case's response-page digest, observed values and expected values. Its only redaction substitutes a placeholder for the disposable private virtual-environment path. The unredacted local result was used to confirm import from `site-packages`; no account or token fields were present. The saved refresh snapshots were disposable artifacts, with both IDs and retention checks captured in the result file. No live source material was exported.
