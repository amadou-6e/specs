# 33-to-65 results

All four non-inferiority checks passed, but no gain interval was strictly positive.
Occupied-IoU improvement CI was [-0.00124, 0.00678], boundary-F1 CI
[-0.00551, 0.00883], and both distance intervals were near zero. Total peak CUDA
allocation was 107.70 MiB at 33 and 610.98 MiB at 65; latency was 13.25-15.60 versus
86.70-86.75 ms/batch. Shared weights were retained, but 33 was preferred for this
local task because 65 showed no clear benefit at higher cost.
