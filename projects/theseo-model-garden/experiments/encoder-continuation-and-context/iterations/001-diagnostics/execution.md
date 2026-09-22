# D0-D2 execution

Run on source `ebb0e44` (`exp/360`) with three seeds, a 17-cubed lattice, 20% masking,
and fresh 48/24/48 train/selection/assessment geometries balanced across four families
and three densities. D0 verified fixtures and metric machinery. D1 trained the fixed
four-block supervised spatial reference for 2,048 updates. D2 trained linear, 32-unit,
and 128-unit heads for 1,024 updates on the same sampled rows, selecting capacity and
F1 threshold on selection only. Boundary F1 0.70 plus the registered paired log-loss
interval governed the result. The campaign completed in 74.86 recorded seconds on an
RTX 3060 Ti; there were zero encoder updates.
