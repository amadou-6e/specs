# Agent Service

## What It Does

Drives all AI-powered content operations: initial article generation from a user brief,
re-generation passes over existing content, and patch generation in response to inline
comments. Spawns a subprocess for each model invocation (Claude or Codex CLI) and
exposes every long-running operation as an async job tracked by `GET /api/jobs/{jobId}`.

Web search is **not** a backend HTTP endpoint. It is a built-in tool of the Claude /
Codex CLIs; the agent service simply enables it via the CLI flag when the user's
connection settings allow it.

---

## Main Features

| Feature | Description |
|---------|-------------|
| Article generation | Accepts a brief, skill, provider, word-count, and optional context file; spawns CLI; returns a new `article_id` + `jobId`. |
| Article regeneration | Re-runs a generation pass on an existing article's body (triggered from editor CLI `regenerate`). |
| Patch generation | Generates diff patches in response to an unresolved comment (triggered by "Fix with AI" in Comments panel). |
| Provider dispatch | Selects `claude` or `codex` subprocess based on `provider` field; validates credential exists in Connections store before spawning. |

---

## Dependencies

| Dependency | Why |
|------------|-----|
| `connections` service | Check that the requested provider credential is present before spawning CLI. |
| `articles` service / store | Create article record (generation), read body (regeneration), write back updated body. |
| `comments-patches` service / store | Write generated patches back to the article's patch list. |
| `jobs` service | Register and update the async job record polled by the frontend. |

---

## File Tree (planned)

```
backend/
  routers/
    agent.py           # POST /api/agent/generate, /regenerate, /generate-patch
  services/
    agent_service.py   # business logic: prompt assembly, CLI dispatch, job wiring
  subprocess/
    cli_runner.py      # helpers for spawning Claude/Codex CLI subprocesses
  store/
    memory.py          # articles + patches store (shared with articles service)
```

---

## Execution Pattern

```
POST /api/agent/generate
  │
  ├─ Validate: connections store has provider credential
  ├─ Create blank Article record → article_id
  ├─ Register Job record (status=running)
  ├─ Assemble prompt (brief + skill system-prompt + context file content)
  ├─ Spawn CLI subprocess (async)
  │     CLI stdout → stream body chunks → write to Article.body on complete
  │     CLI exit 0  → Job status=done, Article.wordCount recalculated
  │     CLI exit ≠0 → Job status=error, Job.error = stderr excerpt
  └─ Return 202 { jobId, article_id }

POST /api/agent/regenerate/{article_id}
  │
  ├─ Read Article.body from store
  ├─ Register Job record (status=running)
  ├─ Spawn CLI subprocess with existing body + regeneration system-prompt
  │     On complete → write new body, recalculate wordCount, re-run gate check
  └─ Return 202 { jobId }

POST /api/agent/generate-patch/{article_id}/comments/{comment_id}
  │
  ├─ Read Comment.text and Comment.anchor from store
  ├─ Register Job record (status=running)
  ├─ Spawn CLI with targeted fix prompt (comment text as instruction, anchor as context)
  │     On complete → write Patch record { removed, added, state=pending }
  │     Mark Comment.hasPatch = true
  └─ Return 202 { jobId }
```

---

## Dataflow

