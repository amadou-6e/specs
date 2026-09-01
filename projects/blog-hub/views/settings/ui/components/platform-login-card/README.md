# Platform login card

Canonical source: [Settings Draw.io, page `Settings · Platforms`](../../../settings.drawio)

| ID | State |
|---|---|
| `PLATFORM-LOGIN-01` | Disconnected |
| `PLATFORM-LOGIN-02` | Hashnode method choice |
| `PLATFORM-LOGIN-03` | Waiting for browser sign-in |
| `PLATFORM-LOGIN-04` | Saving and verifying |
| `PLATFORM-LOGIN-05` | Connected with background synchronization |
| `PLATFORM-LOGIN-06` | Login failed |

Provider-state screenshots are in `references/states/`. Run `python3 generate.py` from
this directory to regenerate only the managed component-workshop section beneath the
Platforms screen. Generated comparison exports are temporary and are not tracked. The
generator does not depend on backup files.
