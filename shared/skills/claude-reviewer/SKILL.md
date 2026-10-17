---
name: claude-reviewer
description: Request an independent, read-only review from the locally authenticated Claude Code CLI for a reviewable code, specification, or PR change. Reuse one Claude reviewer conversation for the current Codex session and the existing Claude subscription login; do not ask the user to relay routine review feedback.
---

# Claude reviewer

When authorized work is ready for an independent review, invoke Claude Code directly and address its evidence-backed findings. Use this for implementation, specification, and PR reviews. Do not ask the user to act as a messenger between Codex and Claude.

## Prepare a bounded review

Identify the exact repository, base and head revisions, changed files, applicable specifications, and checks already run. Give Claude a specific review question and ask for findings ranked by severity with file and line references, a short account of what it verified, and explicit uncertainty. Ask it to read applicable `AGENTS.md` or `CLAUDE.md` and inspect the actual files and diff, not just a summary. Keep credentials, raw login state, personal transcripts, and unrelated private files out of the prompt.

The reviewer is read-only. It must not edit files, post GitHub comments, change issues, approve or merge PRs, or run model-backed probes. Prepare any diff or PR metadata Claude needs in the authorized workspace before invoking it. Do not treat a Claude review as the user's approval where repository rules require explicit approval.

## Visually validate UI changes

When a change affects a rendered interface or UI design artifact, include visual
validation in the review, alongside the code or specification review. Before
implementation, use the review to assess a proposed layout when one is available;
after implementation, review the actual rendered result. A proposal review does
not establish implementation fidelity.

Prepare local screenshots or rendered design images for the reviewer to open
with its file-reading tool. Supply their exact paths, source revision or artifact,
viewport and captured state, the intended design/reference, and any user-marked
feedback. Include a full-view image for hierarchy and relevant detail images for
changed components, expanded content and affected interaction states. Use real
recorded or live integration data when required by workspace instructions; do not
substitute fixtures without authorization. Keep sensitive content out of captures.

Explicitly ask Claude to open and inspect the images, rather than infer appearance
from markup, screenshot filenames or the implementer's description. Check grouping
of different concerns, heading hierarchy, spacing, typography, contrast, density,
overflow, and consistency with the established UI. Compare the intended design
with the rendered result and address marked feedback. Distinguish visible findings
from interaction or accessibility claims that a static image cannot establish;
provide separate browser/check evidence for those claims.

Require separate code/specification and visual verdicts. The response must identify
which images and states were actually inspected, rank visual findings with image
region references (and source lines where applicable), and state missing coverage.
If images cannot be opened or required states are missing, report visual validation
as incomplete and keep UI acceptance blocked; code approval alone is insufficient.
Do not describe an implementer's screenshot inspection as independent visual review.
For blocking visual findings, provide fresh renders of the corrected result in the
focused recheck. Keep the existing read-only restrictions and human approval gates.

## Keep one reviewer conversation per Codex conversation

Use [Invoke-ClaudeReview.ps1](scripts/Invoke-ClaudeReview.ps1) from the same trusted workspace root for every review in this Codex conversation. The script keys an ignored local state file by `CODEX_SESSION_ID`: its first successful call creates a Claude session and later calls resume that session. A new Codex conversation gets a new Claude reviewer session. Never resume a user's interactive Claude/VS Code session for this workflow, and never run two calls to the reviewer session concurrently.

The script discovers the newest installed Claude Code VS Code executable, checks that the existing `claude.ai` subscription login is active, and uses that login in place. It does not copy, export, or print auth files or tokens. Keep the ordinary `HOME`, `USERPROFILE`, and Claude config directory; do not set provider credential overrides, use `--bare`, or create a disposable Claude profile. If authentication is missing or expired, report that once rather than asking the user to sign in for each review.

For this long-lived reviewer conversation, the launcher sets Claude Code's
`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=60` in the child process only. It does not
change global Claude settings or the user's interactive sessions. Existing
reviewer context above 60% may compact on a later review turn; this does not
create a new reviewer session.

The launcher also passes `--effort low` on every review call, including resumed
sessions, to reduce quota use. This changes only the review call's effort, not
its model, read-only permissions, or requirement to state uncertainty and an
explicit verdict.

Claude needs provider network access for the review turn. If the calling tool context blocks that connection, run the same script in an authorized network-enabled context with the same OS profile and state directory. Do not respond by copying the login or starting a different reviewer session.

Write a prompt file in the trusted workspace, then run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  '.\specs\shared\skills\claude-reviewer\scripts\Invoke-ClaudeReview.ps1' `
  -WorkspaceRoot 'C:\CodeWorkspace\agentviz' `
  -StateDirectory 'C:\CodeWorkspace\agentviz\claude-review.local\sessions' `
  -PromptFile 'C:\CodeWorkspace\agentviz\claude-review.local\prompt.txt'
```

Use equivalent absolute paths when this skill is used elsewhere. The per-process execution-policy override runs only this checked-in script and does not change machine settings. The state and prompt paths must be ignored by Git and remain outside tracked specifications. The state file contains only session identifiers, initialization status, and a pending prompt digest and transcript offset, never credentials or prompt text. The script confines Claude's tools to file reading, disables customizations and MCP servers, denies permission prompts, and times out after three minutes by default. It returns Claude's structured result on stdout; preserve a concise finding summary and the reviewed revision in the work handoff.

## Apply the review without micro-reviews

Request one full review of the PR's substantive own-diff. Check findings against source and tests, fix confirmed in-scope defects, and rerun affected checks. Request one focused recheck for each blocking finding. Request another full review only if the PR's own diff changes meaningfully, such as a logic change or roughly 20 or more changed lines; the line count is a cue, not a safe harbor for small security changes. Batch fixes before that recheck. If a blocker remains after its focused recheck, stop and resolve it with the human or a genuinely new substantive review, rather than repeating the same prompt.

Do not ask Claude to recheck nonblocking wording or BOM/encoding corrections in non-executable documents that it already suggested. Verify those with targeted content checks, `git diff --check`, and required CI. Encoding changes to scripts require parsing and relevant tests; request review if behavior may change. For a clean parent merge, compare the PR's own diff before and after with `git range-diff` or an equivalent patch comparison. If the own-diff is unchanged and there is no new interaction risk, record that evidence and use final-head CI without another review. Review a changed resolution or new interaction risk. Preserve the last substantive reviewed revision, the later diff comparison, and the final tested head in the handoff.

Explain rejected or out-of-scope findings with evidence. A clean review supports the reviewed change, not every future edit. Keep issue-edit, configuration, publication, and merge approval rules in force. An independent review is not human approval and does not waive a pause for a recommendation that conflicts with the human's interests or instructions.

On a timeout, native error, or quota refusal, do not blindly resubmit the same prompt. The launcher stores a prompt digest and transcript offset before starting Claude. It first attempts to recover a completed, non-error answer written after that offset in the same local session transcript. If none exists, treat the request as uncertain and stop. Inspect the transcript before passing `-ResolvePendingSha256 <matching digest>` to explicitly abandon that pending request and send the chosen next prompt. This switch is not an approval or a retry shortcut; it records the decision to stop waiting for the earlier result. Never create a new reviewer session just to retry.
