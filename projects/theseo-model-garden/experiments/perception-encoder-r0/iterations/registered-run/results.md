# Results

## Registered disposition

Decision: **defer**. Required stop: `no_topology_identifiable`. P0C, P0D, and P1 did
not start.

## Support

All 216 training and 144 audit quotas were filled. The 23,040 selected labels included
9,216 audit labels.

| Span | In-domain negatives | Transfer negatives | Required per domain | Disposition |
|---|---:|---:|---:|---|
| `1-2` | 84 / 1,536 | 0 / 1,536 | 64 | Unevaluable: transfer support failed |
| `3-5` | 79 / 1,536 | 0 / 1,536 | 64 | Unevaluable: transfer support failed |
| `6+` | 117 / 1,536 | 154 / 1,536 | 64 | Evaluated; all gates failed |

## `6+` gate evaluation

| Gate | Observed bound | Required | Result |
|---|---:|---:|---|
| Conditional entropy | `0.915733` | `< 0.90` bits | Failed |
| Visible skill | `-0.077859` | `> 0.02` bits/query | Failed |
| Forbidden-feature skill | `0.144125` | `< 0.02` bits/query | Failed |
| Transfer drop | `0.156454` | `< 0.05` bits/query | Failed |

The transfer `6+` entropy point estimate was `0.447082` bits, but a point estimate
cannot override the registered conservative bound.

## Interpretation and non-claims

This empirical patch prior, transfer, controls, and budget supplied insufficient
evidence of identifiable completed connectivity. Forbidden metadata was not supplied
to the visible model, so its gate failure does not establish leakage. The result does
not show hidden geometry is random, prove topology unlearnable, or rank any encoder.

The stop rule prohibits continuation. Any local-geometry successor requires a new
protocol rather than retrospective changes to this one.
