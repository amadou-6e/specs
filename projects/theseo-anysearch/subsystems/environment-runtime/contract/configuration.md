# Environment runtime configuration

This page identifies settings that change episode behavior. It points to the exact
schema modules instead of duplicating every Pydantic field.

`theseo_anysearch/settings/environment/environment.py` defines main environment and
episode settings. `theseo_anysearch/settings/environment/action.py` selects the action
mode, which changes cardinality, movement mapping, mask ordering, and checkpoint
compatibility. `theseo_anysearch/settings/environment/lifecycle.py` configures ordered
Python lifecycle rules; order is behavioral because later rules can combine or
override earlier outcomes.

Waypoint, curriculum, and scenario configuration can provide episode state. Compiled
worlds require one of these explicit sources. Invalid combinations fail before useful
execution rather than being silently coerced.

Action mode, episode limit, lifecycle chain, episode source, and runtime variant all
affect reproducibility and belong in experiment identity. Provider cache and world
content identities belong to their owning subsystems.
