# 17-to-33 results

The frozen 33 arm improved all four central-query tasks over frozen 17: boundary F1
rose from 0.696-0.722 to 0.739-0.756 and IoU from 0.660-0.679 to 0.687-0.717. Short
retraining did not beat the established frozen-33 encoder on surface tasks. Incremental
batch-4 allocation rose from 9.93 to 72.91 MiB. Shared weights were retained for a
separately registered 65-cubed check; no full-volume or radius-512 claim followed.
