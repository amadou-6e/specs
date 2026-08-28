# Settings UI

Written specification: [Settings view](../layout.md)

The canonical geometry is [settings.drawio](../settings.drawio), with one page for
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
