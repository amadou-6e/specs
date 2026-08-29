# BlogHub UI specification map

This directory is the entry point for UI material that spans more than one view.
View-specific sources live with the written specification under `views/<view>/ui/`.

## Ownership rules

- A complete page belongs in `views/<view>/ui/`.
- A component used by one view belongs in `views/<view>/ui/components/<component>/`.
- A reused component stays with the view that defines its behavior.
- Only genuinely ownerless components belong in `shared/`.
- Cross-view transitions belong in `flows/` and reference stable state IDs.
- Superseded combined workshops belong in `archive/` and are not canonical sources.

## Artifact rules

- `*.drawio`: the sole authority for UI geometry, component states, interaction IDs,
  and transitions; stored as uncompressed XML.
- `references/`: fidelity evidence from the running application or user feedback, not
  an alternate specification.
- `README.md` and other Markdown: searchable indexes, implementation notes, and test
  projections derived from the owning Draw.io.

An implementation ticket must not infer a control or state from stale Markdown. If its
required behavior is absent from the owning Draw.io, update and review the Draw.io first
or provide that specification change as a stacked PR before implementation.

Draw.io exports are temporary inspection artifacts. Do not commit them: they can drift
from the editable source and create a second, unreliable representation of the design.

Do not create timestamped Draw.io backups. Inspect the current Git diff before editing
and use branches and commits to preserve design history.

## Views

| View | UI specification |
|---|---|
| Overview | [views/overview/ui](../views/overview/ui/README.md) |
| Editor | [views/editor/ui](../views/editor/ui/README.md) |
| Create article | [views/create-article/ui](../views/create-article/ui/README.md) |
| Import article | [views/import-article/ui](../views/import-article/ui/README.md) |
| Settings | [views/settings/ui](../views/settings/ui/README.md) |
| Login | [views/login/ui](../views/login/ui/README.md) |
| Inspection | [views/inspection/ui](../views/inspection/ui/README.md) |
| Publish schedule | [views/publish-schedule/ui](../views/publish-schedule/ui/README.md) |

See [application navigation](flows/application-navigation/README.md) for the current
cross-view transition diagram and [the archive](archive/current-pages/README.md) for
the retired combined-page workshop.
