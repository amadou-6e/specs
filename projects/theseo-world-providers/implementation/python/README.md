# Python implementation

The provider-neutral Python implementation currently lives in
`theseo_anysearch/world_providers/`; optional provider distributions live below
`providers/`. Providers must depend on the public extension contract rather than
consumer-internal environment or training modules.

The [package-boundary plan](package-boundary.md) records the target extraction
contract, compatibility rules, and tests. It is not yet the implemented layout.
