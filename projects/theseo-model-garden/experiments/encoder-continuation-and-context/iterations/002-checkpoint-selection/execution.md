# Checkpoint-selection execution

Source `d7b8e7a` reran the D1 architecture, optimizer, batch size, and 2,048-update
trajectory for seeds 0/1/2 on a fresh 48/24/48 corpus. It retained the final weights
and lowest-selection-loss checkpoint from registered intervals, reran D0, and refit the
linear/32/128 probe ladder. Assessment used paired geometry log loss with 2,000
stratified cluster-bootstrap draws. All three trajectories completed in 71.39 seconds;
all selected update 256 and made zero encoder updates.
