# Login View — Components

---

## 1. BrandMark

**Responsibility:** Identifies the app above the auth card.

**Inputs:** None (static)

**Variants to explore:**
- A: Logo icon + "BlogHub" wordmark, stacked vertically, centered
- B: Logo icon + wordmark inline (horizontal), centered
- C: Wordmark only (no icon), large, centered
- D: Icon only (no text), large, centered

---

## 2. AuthCard

**Responsibility:** Outer container for the entire auth flow. Holds the tab row, form, and footer link.

**Inputs:** `mode` (login | register)

**Variants to explore:**
- A: Bordered panel (border #252a38, bg #181c27, radius 8px, shadow via border elevation)
- B: Floating card with subtle glow border on the accent color
- C: Borderless, blends into surface with soft inner background shift only
- D: Split card: left decorative panel, right form panel

---

## 3. TabRow

**Responsibility:** Toggle between Login and Register modes within the same card. Replaces the active form without a page reload.

**Inputs:** `active` (login | register), `onSwitch` callback

**Variants to explore:**
- A: Underline tabs (active tab has accent bottom border, text goes bright)
- B: Pill segment control (active option has accent bg fill)
- C: Two full-width ghost buttons, active one has accent border
- D: No tabs — a text link below the button ("No account? Register") instead

---

## 4. FormField

**Responsibility:** Labeled input for email or password. Shows validation error inline.

**Inputs:** `label`, `type` (email | password), `value`, `error` (string | null), `placeholder`

**Variants to explore:**
- A: Label above input, error message below in red, input border turns red on error
- B: Floating label (label animates up when field is focused or filled)
- C: Label left-aligned, input right-aligned (horizontal layout, 40% / 60% split)
- D: Label above, input has icon on left (envelope for email, lock for password)

**Password field extras:**
- Show/hide toggle (eye icon) on the right edge of the input
- Always present regardless of variant chosen

---

## 5. RememberMe (login mode only)

**Responsibility:** Checkbox to extend session TTL from 1 hour to 30 days.

**Inputs:** `checked`, `onChange`

**Variants to explore:**
- A: Checkbox + "Remember me for 30 days" label, left-aligned, below password field
- B: Toggle switch + label, right-aligned
- C: Checkbox + label with a tooltip icon explaining the TTL difference
- D: Not visible by default, appears only after a failed login (progressive disclosure)

---

## 6. PrimaryButton

**Responsibility:** Submit the active form (login or register).

**Inputs:** `label` (string), `loading` (bool), `disabled` (bool)

**Variants to explore:**
- A: Full-width, accent fill, white text, radius 6px, spinner replaces label on loading
- B: Full-width, accent border only (ghost), text in accent color, fills on hover
- C: Fixed width centered, accent fill
- D: Full-width, accent fill with an arrow icon on the right

---

## 7. ErrorBanner

**Responsibility:** Surface API-level errors (wrong password, email taken, server error) that are not tied to a specific field.

**Inputs:** `message` (string | null)

**Variants to explore:**
- A: Red-tinted banner at the top of the card (above the form), icon + message
- B: Inline between the button and the switch link, no background, just red text + icon
- C: Shake animation on the card + brief red border flash, message appears below button
- D: Toast notification, appears top-right, auto-dismisses after 5s
