# Experiment tracking configuration

This page identifies tracking selectors defined by `MLflowConfig` and experiment
settings in `theseo_anysearch/experiments/models.py`.

MLflow tracking is disabled when no URI is configured. When enabled, the tracking URI,
experiment name, and run metadata select the remote/local MLflow destination. Output
directory settings select authoritative local storage independently. Authentication is
supplied through the supported MLflow environment/client mechanism and must not be
written into run artifacts.

Changing a tracking URI or experiment name changes publication location, not training
semantics or run identity. A missing/unavailable backend enters degraded state rather
than redirecting artifacts silently. Full resolved settings remain local because
flattening, omission, encoding, and truncation make MLflow parameters lossy.
