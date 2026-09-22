# LG2 results

Primary disposition: **`joint_preserves_specialists`**. Joint qualifies for local
follow-up; occupancy and ESDF remain `not_qualified` under all-task conjunction.

| Three-seed mean metric | Occupancy | ESDF | Joint |
| --- | ---: | ---: | ---: |
| Hidden occupied IoU | 0.9410 | 0.8699 | 0.9378 |
| Hidden exact boundary F1 | 0.7890 | 0.7255 | 0.8225 |
| Observed-free clearance NMAE | 0.1820 | 0.0490 | 0.0491 |
| Hidden-free recovery NMAE | 0.1771 | 0.0479 | 0.0489 |

Joint passed every absolute, control, integrity, and frozen noninferiority gate in all
three seeds. Its paired 95% intervals versus specialists were IoU
[-0.00979,+0.00388], boundary [+0.01461,+0.05295], clearance
[-0.00159,+0.00133], and recovery [-0.00245,+0.00040], all inside their margins.
Occupancy failed clearance in every seed; ESDF failed boundary in seed 1.

Joint did not pass LG1's historical rank floor, but LG2 had prospectively made rank a
diagnostic, while retaining task, control, dead-channel, and integrity gates. The
result retains the joint recipe for independent-generator confirmation only; it does
not establish an optimal weighting, architecture, topology, or deployment readiness.
