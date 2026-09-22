# Engineering-screen execution

## Ordered executions

| Study and run | Frozen identity | Execution |
| --- | --- | --- |
| `compact-c0c3-smoke-v2` | protocol `04673aba3906a50c9a51e4631ef910f8a3e767e7`, source `d34e534` | Replacement for an invalid deterministic-CUDA v1; 18 profiles, six 96-step fits, and fresh probes. |
| `compact-controls-v1-run1` | protocol `97e205793e6e443199f118b528c0c3fc9181e76c`, source `3987482` | 60 frozen-representation probe fits across compact, spatial, raw-neighborhood, coordinate, and random controls. |
| `compact-learnability-v1-run1` | protocol `1bf1359b55b7c9aef2de1fe23a831e2e850009e0`, source `91d50ad` | Six 2,048-step fits on four scenes comparing oracle, learned-table, and actual-encoder inputs with two decoder bundles. |
| `compact-dense-v1-run1` | protocol `fd8eba978a6100b997cc762dbea6078d3b0f5686`, source `2afe8f0` | Three 1,024-step full-grid dense-output fits on fresh four-scene data. |

These studies used deterministic float32 CUDA and bounded single-process execution.
Each successor changed only the diagnostic needed to separate representation learning
from probe or query-decoder difficulty. Those changes prevent treating the four runs
as a matched aggregate comparison.
