# Training and tuning extension points

This page defines supported composition boundaries, not permission for arbitrary code
to mutate trainer state.

Custom completion conditions must declare configuration, finite evaluation behavior,
serializable state, and deterministic composition semantics. Custom metrics must use
the normalized reporting path, distinguish absence from zero, and avoid redefining an
existing canonical name. Reward and lifecycle extensions remain environment-runtime
extensions even when training consumes their metrics.

Pretraining implementations must publish checkpoint and cache identities covering
architecture, input schema, training settings, and initialization scope. A failure to
validate compatibility aborts handoff rather than partially loading a policy.
