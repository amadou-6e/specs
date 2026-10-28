---
name: claude-reviewer
description: Compatibility pointer to the canonical claude-reviewer skill in amadou-6e/my-skills. Use when requesting an independent, read-only Claude Code review of code, specifications, or PRs; read the canonical instructions before invoking the reviewer.
---

# Claude reviewer

The reviewer skill and its bundled scripts are maintained in
`my-skills/05-software_engineering/skill-claude-reviewer/`, not in this repository.

For sibling checkouts, read the local canonical skill at
`../../../../my-skills/05-software_engineering/skill-claude-reviewer/SKILL.md`.
Otherwise, read the [canonical skill on GitHub](https://github.com/amadou-6e/my-skills/blob/main/05-software_engineering/skill-claude-reviewer/SKILL.md).
Follow that skill's instructions and use its launcher in `01-scripts/`.

The former `scripts/` entry points have been removed. Invoke
`my-skills/05-software_engineering/skill-claude-reviewer/01-scripts/Invoke-ClaudeReview.ps1`
from the canonical checkout instead of calling the old specs script path.

Keep this path as a compatibility entry point for existing specifications and
agent guidance. Do not copy the review workflow or scripts back into `specs`.
