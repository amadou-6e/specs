# 17-to-33 execution

Source `6dea43e` generated nested 17- and 33-cubed crops from fresh 49-cubed parent
scenes and evaluated identical central-17 queries and targets. Three seeds compared
frozen validated encoders at both sizes and short 512-update retraining arms, with a
separate fixed 32-hidden probe per arm/task/seed. Paired whole-parent bootstrap
comparisons covered four local tasks. Batch-4 inference and training resources were
profiled. The full run took 247.15 seconds without out-of-memory failure.
