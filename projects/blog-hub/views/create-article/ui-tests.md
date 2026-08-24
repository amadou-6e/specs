# Create Article — UI Tests Spec

---

## Step indicator

- [ ] Step 1 is active on page load; steps 2 and 3 are future state
- [ ] Completing step 1 and clicking Next shows step 1 as past (checkmark), step 2 as active
- [ ] Clicking a past step indicator navigates back to that step without data loss

---

## Step 1: Prompt

- [ ] Textarea is focused on page load
- [ ] Suggested prompt chips are visible when textarea is empty
- [ ] Clicking a chip populates the textarea with the chip text
- [ ] Chips disappear once the textarea has content
- [ ] Textarea grows vertically as content is added, up to 400px
- [ ] Character count appears after 200 characters
- [ ] Next button is disabled when prompt is empty
- [ ] Next button enables when at least one character is entered

---

## Step 2: Configure

- [ ] Only one SkillCard can be selected at a time
- [ ] Clicking a selected SkillCard does not deselect it (selection is required)
- [ ] Provider with missing API key shows warning icon
- [ ] Clicking "Reconnect" on a provider navigates to /settings (new tab or inline flow TBD)
- [ ] WordCountSlider snaps to defined breakpoints
- [ ] Current word count value is readable at all slider positions

---

## Step 3: Destinations

- [ ] At least one destination must be selected to enable Generate
- [ ] Platform with expired session shows amber warning and disabled checkbox
- [ ] "Reconnect" link on expired platform is clickable
- [ ] Unconfigured platform is visually muted and non-interactive
- [ ] Checking/unchecking destinations updates the ConfigSummaryPanel in real time

---

## Config summary panel

- [ ] Panel shows prompt excerpt updating as user types in step 1
- [ ] Panel reflects selected skill after step 2 selection
- [ ] Panel reflects selected destinations after step 3 interaction
- [ ] Panel is not visible at 768px viewport (tablet)

---

## Action bar

- [ ] Back button is not visible on step 1
- [ ] Back button is visible on steps 2 and 3
- [ ] Clicking Back navigates to previous step without clearing data
- [ ] Generate button is disabled when no destinations are selected
- [ ] Clicking Generate with valid inputs triggers generation (spinner appears, Back disabled)
- [ ] On generation success: navigates to /article/:id
- [ ] On generation failure: error banner appears above action bar with reason text
- [ ] Error banner has a retry action that re-triggers generation

---

## Edge cases

- [ ] Refreshing mid-wizard: if browser restore is not supported, returns to step 1 (data cleared, no crash)
- [ ] All platforms expired: Generate is disabled, warning shown prompting user to reconnect at least one
- [ ] Very long prompt (>2000 chars): textarea scrolls, no layout overflow
