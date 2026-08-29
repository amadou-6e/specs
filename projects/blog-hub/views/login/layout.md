# Login View — Layout

> Design blocked: no authoritative `login.drawio` exists. Treat the layout below as
> historical planning input only.

## Purpose

Entry point for all unauthenticated users. Serves both login and registration.
No navigation bar. No sidebar. Single focused task.

---

## Zones

```
┌─────────────────────────────────────────────────────┐
│  Surface background (#0f1117) — full viewport        │
│                                                       │
│         ┌────────────────────────────┐               │
│         │  Logo / branding strip     │  (top, center)│
│         ├────────────────────────────┤               │
│         │  Auth card                 │  (center)     │
│         │  ┌──────────────────────┐  │               │
│         │  │  Tab row (Login /    │  │               │
│         │  │         Register)    │  │               │
│         │  ├──────────────────────┤  │               │
│         │  │  Form fields         │  │               │
│         │  ├──────────────────────┤  │               │
│         │  │  Primary action btn  │  │               │
│         │  ├──────────────────────┤  │               │
│         │  │  Switch link         │  │               │
│         │  └──────────────────────┘  │               │
│         └────────────────────────────┘               │
│                                                       │
└─────────────────────────────────────────────────────┘
```

## Grid

- Full viewport height, flexbox column, align center, justify center
- Auth card: fixed width 400px, no horizontal scroll
- Card padding: 32px

## Responsive

- Below 480px: card fills full width with 16px horizontal margin
- No horizontal scroll at any width

## Scroll model

- Page does not scroll. Everything fits in viewport height.
- If device is very short (< 600px), card may scroll internally (form fields only)

## Fixed vs scrolling regions

- Background: fixed, covers full viewport
- Card: fixed height in normal use, scrollable internally on very short screens
