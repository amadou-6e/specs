# Reference-refinement execution

Source `7f3727c` screened six preregistered recipes with seed 0 using selection loss,
then persisted the chosen recipe before fresh three-seed confirmation. The selected
recipe used dynamic masks, 192 geometries, learning rate 0.003, and weight decay 0.01.
Baseline, selected reference, and frozen probe were evaluated on disjoint confirmation
data. The run completed in 256.16 seconds with zero encoder updates.
