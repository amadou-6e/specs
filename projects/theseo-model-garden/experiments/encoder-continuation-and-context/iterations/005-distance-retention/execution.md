# Distance-retention execution

Source `577da2e` froze the old and new encoders for seeds 0/1/2 and trained fixed
32-hidden SiLU probes for clearance and recovery on a fresh 192/48 train/assessment
corpus. Each probe used 1,024 updates, train-only normalization, equal exposure, and no
assessment selection. Retention required both registered task-level intervals, every
seed difference, and every new-seed absolute error threshold to pass.
