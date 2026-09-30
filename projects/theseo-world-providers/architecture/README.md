# World-provider architecture

Provider plugins produce candidate bundles behind a versioned Python boundary. The
provider-neutral service validates artifacts and rights, derives previews and a
verification report, and makes accepted bundles available for explicit attachment by
a consumer. The [historical CLI design](world-provider-cli.md) supplies background;
the current subsystem contract is authoritative where the two differ.

The [Python package-boundary plan](../implementation/python/package-boundary.md)
assigns SDK, provider-wheel and AnySearch-host ownership and records the staged
implementation in [AnySearch PR #505](https://github.com/amadou-6e/theseo-anysearch/pull/505).
