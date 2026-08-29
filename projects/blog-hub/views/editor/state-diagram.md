# Editor - State Diagram Index

The `ARTICLE EDITOR · INTERACTION LIFECYCLE` region on the `Editor · Full assembly`
page of [editor.drawio](editor.drawio) is the sole authority. This file is a searchable
projection and must not add behavior absent from that Draw.io region.

## Load and autosave

| State | Draw.io behavior |
|---|---|
| Load article | Requests the article by ID |
| Write - saved | Editor is ready at the current revision |
| Unsaved | `ED-02/24` changed content and armed the two-second debounce |
| Autosave | Optimistic PATCH is in flight with the current revision |
| Saved revision | Save succeeded and the returned revision becomes current |
| Conflict / failure | Local changes remain available for edit or retry |

## Review, comments, patches, and preview

| State | Draw.io behavior |
|---|---|
| Write mode | Canonical Markdown editing surface |
| Review mode | Comment anchors are active |
| Comment | Can be resolved or sent to Fix with AI |
| Patch pending | Generated diff waits for explicit review |
| Accept | Applies the diff and returns through automatic applied state |
| Reject | Keeps the comment open and returns to writing |
| Preview | `ED-43` toggles rendered Markdown beside the editor |

## Exit routes

| Destination | Trigger |
|---|---|
| Inspection | `ED-04/40` runs article checks |
| Articles | `ED-01` returns to Overview |

Both exits preserve the latest accepted or autosaved revision represented in Draw.io.
