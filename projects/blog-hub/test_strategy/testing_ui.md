# UI Testing Strategy — blog-hub

> Living design document for the `tests/tests_ui/` test suite.  
> Update this file whenever a new screen, pillar, or run mode is added.

---

## 1. Purpose and Scope

The `tests/tests_ui/` tree validates the browser-side experience of blog-hub across
three orthogonal concerns:

| Concern | Question answered |
|---------|-------------------|
| **Visual correctness** | Does every screen look right in every supported state? |
| **Remote fidelity** | Does the local render match what the upstream source publishes? |
| **Adversarial robustness** | Do unexpected click sequences cause hard crashes or silent JS errors? |

These tests are *human-reviewed* (screenshots) or *crash-only* (breaking paths).  
They do **not** assert pixel-exact values against a baseline — they produce artefacts
for a developer to inspect after a pull-request or deployment.

**Prerequisite:** A live server must be running on `http://localhost:8000` before any
test marked `browser`, `visual`, or `breaking` is executed.

---

## 2. Pillars

### 2.1 Visual Snapshots (`visual`)

Full-page and element-clipped screenshots captured from a live Playwright browser.
Each test navigates to a specific screen URL, drives the UI into a named state,
and calls `snap()` or `snap_element()`.

**Markers required:** `@pytest.mark.visual`, `@pytest.mark.browser`

**Screens implemented:**

| Folder | Visual test file | Breaking test file | Screen URL | Key visual states |
|--------|------------------|--------------------|------------|-------------------|
| `test_overview/` | `test_visual_overview.py` | `test_break_overview.py` | `overview/v3.html` | `empty_store`, `articles_loaded`, `card_close`, `create_menu_open` |
| `test_create_article/` | `test_visual_create_article.py` | `test_break_create_article.py` | `create-article/v1.html` | `step1_empty`, `step1_template_filled`, `step1_char_count`, `step2_default`, `step2_skill_selected`, `step3_default` |
| `test_import_article/` | `test_visual_import_article.py` | `test_break_import_article.py` | `import-article/v1.html` | `platform_step1/2/3`, `upload_step1_empty/drag/png/md` |
| `test_editor/` | `test_visual_editor.py` | `test_break_editor.py` | `editor/v2.html?id=art_001` | `loaded_default`, `panel_collapsed`, `destinations_open`, `chat_open`, `patches_open`, `unsaved_dot`, `word_count_visible` |
| `test_settings/` | `test_visual_settings.py` | `test_break_settings.py` | `settings/v2.html` | `platforms_tab_disconnected`, per-card close-ups, `ai_providers_tab`, key-input expanded, `medium_connected` |

**How to run (all visual):**
```bash
python -m pytest tests/tests_ui/ -m "visual and browser" -v -s
```

**How to run (single screen):**
```bash
python -m pytest tests/tests_ui/test_overview/ -m "visual and browser" -v -s
```

---

### 2.2 Remote Fidelity (`visual`)

Downloads remote assets (images, HTML pages) from their canonical upstream source,
saves them to `outputs/remote_dumps/`, then screenshots the *local* render of the
same component for side-by-side comparison.

**When to run:** After a platform's upstream design changes, or when a card/cover
component is updated locally.

**Test file:** `test_remote/test_remote_components.py`

**What it fetches:**
- `title.png` and `knowledge_graph.png` from the `blog-components` GitHub CDN
- Any additional asset declared as a `COMPONENT_SOURCES` entry in that file

**Failure behaviour:** If the CDN is unreachable the test calls `pytest.skip()` —
a network outage does not make CI red.

**Output paths:**
```
outputs/remote_dumps/images/<name>.<ext>    ← upstream asset
outputs/screenshots/<screen>/<state>.png    ← local render
```

Reviewer opens both images side by side to judge drift.

**Helpers used:** `fetch_remote_image()`, `fetch_remote_html()` from `utils/remote.py`

**How to run:**
```bash
python -m pytest tests/tests_ui/test_remote/ -m "visual and browser" -v -s
```

---

