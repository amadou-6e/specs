# Tiled-context results

All four non-inferiority checks passed against both dense controls. Tiled boundary F1
was 0.6905/0.6838/0.7021 on sampled central-49 queries. Dense-65 coverage took
21.8-23.5 ms/scene at 176.60 MiB allocated peak; tiled-33 took 96.9-104.7 ms/scene at
112.19 MiB. Tiling was 4.1-4.8 times slower for 36.5% lower allocation, so it was
retained as a memory option rather than the speed or default path. No larger-radius or
full-volume claim followed.
