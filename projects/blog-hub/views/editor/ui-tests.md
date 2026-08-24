# Editor — UI Tests Spec

---

## Mode switching

- [ ] Default mode on load is Write
- [ ] Clicking "Review" switches to Review mode (margin panel appears, comment anchors visible)
- [ ] Switching back to Write hides the margin panel without losing comment data
- [ ] Mode toggle state persists on page refresh (localStorage)

---

## Editor content

- [ ] Headings render with correct visual hierarchy (H1 > H2 > H3)
- [ ] Code blocks render with syntax highlighting and language label
- [ ] Code block copy button appears on hover and copies content to clipboard
- [ ] Images render inline with correct aspect ratio
- [ ] Blockquotes render with left border accent

---

## Autosave

- [ ] Unsaved indicator (amber dot) appears immediately on first edit
- [ ] Autosave triggers 2 seconds after last keystroke
- [ ] Amber dot disappears after successful save confirmation from API
- [ ] If save fails: dot stays amber, tooltip shows "Save failed — retrying"

---

## Write mode toolbar

- [ ] Bold applies `**` markdown around selected text
- [ ] Inline code applies `` ` `` around selected text
- [ ] Code block inserts fenced block at cursor position with language field focused
- [ ] Heading dropdown applies correct heading level to current line
- [ ] Link action prompts for URL and wraps selected text in markdown link

---

## Review mode: comments

- [ ] "Add Comment" activates selection mode (cursor changes to crosshair)
- [ ] Selecting text in selection mode creates a comment anchor (amber underline)
- [ ] A new comment thread appears in the margin panel anchored to the selection
- [ ] Hovering a comment thread highlights the anchored text in the editor
- [ ] "Resolve" collapses the thread with a "Resolved" label
- [ ] Resolved threads can be expanded again
- [ ] "Fix with AI" on a comment triggers a patch request (spinner shown in thread)

---

## AI patches

- [ ] Accepted patch replaces editor content at the correct range
- [ ] Rejected patch is removed from the panel; the original comment stays open
- [ ] Diff view shows red for removed lines, green for added lines
- [ ] Accepting a patch updates the unsaved indicator

---

## Generation progress overlay

- [ ] Overlay appears immediately after navigating from /create while job is running
- [ ] Progress stages update: Outlining, Writing, Reviewing
- [ ] On generation complete: overlay dismisses and editor content is populated
- [ ] Navigating away while generating shows a confirmation prompt ("Generation in progress. Leave anyway?")
- [ ] On generation error: error message shown with Retry and Start over options

---

## Destinations panel (margin)

- [ ] Each configured destination shows with current status pill
- [ ] Draft URL link is clickable and opens in new tab
- [ ] Error reason text is shown for failed destinations
- [ ] "Run inspection" navigates to /inspect/:id

---

## Top nav actions

- [ ] Inspect button navigates to /inspect/:id
- [ ] Publish button is disabled when gate result is "fail"
- [ ] Publish button is disabled when no destinations are configured
- [ ] Back arrow navigates to / (overview) with confirmation if unsaved changes exist
- [ ] Article title is inline editable; saving updates the article title via PATCH

---

## Tablet layout

- [ ] Margin panel is not visible at 768px by default
- [ ] "Comments" button in toolbar opens the margin panel as a slide-in drawer
- [ ] Drawer closes on overlay click or Escape key
