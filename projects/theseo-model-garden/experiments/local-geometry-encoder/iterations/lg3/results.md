# LG3 results

Primary disposition: **`not_confirmed`**.

| Metric | Fresh-probe mean | Unchanged LG2 probe mean |
| --- | ---: | ---: |
| Occupied IoU | 0.6414 | 0.6256 |
| Boundary F1 | 0.3029 | 0.4620 |
| Clearance NMAE | 0.0525 | 0.0556 |
| Recovery NMAE | 0.0521 | 0.0554 |

Pooled occupancy passed, but oblique sheets failed per-family IoU in every seed
(0.2425/0.3102/0.2700). Boundary failed its absolute bar for every family and seed;
aggregate seed scores were 0.0000/0.5124/0.3963, and seed-0 control improvement also
failed. Clearance and recovery passed all family absolute bars. Encoder state, mask
isolation, and dead-channel integrity gates passed.

Thus distance transfer has component-level support, while broad local-surface and
geometry confirmation does not. Fresh-probe failure does not isolate encoder,
sampling, aliasing, or optimization causes. This is not total collapse and does not
revise LG2's narrower in-family result. It authorizes no tuning on LG3 evaluation,
architecture scaling, or navigation/topology claim.
