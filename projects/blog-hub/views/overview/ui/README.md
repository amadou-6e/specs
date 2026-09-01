# Overview UI

Written specification: [Overview view](../layout.md)

The [Overview Draw.io](../overview.drawio) is the sole authoritative artifact. It contains
the full-page implementation, article-card states, details-sidebar study, and interaction
lifecycle on one tab. Markdown files in the parent directory are searchable projections
and test indexes; they must not define states or interactions independently. The running
implementation screenshot is preserved in `references/overview.png`.

## Interaction markers

Amber `OV-*` badges identify interactive elements using the stable IDs from
[interactions.md](../interactions.md). User-triggered transition edges repeat the same
ID; automatic loading, API responses, refresh, recovery, and job polling use stable
`OV-S*` IDs.
The interaction index to the right of the reconstructed screen maps each badge to its
action. Run `python3 generate_interaction_markers.py` from this directory after changing
marker placement or the index.

| ID | Component |
|---|---|
| `OVERVIEW-ARTICLE-CARD` | [Article card](components/article-card/README.md) |
| `OVERVIEW-DETAILS-SIDEBAR` | [Details sidebar](components/details-sidebar/README.md) |
