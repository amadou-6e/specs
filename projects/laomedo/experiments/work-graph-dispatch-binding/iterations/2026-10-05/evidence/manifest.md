---
title: EXP-16 evidence manifest
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
| Work Graph contract and specs baseline | `ddb99c6d4aef61679df91229b668d0a87714e8bf` |
| Prospective EXP-16 protocol | specs `1df9f000f702e43bd1429682d451160f6adc6115` |
| Installed Laomedo product baseline | `d3be94acf05b9720d55e4b9844067f073052846d` |
| Frozen corpus/cases/oracle | Laomedo `716baeb`, then `a776578` for the filtered projection expectation |
| Probe before run | Laomedo `6495714b0c9bce4a319dc74609b589f93e91c381` |
| Local installed wheel `laomedo-0.1.0-py3-none-any.whl` | `45811eb4b87e7cdf543ee285c2b02e7ac4454f07f2e7e1543573fd5ffab72684` |
| Frozen `corpus.json`, local Windows working-tree bytes read by probe (CRLF) | `6517d65a101eaba5ef1e126d3440d9a8e21daafe44b4078cf47772377e7fabb2` |
| Frozen `corpus.json`, published Git blob bytes (LF) | `af6625036a4c9213498dc1c932a1a057db22591df376f380e8db5cec332c8f4d` |
| Frozen `cases.json` | `ea8a66961f38206c9c1e0de3d330cda8a346b6c157629392bcff1acc7498e03f` |
| Hand-written `oracle.json` | `5fa15ce568ddbe1932730505e7b37b7d926076a221c3a780a0864bd18360dbda` |
| [Sanitized per-case result](https://github.com/amadou-6e/laomedo/blob/1906f8b3440c4beef0f9325bf2cb452a3351e418/experiments/exp16/result.json), published Git blob bytes (LF) | `7bb4753626d53f1cb1a85dd4a0a561f3bc43f4c92b2e53e86a5394a71a2a2df5` |
| Sanitized per-case result, local Windows working-tree bytes (CRLF) | `a8cb63295d8d3524cc05e837fecc93a9202cd82599824d59ffda75f23860f6c1` |

The result contains source snapshot IDs, expected and observed decisions, mock run/trace IDs, counter and artifact checks. It omits the disposable host path to the installed package. No raw private issue body, credential or native model trace was created or published. Windows Git converted the JSON working-tree line endings to CRLF; the probe hashed those actual input bytes, while the committed artifacts use LF. The parsed fixture content and source revision are the same, but a fresh LF checkout will report a different raw file-byte hash. The wheel hash identifies this local artifact, not a guarantee that another wheel build has identical bytes; the product and frozen-input source revisions are reproducible pins. The corpus and oracle were prepared by the experiment author, not an independent second party.
