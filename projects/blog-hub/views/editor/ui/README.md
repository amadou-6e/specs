# Editor UI

Derived written layout index: [Editor view](../layout.md)

## Authoritative source

[editor.drawio](../editor.drawio) is the sole authority. It contains the complete
assembly, interaction lifecycle, and isolated component workshop. The
[component README](components/editor-workshop/README.md) is a searchable index only.

Live implementation screenshots belong in `references/`. Draw.io exports and fidelity
crops are temporary review artifacts and are not tracked.

## Interaction markers

Amber `ED-*` badges in the Draw.io are the stable interaction IDs;
[interactions.md](../interactions.md) is their searchable projection.
They mark the primary assembly and the isolated component state where an action is
visible. User-triggered transition edges repeat the triggering ID; `SYSTEM` labels
identify autosave timing and backend results. Regenerate managed annotations with
`python3 tools/generate_bloghub_interaction_markers.py`.
