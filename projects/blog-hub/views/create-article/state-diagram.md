# Create Article - State Diagram Index

[create-article.drawio](create-article.drawio) is the sole authority. Its three pages
contain the editable screens and their authoritative transition regions:

| Draw.io page | Lifecycle region |
|---|---|
| Create Article · Prompt & Context | CREATE ARTICLE · PROMPT TRANSITIONS |
| Create Article · Configure | CREATE ARTICLE · CONFIGURATION TRANSITIONS |
| Create Article · Destinations | CREATE ARTICLE · GENERATION TRANSITIONS |

This Markdown file is only a searchable projection. It must not add states or
transitions that are absent from the Draw.io.

## Prompt and context

| State | Draw.io behavior |
|---|---|
| Write brief | Required article intent |
| Add context | Optional file, URL, or web-search context |
| Brief ready | Validated prompt can continue with `CA-12` |
| Context error | Invalid context remains on the page and explains recovery |

`CA-09/10` adds context, `CA-11` removes or retries it, and automatic validation is
shown as `SYSTEM` work.

## Configure

| State | Draw.io behavior |
|---|---|
| Choose format | Select article structure with `CA-13` |
| Choose provider | Select Claude or Codex with `CA-14/15` |
| AI Settings | `CA-16` exits to provider configuration when required |
| Tone and length | Generation controls include the `CA-17` target length |
| Destinations | Valid configuration continues with `CA-19` |

Returning from AI Settings is automatic system navigation and preserves the brief.

## Generate

| State | Draw.io behavior |
|---|---|
| Pick destinations | Zero or more platform targets selected by `CA-20` through `CA-23` |
| Generate | `CA-27` submits the canonical article generation job |
| Poll job | Automatic polling follows the accepted request |
| Editor | Successful generation opens the generated article |
| Generation failed | Failure remains visible and `CA-28` retries |
