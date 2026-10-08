---
name: claude-reviewer
description: Request an independent, read-only review from the locally authenticated Claude Code CLI for a reviewable code, specification, or PR change. Reuse one Claude reviewer conversation for the current Codex session and the existing Claude subscription login; do not ask the user to relay routine review feedback.
---

# Claude reviewer

When authorized work is ready for an independent review, invoke Claude Code directly and address its evidence-backed findings. Use this for implementation, specification, and PR reviews. Do not ask the user to act as a messenger between Codex and Claude.

## Prepare a bounded review

Identify the exact repository, base and head revisions, changed files, applicable specifications, and checks already run. Give Claude a specific review question and ask for findings ranked by severity with file and line references, a short account of what it verified, and explicit uncertainty. Ask it to read applicable `AGENTS.md` or `CLAUDE.md` and inspect the actual files and diff, not just a summary. Keep credentials, raw login state, personal transcripts, and unrelated private files out of the prompt.

The reviewer is read-only. It must not edit files, post GitHub comments, change issues, approve or merge PRs, or run model-backed probes. Prepare any diff or PR metadata Claude needs in the authorized workspace before invoking it. Do not treat a Claude review as the user's approval where repository rules require explicit approval.

## Keep one reviewer conversation per Codex conversation

Use [Invoke-ClaudeReview.ps1](scripts/Invoke-ClaudeReview.ps1) from the same trusted workspace root for every review in this Codex conversation. The script keys an ignored local state file by `CODEX_SESSION_ID`: its first successful call creates a Claude session and later calls resume that session. A new Codex conversation gets a new Claude reviewer session. Never resume a user's interactive Claude/VS Code session for this workflow, and never run two calls to the reviewer session concurrently.

The script discovers the newest installed Claude Code VS Code executable, checks that the existing `claude.ai` subscription login is active, and uses that login in place. It does not copy, export, or print auth files or tokens. Keep the ordinary `HOME`, `USERPROFILE`, and Claude config directory; do not set provider credential overrides, use `--bare`, or create a disposable Claude profile. If authentication is missing or expired, report that once rather than asking the user to sign in for each review.

For this long-lived reviewer conversation, the launcher sets Claude Code's
`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=60` in the child process only. It does not
change global Claude settings or the user's interactive sessions. Existing
reviewer context above 60% may compact on a later review turn; this does not
create a new reviewer session.

Claude needs provider network access for the review turn. If the calling tool context blocks that connection, run the same script in an authorized network-enabled context with the same OS profile and state directory. Do not respond by copying the login or starting a different reviewer session.

Write a prompt file in the trusted workspace, then run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  '.\specs\shared\skills\claude-reviewer\scripts\Invoke-ClaudeReview.ps1' `
  -WorkspaceRoot 'C:\CodeWorkspace\agentviz' `
  -StateDirectory 'C:\CodeWorkspace\agentviz\claude-review.local\sessions' `
  -PromptFile 'C:\CodeWorkspace\agentviz\claude-review.local\prompt.txt'
```

Use equivalent absolute paths when this skill is used elsewhere. The per-process execution-policy override runs only this checked-in script and does not change machine settings. The state and prompt paths must be ignored by Git and remain outside tracked specifications. The state file contains only session identifiers and initialization status, never credentials. The script confines Claude's tools to file reading, disables customizations and MCP servers, denies permission prompts, and times out after three minutes by default. It returns Claude's structured result on stdout; preserve a concise finding summary and the reviewed revision in the work handoff.

## Apply the review

Check each finding against source and tests. Fix confirmed in-scope defects, rerun affected checks, and ask the same Claude reviewer session to recheck the new revision. Explain rejected or out-of-scope findings with evidence. A clean review is evidence for the stated revision, not proof that all behavior works. Keep issue-edit, configuration, publication, and merge approval rules in force.

Where repository guidance permits merging after independent review, a review of
the final PR head can satisfy that merge requirement once its checks pass. It is
not a human approval and does not waive a pause for a recommendation that
conflicts with the human's interests or instructions.
