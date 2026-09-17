# UI design

UI design is an expandable collection of multi-file surface entries. Each entry owns
one independently navigable tab or window.

## Contained elements

```text
ui-design/
├── 1 README.md
├── 1 template/
├── 0..1 shared/
└── 0..* <tab-or-window>/ entries
```

Each surface entry has one `README.md` and one authoritative editable Draw.io file. It
may own references, reviewed captures, and components specific to that surface.
Panels, dialogs, and sidebars remain under their owning tab/window. `shared/` is only
for elements with no single surface owner.

Copy [template/](template/README.md) to create an entry. The template and the current
combined replayer workshop are not tab/window entries under the target structure; the
workshop requires a separate migration.
