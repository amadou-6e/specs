# Import article UI

Derived written layout index: [Import article view](../layout.md)

The [Import Article Draw.io](../import-article.drawio) is the sole authority. It contains separate Upload
and Review tabs with editable transition logic beneath each full screen. The import and
review implementation screenshots remain in `references/`.

State ID prefix: `IMPORT-ARTICLE-*`.

## Interaction markers

Amber `IM-*` badges in the Draw.io are the stable interaction IDs;
[interactions.md](../interactions.md) is their searchable projection.
User-triggered transition edges repeat the triggering ID; `SYSTEM` labels identify
validation, fetching, and other automatic work. Regenerate the managed annotations with
`python3 tools/generate_bloghub_interaction_markers.py`.
