# Login - State Diagram Index

The `LOGIN · AUTHORITATIVE LIFECYCLE` region in [login.drawio](login.drawio) is the sole
authority. This file is a searchable projection.

| State | Draw.io behavior |
|---|---|
| Session check | Redirects an existing valid session to Overview |
| Sign in | Email, password, session duration, and submission controls |
| Register | Email and password account creation controls |
| Submitting | Active auth request; duplicate submission disabled |
| Overview | Successful cookie-backed session destination |
| Recoverable error | Field or API feedback remains in the auth card |

No social-login control is represented. Adding one requires a Draw.io-first change.
