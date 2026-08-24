# Publish / Schedule — UI Tests Spec

---

## Destination rows

- [ ] Only destinations with existing drafts are shown
- [ ] Destinations with errors are shown but unchecked and non-interactive
- [ ] Error reason text is visible on the disabled row
- [ ] "Fix" link on error row navigates to /inspect/:id
- [ ] Checking a destination enables the publish mode toggle
- [ ] Unchecking a destination hides the mode toggle and clears any scheduled time

---

## Publish mode toggle

- [ ] Default mode is "Now"
- [ ] Switching to "Scheduled" shows the date/time picker inline below the row
- [ ] Switching back to "Now" hides the picker and clears the scheduled time
- [ ] Date picker does not allow selecting a time in the past
- [ ] Date picker does not allow selecting a time within 10 minutes of now
- [ ] Timezone label is displayed next to the time input

---

## Confirm summary

- [ ] Summary appears as soon as at least one destination is checked
- [ ] Summary updates in real time when modes or times change
- [ ] Prose is grammatically correct for 1, 2, and 3 destination combinations

---

## Action bar

- [ ] Confirm button is disabled when no destinations are checked
- [ ] Confirm button enables when at least one destination is checked and valid
- [ ] Scheduled destination with no time selected keeps Confirm disabled
- [ ] Clicking Confirm shows spinner and "Publishing…" label
- [ ] Back link is disabled while publishing is in flight

---

## Post-publish outcome

- [ ] Outcome screen replaces form content (no page reload)
- [ ] Published destinations show green status and "View on [platform]" link
- [ ] Scheduled destinations show date/time of scheduled publish
- [ ] Skipped/failed destinations show reason text
- [ ] "Back to overview" navigates to /
- [ ] "View article" opens first published URL in new tab
- [ ] If all destinations failed: Outcome screen shows error state with "Retry" option

---

## Edge cases

- [ ] All destinations have errors: Confirm is disabled, explanation shown above action bar
- [ ] Publishing completes partially (some succeed, some fail): Outcome screen shows mixed results
- [ ] Session expires mid-publish: redirect to /settings with "Session expired" banner