![Agent dataflow diagram](https://mermaid.ink/img/Zmxvd2NoYXJ0IExSCiAgRkVbIkZyb250ZW5kCkNyZWF0ZS1hcnRpY2xlIHdpemFyZCAvCkVkaXRvciBDTEkgcGFuZWwiXQogIEFHWyJBZ2VudCBSb3V0ZXIKL2FwaS9hZ2VudC8uLi4iXQogIENTWyJDb25uZWN0aW9ucyBTdG9yZSJdCiAgSlNbIkpvYnMgU2VydmljZSJdCiAgQ0xJWyJDbGF1ZGUgLyBDb2RleApDTEkgc3VicHJvY2VzcyJdCiAgQVNbIkFydGljbGVzIFN0b3JlIl0KICBQU1siUGF0Y2hlcyBTdG9yZSJdCgogIEZFIC0tPnwiUE9TVCAvZ2VuZXJhdGUifCBBRwogIEFHIC0tPnwiY2hlY2sgY3JlZGVudGlhbCJ8IENTCiAgQUcgLS0-fCJyZWdpc3RlciBqb2IifCBKUwogIEFHIC0tPnwic3Bhd24ifCBDTEkKICBDTEkgLS0-fCJib2R5IHRleHQifCBBUwogIENMSSAtLT58ImRpZmYgcGF0Y2gifCBQUwogIEpTIC0tPnwiam9iIGRvbmUifCBGRQ==)

---

## UML Class Diagram

![Agent class diagram](https://mermaid.ink/img/Y2xhc3NEaWFncmFtCiAgY2xhc3MgR2VuZXJhdGVSZXF1ZXN0IHsKICAgICtzdHIgcHJvbXB0CiAgICArc3RyIHNraWxsCiAgICArc3RyIHByb3ZpZGVyCiAgICAraW50IHdvcmRfY291bnQKICAgICtsaXN0IGRlc3RpbmF0aW9ucwogICAgK3N0ciBjb250ZXh0X3RleHQKICB9CiAgY2xhc3MgUmVnZW5lcmF0ZVJlcXVlc3QgewogICAgK3N0ciBhcnRpY2xlX2lkCiAgICArc3RyIHByb3ZpZGVyCiAgfQogIGNsYXNzIEdlbmVyYXRlUGF0Y2hSZXF1ZXN0IHsKICAgICtzdHIgYXJ0aWNsZV9pZAogICAgK3N0ciBjb21tZW50X2lkCiAgICArc3RyIHByb3ZpZGVyCiAgfQogIGNsYXNzIEFnZW50U2VydmljZSB7CiAgICArZ2VuZXJhdGUoR2VuZXJhdGVSZXF1ZXN0KSBBc3luY0pvYgogICAgK3JlZ2VuZXJhdGUoUmVnZW5lcmF0ZVJlcXVlc3QpIEFzeW5jSm9iCiAgICArZ2VuZXJhdGVfcGF0Y2goR2VuZXJhdGVQYXRjaFJlcXVlc3QpIEFzeW5jSm9iCiAgICAtX2J1aWxkX3Byb21wdChicmllZiwgc2tpbGwsIGNvbnRleHQpIHN0cgogICAgLV9zcGF3bl9jbGkocHJvdmlkZXIsIHByb21wdCkgQ0xJUHJvY2VzcwogICAgLV93cml0ZV9hcnRpY2xlKGFydGljbGVfaWQsIGJvZHkpIHZvaWQKICAgIC1fd3JpdGVfcGF0Y2goYXJ0aWNsZV9pZCwgY29tbWVudF9pZCwgcmVtb3ZlZCwgYWRkZWQpIHZvaWQKICB9CiAgY2xhc3MgQ0xJUnVubmVyIHsKICAgICtydW5fYXN5bmMoY21kKSBBd2FpdGFibGUKICAgICtjbGF1ZGVfY21kKHByb21wdCwgZmxhZ3MpIGxpc3QKICAgICtjb2RleF9jbWQocHJvbXB0LCBmbGFncykgbGlzdAogIH0KCiAgQWdlbnRTZXJ2aWNlIC0tPiBDTElSdW5uZXIKICBBZ2VudFNlcnZpY2UgLS0-IEdlbmVyYXRlUmVxdWVzdAogIEFnZW50U2VydmljZSAtLT4gUmVnZW5lcmF0ZVJlcXVlc3QKICBBZ2VudFNlcnZpY2UgLS0-IEdlbmVyYXRlUGF0Y2hSZXF1ZXN0)
