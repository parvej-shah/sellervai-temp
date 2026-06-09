# Sellervai Design System

A production design system for **Sellervai** — a B2B SaaS that connects a merchant's
store to **WhatsApp, Messenger, Instagram, and Telegram** and runs an **AI agent
(DeepSeek + RAG)** that answers customers, recommends products, and closes orders 24/7.

This system builds directly on the live app's token + class architecture
(`--sv-*` custom properties, `.sv-*` classes, Pico CSS v2, Tabler Icons, HTMX) —
it restyles what exists and adds the dashboard components the product needs, without
introducing a new framework or build step.

## Sources

- **GitHub repo:** https://github.com/parvej-shah/sellervai-temp
  - `static/css/app.css` — original token + component layer (this system supersedes it)
  - `templates/base.html`, `index.html`, `login.html`, `register.html` — Mako templates
  - `README.md`, `CONTEXT.md`, `V1.0.md` — architecture & product context

  Explore that repo to build higher-fidelity designs against the real product
  (data models, routes, HTMX wiring, platform connection flows).

---

## Who it serves

Non-technical store owners in a multilingual / South-Asian-and-global SMB market.
They keep the **dashboard open all day** during business hours. The system must feel
**trustworthy, calm, and competent** — it handles their customers and their money.
We favor clarity and confidence over flashy "AI startup" gimmickry.

**Surfaces, in priority order:**
1. **Dashboard** — conversations, orders, products, coupons, platform status, live HTMX widgets. Data-dense, long-session. Readability and calm win over saturation.
2. **Store detail** (`/stores/{id}`) — store config, products, coupons, orders, platform connect/disconnect.
3. **Marketing homepage + auth** — login / register incl. Google sign-in.

---

## The three rules (enforce these)

1. **Reserve the brand color.** Only the *primary* action is indigo-solid; secondary
   actions are neutral/outline. The gradient + glow (`.sv-btn-hero`) is for hero brand
   moments only — never on dense UI like table rows or form controls.
2. **Semantic, not decorative, color.** Connection chips, "AI online", "webhook failed",
   "order paid" ALWAYS use semantic/platform tokens — never brand indigo/purple.
3. **Light mode is the default; dark is opt-in.** Wire the toggle, persist the choice
   (`sv-theme` in `localStorage`, alongside the existing `bizzz_token` key).

---

## CONTENT FUNDAMENTALS

How Sellervai writes copy (lifted from the live templates):

- **Voice:** confident, plain, benefit-first. Speaks to a busy owner, not an engineer.
  *"Automate your store with intelligent AI"*, *"Everything you need to sell smarter"*,
  *"Connect Facebook, Instagram, and WhatsApp via OAuth in seconds — no API keys needed."*
- **Person:** addresses the user as **you / your** ("your store", "your AI assistant").
  Refers to the product by name ("Sellervai connects your store…") — first person plural
  is avoided in UI copy.
- **Casing:** **Sentence case** everywhere — headings, buttons, labels. Not Title Case.
  ("Start for free", "Create account", "Get started", "Platform status".)
- **Tone:** calm and reassuring on anything touching money or security
  ("All tokens are encrypted at rest. Your data never leaves your own database.").
  Action labels are short imperatives ("Sign in", "Get started", "Create one").
- **Emoji:** used **only** in long-form docs/README, **never** in product UI. In the UI,
  meaning is carried by Tabler icons + semantic color, not emoji.
- **Numbers & units:** tabular figures for any aligned data; currency and counts are
  concrete, never faked filler.
