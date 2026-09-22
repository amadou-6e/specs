# LG1 results

Disposition: both occupancy and ESDF are **`not_qualified`**.

| Metric | Occupancy seeds 0 / 1 | ESDF seeds 0 / 1 |
| --- | --- | --- |
| Hidden occupied IoU | 0.9269 / 0.9354 | 0.8837 / 0.8033 |
| Hidden exact boundary F1 | 0.7811 / 0.8043 | 0.7146 / 0.5914 |
| Observed-free clearance NMAE | 0.1904 / 0.1833 | 0.0515 / 0.0553 |
| Hidden-free recovery NMAE | 0.2023 / 0.1793 | 0.0530 / 0.0563 |
| Effective-rank fraction | 0.20204 / 0.19716 | 0.24991 / 0.24587 |

Occupancy failed clearance in both seeds and recovery in seed 0. ESDF failed
boundary in seed 1. Every run failed LG1's 0.25 rank floor without rounding. All
control-improvement and paired-bootstrap gates passed, and integrity checks found no
dead channels, input leakage, or encoder mutation. The failed conjunctive gates
therefore determine the verdict despite high occupancy scores.

This supports complementary objective-specific local information, not a navigation,
topology, or architecture-selection claim. Joint training was authorized only as a
freshly registered follow-up.
