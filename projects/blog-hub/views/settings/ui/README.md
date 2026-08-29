# Settings UI

Derived written layout index: [Settings view](../layout.md)

The sole authority is [settings.drawio](../settings.drawio), with one page for
each top-level Settings state. The platform-login component workshop appears below
the full screen on the Platforms page. The corresponding source screenshots are
stored in `references/`.

| ID | Page |
|---|---|
| `SETTINGS-PAGE-PLATFORMS` | Platforms |
| `SETTINGS-PAGE-AI-PROVIDERS` | AI Providers |
| `SETTINGS-PAGE-ACCOUNT` | Account |

Connection-card behavior is maintained as a view-owned component:

| ID | Component |
|---|---|
| `SETTINGS-PLATFORM-LOGIN` | [Platform login card](components/platform-login-card/README.md) |
| `SETTINGS-AI-PROVIDER-TRANSITIONS` | [AI provider transitions](components/ai-provider-transitions/README.md) |

## Interaction markers

Amber `ST-*` badges in the Draw.io are the stable interaction IDs;
[interactions.md](../interactions.md) is their searchable projection.
User-triggered state edges repeat the triggering ID; `SYSTEM` labels identify browser
handoff, polling, credential validation, and background synchronization. Regenerate the
managed annotations with `python3 tools/generate_bloghub_interaction_markers.py`.
