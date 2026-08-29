# Create article UI

Derived written layout index: [Create article view](../layout.md)

The [Create Article Draw.io](../create-article.drawio) is the sole authority. It contains separate tabs
for Prompt & Context, Configure, and Destinations. Each tab includes its editable
transition logic beneath the full screen. Current implementation screenshots remain in
`references/`.

State ID prefix: `CREATE-ARTICLE-*`.

## Interaction markers

Amber `CA-*` badges in the Draw.io are the stable interaction IDs;
[interactions.md](../interactions.md) is their searchable projection.
User-triggered transition edges repeat the triggering ID; `SYSTEM` labels identify
validation, polling, and other automatic work. Regenerate the managed annotations with
`python3 tools/generate_bloghub_interaction_markers.py`.
