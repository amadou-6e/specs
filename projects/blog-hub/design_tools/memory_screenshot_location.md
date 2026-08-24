---
name: screenshot-location
description: Where to save design tool screenshots during development
metadata:
  type: feedback
---

Always save design tool screenshots to `.spec/design_tools/` (not the repo root).

**Why:** User explicitly requested this to keep tool-related artifacts organized alongside the tools themselves.

**How to apply:** When using Playwright `browser_take_screenshot` for layout/design tool work, use filenames like `.spec/design_tools/layout-lshape.png` etc.
