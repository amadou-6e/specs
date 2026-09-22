# Trajectory storage migration

This page records compatibility between historical and current replay artifacts.

Current writers publish finite-valued zstd-compressed JSON as `.json.zst`. Readers
continue to accept legacy uncompressed `.json`; they do not rewrite or remove it. A
corrupt current-format file takes precedence and fails rather than falling back.

Compiled-world trajectories use a schema-v2 world reference plus sparse overlay
mutations. Small-world sidecar occupancy remains a different representation. Tools
must branch on the declared schema rather than assuming compression was the only
format change.
