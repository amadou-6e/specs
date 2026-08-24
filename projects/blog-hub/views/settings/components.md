# Settings — Components Spec

---

## SettingsNav

Vertical nav list in Zone B.

### Props
- `sections: { id: string, label: string }[]`
- `active: string`
- `onChange: (id: string) => void`

### Item states
- Active: left indigo border, bright label
- Inactive: muted label, no border

---

## PlatformCard

One card per publishing destination (Medium, Hashnode, Dev.to).

### Props
- `platform: 'medium' | 'hashnode' | 'devto'`
- `status: 'connected' | 'expired' | 'not_connected'`
- `connectedAt: string | null`
- `expiresAt: string | null`
- `onConnect: () => void`
- `onReconnect: () => void`
- `onDisconnect: () => void`
- `onTest: () => void`

### States

**Connected:**
- Green status badge
- "Connected [date]" label
- "Test connection" secondary button (confirms session alive)
- "Disconnect" danger link (requires confirmation)

**Expired:**
- Amber status badge + expiry date
- "Reconnect" primary button

**Not connected:**
- Muted status badge
- "Connect" primary button

### Connect/Reconnect auth model per platform
- **Medium:** browser-based session (MCP import flow or guided cookie entry)
- **Hashnode:** API key input field
- **Dev.to:** API key input field

After connection: card updates to Connected state without page reload.

---

## CliProviderCard

One card per AI CLI provider (Claude, Codex). These are CLI tools run locally,
not cloud API endpoints. Auth is separate from a raw API key.

### Props
- `provider: 'claude' | 'codex'`
- `status: 'authenticated' | 'not_authenticated' | 'testing'`
- `identity: string | null`   — e.g. "user@example.com" or org name shown after auth
- `cliVersion: string | null` — e.g. "claude 1.0.2" or "codex 0.1.0"
- `onLogin: () => void`       — runs the CLI login flow (browser OAuth or key entry)
- `onLogout: () => void`
- `onTest: () => void`

### Auth model per provider
- **Claude CLI:** `claude` binary on PATH. Auth via browser OAuth (`claude auth login`).
  After login the CLI stores a session token locally. BlogHub detects auth by running
  `claude --version` and checking for a valid session.
- **Codex CLI:** `codex` binary on PATH. Auth via OpenAI API key stored in environment
  or keychain. BlogHub prompts for the key and stores it.

### States

**Authenticated:**
- Green badge + identity string
- CLI version shown in muted mono below name
- "Test" button: runs a short generation ping, shows inline result
- "Log out" danger link

**Not authenticated:**
- Muted badge
- One-line explanation of what this CLI enables
- "Log in" primary button (Claude: opens browser OAuth, Codex: shows key input inline)

**Testing:**
- Spinner inside card while ping is in flight

---

## ApiKeyInput

Reusable secure text input for API keys and tokens.

### Props
- `value: string`
- `onChange: (v: string) => void`
- `placeholder: string`
- `label: string`

### Behaviour
- `type="password"` by default
- Show/hide toggle (eye icon) on the right
- Does not autocomplete (`autocomplete="off"`)

---

## ConnectionTestResult

Inline result shown after a "Test" or "Test connection" action.

### Props
- `status: 'idle' | 'testing' | 'success' | 'error'`
- `detail: string | null` — model name or CLI response on success, error reason on failure

### States
- idle: nothing rendered
- testing: spinner + "Testing…"
- success: green check + detail string
- error: red cross + error reason

---

## ConfirmDialog

Inline confirmation shown before destructive actions (Disconnect, Log out, Remove key).

### Props
- `message: string`
- `confirmLabel: string`
- `onConfirm: () => void`
- `onCancel: () => void`

Renders inline below the trigger element, not as a modal overlay.
