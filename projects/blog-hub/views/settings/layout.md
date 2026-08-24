# Settings — Layout Spec

## Purpose
One-time and occasional configuration: connecting publishing platforms, configuring AI providers, managing account.

---

## Page Zones

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE A: Top nav (fixed, 48px)                                  │
├──────────────────┬──────────────────────────────────────────────┤
│                  │                                              │
│  ZONE B:         │  ZONE C: Section content                    │
│  Settings nav    │  (scrollable, flex-1)                        │
│  (sticky, 200px) │                                              │
│                  │                                              │
└──────────────────┴──────────────────────────────────────────────┘
```

Split layout. Zone B is a vertical nav list. Zone C renders the selected section.

On mobile: Zone B collapses into a dropdown selector at the top of the page.

---

## Zone B: Settings nav sections

1. Platforms
2. AI Providers
3. Account

Active section has left border accent and bright label.

---

## Zone C: Platforms section

One card per supported platform (Medium, Hashnode, Dev.to).

Each card:
- Platform logo + name
- Connection status badge (Connected, Expired, Not connected)
- If connected: session health indicator, connected-at date, Disconnect button
- If expired: "Reconnect" primary button, expiry date shown
- If not connected: "Connect" primary button

Connect/Reconnect opens a browser session flow (either OAuth redirect or a guided manual cookie/token entry, depending on the platform).

---

## Zone C: AI Providers section

One card per provider (Claude, Codex).

Each card:
- Provider logo + name
- If configured: masked API key display, "Remove" button, "Test connection" button
- If not configured: API key input field + "Save" button
- Connection test result shown inline: "Connected — claude-opus-4-6" or error reason

---

## Zone C: Account section

- Display name field
- Email (read-only, shown for context)
- "Sign out" action (destructive, requires confirmation)
