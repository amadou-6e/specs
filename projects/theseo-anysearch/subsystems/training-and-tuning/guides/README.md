# Running training and tuning

This guide explains the normal local workflow. It assumes the project environment and
native extension are installed and that a validated experiment directory already
exists. A successful run creates an isolated runtime directory with metadata, metrics,
and checkpoints.

1. Start from a maintained example under `usage/experiments/train/` or
   `usage/experiments/tune/`, then copy it to a new experiment directory.
2. Review environment, observation/model, algorithm, evaluation, staging, resource,
   and output settings together; they form one reproducibility boundary.
3. Launch with `anysearch run <experiment-directory>`. For a tagged Tune definition,
   use the run command's `--tag` option rather than the deprecated Tune command.
4. Monitor the emitted runtime path with TensorBoard using the log directory printed
   by the runner.
5. Resume or compare only through persisted run/checkpoint metadata; do not infer
   compatibility from filenames.

If startup rejects an unknown or inactive parameter, correct the experiment instead
of suppressing the warning. If Ray integration fails, distinguish construction/unit
failures from failures requiring a live Ray runtime. Parallel evaluation metrics may
refer to a policy snapshot one update behind the learner.
