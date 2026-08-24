# Settings — UI Tests Spec

---

## Settings nav

- [ ] Default active section is "Platforms"
- [ ] Clicking a nav item switches the section content without page reload
- [ ] Active item has left border accent and bright label
- [ ] On mobile: section selector renders as a dropdown, not a sidebar

---

## Platform cards

- [ ] Connected platform shows green badge and connected date
- [ ] Expired platform shows amber badge and expiry date
- [ ] Not connected platform shows muted badge
- [ ] "Connect" button is the only action shown for not_connected state
- [ ] "Reconnect" is primary and "nothing else" for expired state
- [ ] "Disconnect" is a danger link requiring confirmation dialog before acting
- [ ] Confirming disconnect reverts card to not_connected state without page reload
- [ ] Cancelling disconnect leaves the card unchanged
- [ ] "Test" button on connected card shows testing spinner then inline result
- [ ] Test success shows green check + connection detail
- [ ] Test failure shows red cross + reason

---

## AI provider cards

- [ ] Unconfigured provider shows password input and Save button
- [ ] Save button is disabled when input is empty
- [ ] Saving a key masks it and shows the configured state without page reload
- [ ] Masked key is displayed (not editable inline; must remove and re-add)
- [ ] Show/hide toggle reveals and hides the masked key value
- [ ] "Remove" requires confirmation before clearing the key
- [ ] "Test connection" on a configured provider shows spinner then inline result
- [ ] Test success displays the connected model name
- [ ] Test failure displays the API error reason

---

## Account section

- [ ] Display name field is editable and saves on blur or Enter
- [ ] Email field is read-only
- [ ] "Sign out" shows a confirmation prompt before signing out
- [ ] Cancelling sign out leaves the user on the settings page

---

## Edge cases

- [ ] Connecting a platform that fails mid-flow: card stays in previous state, error toast shown
- [ ] Saving an invalid API key: inline error shown on the card, not a toast
- [ ] Two provider cards are always shown (Claude and Codex) regardless of configuration state
