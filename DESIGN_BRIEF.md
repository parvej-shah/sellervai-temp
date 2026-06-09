# Design System Brief — Sellervai

> **Your task:** Study this repository, then produce a **complete, production-ready design system** for Sellervai as a single drop-in `static/css/app.css` (plus any small Mako template edits needed to wire it). The output must build on the existing token + class architecture — do NOT introduce a new CSS framework, build step, or component library. Deliver tokens, components, and usage guidance specific to THIS app's screens.

---

## 1. What Sellervai is

Sellervai is a **B2B SaaS for small/mid store owners**. It connects a merchant's store to **WhatsApp, Facebook Messenger, Instagram, and Telegram**, and runs an **AI agent (DeepSeek + RAG)** that answers customers, recommends products, and helps close orders 24/7.

**Who uses it:** non-technical store owners, often in a multilingual / South-Asian-and-global SMB market. They keep the **dashboard open all day** during business hours. The design must feel **trustworthy, calm, and competent** — this tool handles their customers and their money. Avoid flashy "AI startup" gimmickry; favor clarity and confidence.

**Surfaces, in priority order:**
1. **Dashboard** (the real product) — conversations, orders, products, coupons, platform connection status, live HTMX status widgets. Data-dense, long-session. **Readability and calm win over saturation.**
2. **Store detail page** (`/stores/{id}`) — store config, products, coupons, orders, and platform connect/disconnect controls.
3. **Marketing homepage** + **auth pages** (login / register, incl. Google sign-in).

---

## 2. Tech constraints (read before designing)

