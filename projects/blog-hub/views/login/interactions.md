# Login - Interactions

[login.drawio](login.drawio) is the sole authority. This table is its searchable
interaction index.

| ID | Control | Result |
|---|---|---|
| `LI-01` | Sign in / Register segment | Switches auth mode without navigation |
| `LI-02` | Password visibility | Toggles masking without changing auth state |
| `LI-03` | Remember me | Selects the 30-day session TTL |
| `LI-04` | Sign in | Submits login and enters Submitting |
| `LI-05` | Auth mode link | Switches between Sign in and Register |
| `LI-06` | Create account | Submits registration and enters Submitting |
| `LI-07` | Edit / retry | Returns a recoverable error to editable form state |

Automatic session checks, responses, redirects, and validation use `SYSTEM` labels in
the Draw.io lifecycle.