### 2.3 Breaking Paths (`breaking`)

Adversarial click sequences that a real user might accidentally trigger:
rapid repeated clicks, Next without a selection, pasting enormous text, navigating
away mid-flow, spamming toggles.

**Goal:** The page must remain *responsive* after every sequence — no white screen,
no frozen spinner, no unhandled exception hard-crash.  
JS errors are *captured and logged* (pytest warning) but do **not** fail the test
unless the page becomes unresponsive.

**Markers required:** `@pytest.mark.breaking`, `@pytest.mark.browser`

**Screen coverage** (each file lives in the same folder as the screen's visual tests):

| Folder | Breaking test file | Scenarios |
|--------|--------------------|-----------|
| `test_import_article/` | `test_break_import_article.py` | rapid Next no selection, multi-click after select, back at step1, unsupported→md recovery, upload spam, back-from-step3 re-advance |
| `test_create_article/` | `test_break_create_article.py` | Next with empty prompt, rapid Next/Back, whitespace template, step3 multi-back, template-btn spam |
| `test_editor/` | `test_break_editor.py` | missing `?id=`, bad article ID, accordion rapid toggle, navigate away unsaved, panel triple toggle, paste 50k chars |
| `test_settings/` | `test_break_settings.py` | save empty token, rapid tab switch, key expand/collapse spam, test-connection spam, disconnect while disconnected |
| `test_overview/` | `test_break_overview.py` | menu open then navigate, click card empty store, split menu rapid toggle, menu dismiss+reopen, import→browser back |

**Responsiveness check pattern:**
```python
def _responsive(page) -> bool:
    """Return True if the page JS can still execute."""
    try:
        return page.evaluate("() => document.readyState") == "complete"
    except Exception:
        return False
```

**Screenshot on exit:** Every breaking test saves a `<scenario>.png` to
`outputs/screenshots/breaking/<screen>/` so a developer can see the post-sequence
state at a glance.

**How to run (all breaking):**
```bash
python -m pytest tests/tests_ui/ -m "breaking and browser" -v -s
```

**How to run (single screen):**
```bash
python -m pytest tests/tests_ui/test_editor/ -m "breaking and browser" -v -s
```

---

### 2.4 Bridges

Cross-screen flows that verify navigation continuity between two adjacent screens.
These are regular `browser`-marked tests — not visual, not breaking.

**Location:** `tests/tests_ui/test_bridges/` (standalone folder — bridges span two screens, so no single per-screen home)

**Files:**
- `test_overview_import_bridge.py` — overview → import-article → back → overview
- `test_settings_bridge.py` — settings → connected state → back to dashboard

---

### 2.5 Utilities

#### `utils/screenshots.py`

| Function | Signature | Description |
|----------|-----------|-------------|
| `snap` | `(page, screen, state) → Path` | Full-page PNG |
| `snap_element` | `(locator, screen, state) → Path` | Element-clipped PNG |
| `snap_states` | `(page, screen, states, *, settle_ms=200) → list[Path]` | Iterate a list of `(label, setup_fn)` pairs, screenshot after each |

All outputs go to `tests/tests_ui/outputs/screenshots/<screen>/<state>.png`.

#### `utils/remote.py`

| Function | Signature | Description |
|----------|-----------|-------------|
| `fetch_remote_image` | `(url, name, *, ext=None) → Path \| None` | Download image, save to `remote_dumps/images/` |
| `fetch_remote_html` | `(url, name) → Path \| None` | Fetch HTML page, save to `remote_dumps/html/` |

Both return `None` (never raise) on network failure — callers use `pytest.skip()`.

---

## 3. Output Directory Tree

```
tests/tests_ui/outputs/
├── screenshots/
│   ├── overview/
│   │   ├── empty_store.png
│   │   ├── articles_loaded.png
│   │   └── ...
│   ├── create_article/
│   ├── import_article/
│   ├── editor/
│   ├── settings/
│   └── breaking/
│       ├── overview/
│       ├── create_article/
│       ├── import_article/
│       ├── editor/
│       └── settings/
└── remote_dumps/
    ├── images/
    │   └── <name>.<ext>
    └── html/
        └── <name>.html
```

All output directories are created on first run — no manual `mkdir` needed.

---

## 4. Marker Catalog

| Marker | Meaning | Default run? | Requires |
|--------|---------|-------------|---------|
| `browser` | Any Playwright test (live server) | **excluded** | `localhost:8000` |
| `visual` | Screenshot-only, human inspection | **excluded** | live server + `browser` |
| `breaking` | Adversarial click paths | **excluded** | live server + `browser` |
| `integration` | External service calls (Medium API etc.) | **excluded** | API credentials |

Default `pytest` run (no `-m` flag) collects only unit tests — none of the above.

### Run commands

```bash
# All browser-dependent tests
python -m pytest tests/tests_ui/ -m browser -v

# All visual snapshots
python -m pytest tests/tests_ui/ -m "visual and browser" -v -s

# All breaking paths
python -m pytest tests/tests_ui/ -m "breaking and browser" -v -s

# Single screen — both strategies
python -m pytest tests/tests_ui/test_editor/ -m "browser or visual or breaking" -v -s

# Remote fidelity comparison
python -m pytest tests/tests_ui/test_remote/ -m "visual and browser" -v -s

# Everything in tests_ui
python -m pytest tests/tests_ui/ -m "browser or visual or breaking" -v -s
```

---

## 5. Screenshot Naming Convention

```
outputs/screenshots/<screen>/<state>.png
```

- **`screen`** — snake_case name matching the folder:
  `overview`, `create_article`, `import_article`, `editor`, `settings`, `remote`
- **`state`** — snake_case description of the UI state at time of capture:
  `step1_empty`, `card_hover`, `panel_collapsed`, `medium_connected`
- Breaking-path screenshots use `breaking/<screen>/<scenario>.png`

---

## 6. Authoring Guide

### Adding a new visual state

1. Open the relevant `<screen>/test_visual_<screen>.py`
2. Add a step inside `snap_states()` or add a standalone `snap()` call
3. Name the state descriptively — future readers must understand what they're looking at

### Adding a new breaking scenario

1. Open `<screen>/test_break_<screen>.py`
2. Write a `test_break_<scenario>` function with `@pytest.mark.breaking @pytest.mark.browser`
3. Set up JS error capture with `page.on("pageerror", ...)`
4. Perform the adversarial actions
5. Call `_responsive(page)` and assert it is `True`
6. Call `snap(page, "breaking/<screen>", "<scenario>")` at the end

### Adding a new screen

1. Create `tests/tests_ui/<screen>/` folder with an `__init__.py`
2. Create `<screen>/test_visual_<screen>.py` — import `snap`, `snap_states` from utils
3. Create `<screen>/test_break_<screen>.py` — import `snap`, `_responsive` pattern
4. Add the screen row to the screens table (section 2.1)
5. Add the screen sub-directory to the output tree (section 3)

### Remote fidelity — adding a new asset

1. Open `test_remote/test_remote_components.py`
2. Add an entry to `COMPONENT_SOURCES`:
   ```python
   COMPONENT_SOURCES = [
       ("https://raw.githubusercontent.com/.../title.png", "title", None),
       ("https://raw.githubusercontent.com/.../my_asset.png", "my_asset", None),  # ← new
   ]
   ```
3. The test will automatically download, save, and screenshot it on next run

---

## 7. Decision Log

| Decision | Rationale |
|----------|-----------|
| Screenshots over pixel-diff baselines | Baselines rot quickly during active UI development; human review is more resilient to minor style shifts |
| Breaking tests warn on JS errors rather than fail | A console warning should not block CI; a frozen page should |
| `fetch_*` helpers return `None` instead of raising | CDN outages must not make CI red; callers choose to skip or warn |
| `visual` marker excluded from default run | Screenshot tests are slow and require a live server; wrong environment = confusing failure |
| Output tree under `tests/tests_ui/outputs/` | Co-location with the test code makes artefacts easy to find; gitignore the directory to keep the repo clean |
