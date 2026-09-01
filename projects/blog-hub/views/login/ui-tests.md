# Login - UI Tests Spec

> Test authority: [login.drawio](login.drawio). Tests project its represented states and
> `LI-*` transitions; they must not create new UI requirements.

## Session entry

- [ ] A successful session check redirects directly to Overview.
- [ ] A `401` session check leaves the Sign in card available.

## Authentication card

- [ ] `LI-01` and `LI-05` switch between Sign in and Register without navigation.
- [ ] `LI-02` toggles password masking without changing the value.
- [ ] `LI-03` selects the 30-day session duration.
- [ ] `LI-04` and `LI-06` enter Submitting and prevent duplicate submission.
- [ ] Structured validation errors mark the responsible field.
- [ ] Authentication and server errors remain visible inside the card.
- [ ] `LI-07` preserves entered values while returning to editable form state.
- [ ] Successful sign-in or registration opens Overview using the server session cookie.

## Responsive behavior

- [ ] The 580 px card remains centred on desktop.
- [ ] Below 480 px, the card fits with 16 px page margins and no horizontal scrolling.
- [ ] On short viewports, only the form region scrolls.