- **CSS framework:** [Pico CSS v2](https://picocss.com/) loaded via CDN — semantic/classless, token-driven. We override it via CSS custom properties and a thin `.sv-*` class layer. **Keep using Pico's semantic elements and variables; do not replace it.**
- **Icons:** Tabler Icons webfont (`<i class="ti ti-xxx">`). Use Tabler icon names in examples.
- **Interactivity:** HTMX v2 (`hx-get`, `hx-swap`, `hx-trigger`). No React/Vue/build step. Components must be plain HTML+CSS that survives partial DOM swaps.
- **Templates:** Mako (`templates/*.html`) with inheritance from `base.html`. Pages override named defs: `nav_items`, `extra_head`, `extra_scripts`, `title`, `meta_description`.
- **Single stylesheet:** all custom styling lives in `static/css/app.css` (currently ~356 lines). Your deliverable replaces/extends this file.
- **Theme attribute:** `<html data-theme="dark">` is set in `base.html`. Pico reads `data-theme`. **You must support both light and dark.**

### Existing token layer (build ON this, keep the `--sv-*` prefix)
```css
:root {
  --sv-accent: #7c6aff; --sv-accent-hover: #6355e0;
  --sv-surface: #1a1a2e; --sv-surface-2: #16213e;
  --sv-border: rgba(255,255,255,.08); --sv-text-muted: rgba(255,255,255,.5);
  --sv-radius: 12px; --sv-transition: .2s ease;
}
```

### Existing component classes (preserve these names; restyle, don't rename)
`.sv-nav`, `.sv-brand`, `.sv-main`, `.sv-footer`, `.sv-hero`, `.sv-badge`, `.sv-hero-actions`, `.sv-hero-visual`, `.sv-hero-icon`, `.sv-section-title`, `.sv-feature-grid`, `.sv-feature-card`, `.sv-feature-icon`, `.sv-status-box`, `.sv-auth-wrap`, `.sv-auth-card`, `.sv-auth-header`, `.sv-auth-logo`, `.sv-google-btn-wrap`, `.sv-divider`, `.sv-form`, `.sv-form-error`, `.sv-optional`, `.sv-auth-footer`.

---

## 3. The chosen palette: **Indigo + Purple**

Brand identity = **indigo paired with purple**, not a single hue. They are the same family (indigo = purple shifted toward blue), used with distinct jobs:

- **Indigo = the workhorse.** Solid action color: primary buttons, links, focus rings, active states. Carries the *trust / reliable* signal — it's what users click 100×/day, so it must stay disciplined and solid.
- **Purple = the flourish.** Gradient end, hero headline accent, badges, AI-specific accents. Carries the *intelligent / AI* signal — used for brand moments, NOT for everyday controls.
- **The indigo→purple gradient** is the signature brand element. Use it sparingly: hero `<h1>` accent word, `.sv-badge`, brand logo icon, the single hero CTA, hover glow. Never on dense UI like table rows or form controls.

### Base brand tokens to anchor on
```css
:root {                /* light is the DEFAULT for daytime business use */
  --sv-indigo:        #5b5bf0;
  --sv-purple:        #a855f7;
  --sv-accent:        var(--sv-indigo);
  --sv-accent-hover:  #4848d6;
  --sv-accent-subtle: rgba(124,92,246,.10);
  --sv-gradient:      linear-gradient(135deg, #5b5bf0, #a855f7);
}
[data-theme="dark"] {
  --sv-indigo:        #7c7cff;
  --sv-purple:        #c084fc;
  --sv-accent:        var(--sv-indigo);
  --sv-accent-hover:  #9b9bff;
  --sv-accent-subtle: rgba(124,92,246,.14);
  --sv-gradient:      linear-gradient(135deg, #7c7cff, #c084fc);
}
```

---

## 4. What to deliver

Produce a **complete `static/css/app.css`** plus a short markdown **DESIGN_SYSTEM.md** documenting it. Cover ALL of the following.

### 4a. Full token system (light + dark, via `data-theme`)
- **Neutrals ramp:** page bg, card surface, raised surface, border, text, muted text — for BOTH themes. Light must be the comfortable default; dark must give cards real separation from the page.
- **Brand:** indigo, purple, gradient, accent, hover, subtle tint (from §3).
- **Semantic status colors** (light + dark): `--sv-success` (AI online / order paid), `--sv-warning` (token expiring / RAG out of sync), `--sv-danger` (webhook failed / disconnected), `--sv-info`. These must be visually distinct from the brand indigo/purple.
- **Platform brand colors** for connection chips: `--sv-whatsapp #25d366`, `--sv-messenger #0084ff`, `--sv-instagram #e1306c`, `--sv-telegram #229ed9`.
- **Scale:** a spacing scale (`--sv-space-*`), radius scale (`--sv-radius-sm/-/-lg`), elevation/shadow scale (`--sv-shadow-sm/-`), and a type scale. Use existing `--sv-radius` / `--sv-transition` as the basis.

### 4b. Theming
- Light + dark via `[data-theme]`. **Make light the default look** and dark a deliberate alternative.
- Specify the **nav theme-toggle** UX: a small icon button in `.sv-nav` (Tabler `ti-sun` / `ti-moon`) that flips `document.documentElement.dataset.theme` and persists to `localStorage` (alongside the existing `bizzz_token` key — don't collide with it). Provide the few lines of JS and where they go (`base.html` `extra_scripts` or a shared snippet).

### 4c. Components — restyle existing + add what the dashboard needs
Restyle every existing `.sv-*` class (§2) under the new tokens. Then design these **new dashboard components** (this app needs them but they don't exist yet — give HTML + CSS):
- **Button hierarchy:** primary (solid indigo), secondary (outline/neutral), ghost, danger. **Reserve the lift+glow gradient effect for the hero CTA only** — current CSS applies a purple glow to *every* button, which is noise in an admin UI. Fix this.
- **Cards / panels** for dashboard sections (with header, body, optional action row).
- **Stat / metric tiles** (e.g. conversations today, orders, AI status).
- **Platform connection chips/cards** using the platform brand colors, with connected/disconnected/error states.
- **Status badges / pills** using semantic colors (online, paid, pending, failed).
- **Data tables** (products, orders, conversations) — comfortable density, zebra or bordered, responsive behavior.
- **Forms** — inputs, selects, labels, validation/error states (extend `.sv-form` / `.sv-form-error`), built on Pico's form elements.
- **Empty states**, **loading states** (HTMX `aria-busy` spinner styling — already used in `.sv-status-box`), and **toast/inline alert** styling for the 4 semantic colors.
- **A simple dashboard shell**: sidebar or top-nav layout suggestion that fits the existing `.sv-nav` + `.container`/`.container-fluid` Pico structure.

### 4d. Three design rules to enforce (state them in DESIGN_SYSTEM.md)
1. **Reserve the brand color.** Only the *primary* action is indigo-solid; secondary actions are neutral/outline. The gradient + glow is for hero brand moments only.
2. **Semantic, not decorative, color.** Connection chips, "AI online", "webhook failed", "order paid" ALWAYS use semantic/platform tokens — never brand indigo/purple.
3. **Light mode is the default; dark is opt-in.** Wire the toggle, persist the choice.

### 4e. Typography
- Recommend a font pairing that works via Google Fonts CDN (one line in `base.html`) and reads well for a multilingual SMB audience (Latin + good fallback). Keep it professional, not decorative. Provide the `<link>` and the `--sv-font-*` tokens + base `body`/heading rules. Default to system fonts if you judge a webfont adds risk — justify the call.

---

## 5. Output format

1. **`static/css/app.css`** — the complete, ready-to-commit stylesheet (replaces the current file). Keep all existing `.sv-*` class names working. Well-commented section headers like the current file.
2. **`DESIGN_SYSTEM.md`** — token reference table, component gallery (HTML snippets), the 3 rules, theming/toggle instructions, font setup, and a short "how to add a new component" note.
3. **Any required edits to `templates/base.html`** (font link, theme-toggle button + JS) — show them as diffs or full snippets with exact placement.

Keep everything dependency-free beyond the already-loaded Pico, Tabler Icons, HTMX, and (optionally) one Google Fonts link. Match the existing code's comment density and naming idiom. Explain non-obvious choices briefly inline.
