# Settings - State Diagram Index

[settings.drawio](settings.drawio) is the sole authority. The Platforms, AI Providers,
and Account pages contain their complete editable geometry. Platform connection states
are represented by `BLOG PLATFORM LOGIN CARDS · VERIFIED STATES` and `CORE STATE
TRANSITIONS`; AI connection states are represented by `AI PROVIDER CONNECTIONS · STATE
TRANSITIONS`.

This Markdown file is only a searchable projection and must not introduce a state or
maintenance action absent from the Draw.io.

## Platform login cards

| State | Draw.io behavior |
|---|---|
| Disconnected | Hashnode opens method choice; Medium begins browser login directly |
| Method choice | Hashnode chooses Plus API token or free persistent-browser login |
| Waiting | Provider tab is open; user completes sign-in and closes it, or cancels |
| Verifying | BlogHub saves and verifies the profile with no card action available |
| Connected | Verified method is visible; sync starts automatically; Disconnect is the maintenance action |
| Failed | Explains failure and starts a fresh provider entry flow on Connect/Retry |

Successful connection queues an immediate durable import and a recurring 1-minute
schedule. Sync failure leaves the platform connected and retries as durable work.

## Connection health

The `CONNECTION HEALTH - SHARED PLATFORM LIFECYCLE` region applies to every
browser blog extension. A saved profile or cookie is a non-authoritative hint and
enters Verification stale. A live probe or successful remote operation enters
Connected. Authoritative failures enter Reauthentication required, Temporarily
blocked, Rate limited, Unavailable, or Unknown.

User-facing proof is fresh for five minutes. Connected blogs synchronize every
one minute, normally refreshing proof sooner; the idle verification target is
fifteen minutes. Settings requests one leased verification when stale. A
reauthentication result pauses remote jobs, while temporary failures retain their
schedule and resume at `retry_at`. Disconnect clears the health record.

## AI provider API-key path

| State | Draw.io behavior |
|---|---|
| Not configured | Choose browser login or `ST-21` Add API key |
| Key form | Enter a key, `ST-22` Save, or `ST-23` Cancel |
| Validating | Provider probe is in progress |
| Connected | Credential is encrypted and available to agents |
| Validation failed | Reason remains visible with key editing/retry available |

## AI provider browser paths

| Provider | Draw.io path |
|---|---|
| Anthropic | Start CLI login, paste loopback callback URL, `ST-26` Submit, then poll |
| OpenAI | Request device code, approve it in the provider browser, then poll |

Both paths converge on Connected or Login failed. Failure and timeout return through
`ST-20` Try again.

## AI provider maintenance

| State | Draw.io behavior |
|---|---|
| Testing | `ST-32` probes the current credential and remains connected after the result |
| Update key | `ST-33` opens key replacement and a valid `ST-22` save reconnects |
| Remove confirmation | `ST-34` opens; `ST-36` cancels or `ST-35` removes |
| Not configured | Removed provider is unavailable to agents |

The Account page currently defines navigation and account geometry but no independent
connection lifecycle.