- **Microcopy patterns:** friendly recovery for errors ("Network error. Please try
  again."), optional fields marked inline with a muted "(optional)" via `.sv-optional`.

---

## VISUAL FOUNDATIONS

- **Palette identity:** **Indigo + Purple** — same family, distinct jobs. Indigo
  (`--sv-indigo`) is the workhorse (buttons, links, focus, active). Purple
  (`--sv-purple`) is the flourish (gradient end, hero accent word, badges, AI moments).
  The **indigo→purple gradient** (`--sv-gradient`, 135°) is the signature element, used
  sparingly: hero `<h1>` accent, `.sv-badge`, brand logo icon, the single hero CTA, hover glow.
- **Neutrals:** light is the comfortable default — page `#f6f7fb`, white cards, hairline
  `#e4e6f0` borders. Dark gives cards real separation: page `#0f1020`, cards `#1a1a2e`,
  raised `#232544`.
- **Type:** Plus Jakarta Sans (UI + display, weights 400–800), JetBrains Mono (IDs, code,
  aligned numbers). Headings are bold with tight tracking (`-0.02em`) and balanced wrap;
  body is 1.6 line-height. Eyebrows are uppercase, `0.04em`, muted.
- **Spacing:** 4px base scale (`--sv-space-1..8`). Cards pad `--sv-space-5` (24px).
- **Corner radii:** controls/inputs `8px` (`--sv-radius-sm`), cards `12px` (`--sv-radius`),
  large panels `18px` (`--sv-radius-lg`), pills `100px`.
- **Borders:** 1px hairlines are the primary separator — calm, not heavy. Inputs use a
  stronger border (`--sv-border-strong`); focus is a 2px indigo ring + 3px subtle halo.
- **Shadows:** soft and low. Cards rest on `--sv-shadow-sm`; raised/hover on `--sv-shadow`;
  modals on `--sv-shadow-lg`. The **glow** (`--sv-shadow-glow`, indigo) is RESERVED for the
  hero CTA — it is deliberately absent from admin UI.
- **Backgrounds:** flat solid surfaces. No full-bleed photography, no textures, no noise.
  Gradients appear ONLY as the brand signature (hero accent / badge / logo / hero CTA).
- **Animation:** quiet. `0.2s ease` default (`--sv-transition`), `0.12s` for fast row hovers.
  A gentle float on the hero icon; a `sv-pulse` ring on the live "AI online" dot; an
  `sv-shimmer` skeleton for HTMX loading. No bounces, no infinite decorative loops on content.
- **Hover/press:** buttons shift to a darker indigo on hover (not lift) — except the hero
  CTA, which lifts `-2px` and gains the glow. Rows tint to `--sv-surface-2`. Ghost buttons
  fill with the surface tint. Cards lift subtly only on the marketing feature grid.
- **Transparency / blur:** the sticky nav uses `backdrop-filter: blur(12px)` over a
  translucent surface. Subtle tints (`--sv-accent-subtle`, `*-subtle` semantics) are
  10–16% alpha fills behind icons, pills, and alerts.
- **Imagery vibe:** icon-driven, not photographic. Tabler line icons throughout; platform
  brand logos only on connection chips/cards.

---

## ICONOGRAPHY

- **System:** **Tabler Icons** webfont, loaded from CDN and used as `<i class="ti ti-xxx">`.
  This is the app's only icon system — match its stroke weight (1.5–2px line icons).
- **In React components:** pass the icon name *without* the `ti-` prefix
  (e.g. `<Button icon="rocket">`); the component prepends `ti ti-`.
- **Common glyphs in use:** `ti-robot` (brand mark), `ti-sparkles` (AI badge),
  `ti-messages`, `ti-brain`, `ti-database`, `ti-chart-bar`, `ti-plug-connected`,
  `ti-lock`, `ti-rocket`, `ti-login`, `ti-user-plus`, `ti-sun` / `ti-moon` (theme toggle).
- **Platform marks:** `ti-brand-whatsapp`, `ti-brand-messenger`, `ti-brand-instagram`,
  `ti-brand-telegram` — always tinted with the matching platform token, never brand indigo.
- **No emoji and no ad-hoc SVGs** in product UI — Tabler covers the set. The brand logo is
  the `ti-robot` glyph in indigo + the "Sellervai" wordmark; `static/favicon.ico` is the
  imported app favicon.

---

## INDEX / manifest

**Root**
- `styles.css` — entry point (consumers link this). `@import` manifest only.
- `base.css` — base element styles (body, headings, links, focus).
- `components.css` — the full `.sv-*` component layer (source of truth for production app.css).
- `tokens/` — `colors.css`, `typography.css`, `spacing.css`, `fonts.css`.

**Components** (`window.SellervaiDesignSystem_76e02e.*`)
- `buttons/` — `Button`, `IconButton`
- `badges/` — `StatusPill`, `PlatformChip`
- `surfaces/` — `Card`, `StatTile`
- `forms/` — `Field`
- `feedback/` — `Alert`, `EmptyState`

**Foundation cards** — Type, Colors, Spacing, Brand specimen cards (Design System tab).

**UI kits**
- `ui_kits/dashboard/` — the live product dashboard.
- `ui_kits/store_detail/` — store config, products, platform connections.
- `ui_kits/marketing/` — homepage + auth (login / register).

**Production deliverables** (`production/`)
- `production/static/css/app.css` — the complete, drop-in stylesheet.
- `production/DESIGN_SYSTEM.md` — token reference, component gallery, theming + font setup.
- `production/base.html.snippet.md` — exact `base.html` edits (font link, theme toggle + JS).

**`SKILL.md`** — makes this folder usable as a downloadable Agent Skill.

---

## How to add a new component

1. Create `components/<group>/<Name>.jsx` with `export function <Name>(props) {…}`,
   styling via `.sv-*` classes (add the class to `components.css`, never CSS-in-JS).
2. Add `<Name>.d.ts` (props interface) and `<Name>.prompt.md` (one-line what/when + usage).
3. Add/extend the directory's `*.card.html` (`<!-- @dsCard group="Components" … -->` on line 1).
4. Run `check_design_system` until clean.
