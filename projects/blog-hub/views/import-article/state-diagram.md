# Import Article - State Diagram Index

[import-article.drawio](import-article.drawio) is the sole authority. Its `Import Article
· Upload` and `Import Article · Review` pages contain the `IMPORT ARTICLE · SOURCE
TRANSITIONS` and `IMPORT ARTICLE · REVIEW TRANSITIONS` lifecycle regions.

This Markdown file is only a searchable projection. Two entry modes are represented in
the Draw.io and converge on the same Review state.

## State summary

| State | Draw.io behavior |
|---|---|
| Entry mode | Route selects upload or connected-platform source |
| File drop | `IM-14/15` accepts Markdown; invalid input enters Source error |
| Platform picker | `IM-05` chooses a connected platform |
| Draft list | User selects a remote draft and `IM-11/24` continues |
| Source error | Invalid upload or failed fetch remains visible; `IM-17/21` retries |
| Review | Editable title and preview for either source path |
| Importing | `IM-25` submits the import and disables actions while in flight |
| Editor | Automatic `201` success opens the created article |
| Import failed | Automatic `4xx/5xx` failure shows a retryable banner |
| Return | `IM-22/23` returns to Overview or Create Article |
