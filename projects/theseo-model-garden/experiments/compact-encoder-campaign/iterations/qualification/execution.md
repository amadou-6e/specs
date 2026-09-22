# Qualification execution

## Ordered executions

The retained fine729 recipe was replicated on fresh identities for seeds 401, 402,
and 403. The experimental package then exported those frozen encoders and native heads
under manifest identity
`2ddf188ecedff4699dba434fec05a851c5649119c07dcf30c9d9afd1292d4ed1`.

The final qualification execution used frozen protocol
`191f883a24b67afe75a5ce9b0783f53351802423`, implementation `e16fbc6`, and manifest
commit `a40a7ec`. Robustness ran at `runtime/compact-robustness-v1-run1`; collision
transfer ran at `runtime/compact-collision-transfer-v1-run1`. It evaluated the same
three packaged seeds without selecting among them or retraining the encoder.

Robustness produced 2,016 paired observations across seven generators and 12
conditions. Collision transfer completed 12 heads, 4,096 updates each, across compact,
raw, spatial, and null inputs. All thresholds were locked before ID/OOD test access.
The two studies accounted for 3,706.844 seconds, and replay verified the recorded
artifacts and unchanged encoder states.
