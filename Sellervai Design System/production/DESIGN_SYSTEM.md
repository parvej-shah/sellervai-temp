# Sellervai — DESIGN_SYSTEM.md

Production design system for the Sellervai dashboard, store pages, and marketing site.
Built **on top of** Pico CSS v2 (CDN) + Tabler Icons + HTMX — no new framework, no build
step. All custom styling lives in `static/css/app.css` as `--sv-*` tokens and a thin
`.sv-*` class layer. Supports **light (default)** and **dark** via `<html data-theme>`.

> Files: `static/css/app.css` (drop-in stylesheet) · `base.html.snippet.md` (template edits).

---

## The three rules

1. **Reserve the brand color.** Only the *primary* action is indigo-solid (`.sv-btn-primary`);
   secondary actions are neutral/outline. The gradient + glow (`.sv-btn-hero`) is for hero
   brand moments only — never on table rows or form controls.
2. **Semantic, not decorative, color.** Connection chips, "AI online", "webhook failed",
   "order paid" ALWAYS use semantic/platform tokens — never brand indigo/purple.
3. **Light mode is the default; dark is opt-in.** Wire the toggle, persist to
   `localStorage` under `sv-theme` (separate from `bizzz_token`).

---

## Token reference

### Brand
| Token | Light | Dark | Job |
|---|---|---|---|
| `--sv-indigo` | `#5b5bf0` | `#7c7cff` | Workhorse: buttons, links, focus, active |
| `--sv-purple` | `#a855f7` | `#c084fc` | Flourish: gradient end, AI accents, badges |
| `--sv-accent` | = indigo | = indigo | Primary action color |
| `--sv-accent-hover` | `#4848d6` | `#9b9bff` | Hover |
| `--sv-accent-subtle` | `rgba(124,92,246,.10)` | `.16` | Soft tint behind icons/pills |
| `--sv-gradient` | `135° indigo→purple` | (lifted) | Signature element — use sparingly |

### Neutrals
| Token | Light | Dark |
|---|---|---|
| `--sv-bg` | `#f6f7fb` | `#0f1020` |
| `--sv-surface` | `#ffffff` | `#1a1a2e` |
| `--sv-surface-2` | `#eef0f7` | `#232544` |
| `--sv-border` | `#e4e6f0` | `rgba(255,255,255,.09)` |
| `--sv-border-strong` | `#d2d6e6` | `rgba(255,255,255,.16)` |
| `--sv-text` | `#181a2c` | `#eef0fb` |
| `--sv-text-muted` | `#5b6184` | `rgba(255,255,255,.60)` |
| `--sv-text-subtle` | `#8a90ab` | `rgba(255,255,255,.40)` |

### Semantic status (each has a matching `*-subtle` tint)
| Token | Light | Dark | Use |
|---|---|---|---|
| `--sv-success` | `#16a34a` | `#34d399` | AI online, order paid |
| `--sv-warning` | `#d97706` | `#fbbf24` | Token expiring, RAG out of sync |
| `--sv-danger` | `#dc2626` | `#f87171` | Webhook failed, disconnected |
| `--sv-info` | `#0284c7` | `#38bdf8` | Neutral notices, syncing |

### Platform (fixed — never themed)
`--sv-whatsapp #25d366` · `--sv-messenger #0084ff` · `--sv-instagram #e1306c` · `--sv-telegram #229ed9`

### Scales
- **Spacing** `--sv-space-1..8` → 4/8/12/16/24/32/48/64px
- **Radius** `--sv-radius-sm 8` · `--sv-radius 12` · `--sv-radius-lg 18` · `--sv-radius-pill`
- **Elevation** `--sv-shadow-sm` (rest) · `--sv-shadow` (raised) · `--sv-shadow-lg` (modal) · `--sv-shadow-glow` (hero CTA only)
- **Type** `--sv-fs-xs 12 … --sv-fs-2xl 36`, `--sv-fs-3xl` (hero); weights `--sv-fw-normal..bold` (400–700, plus 800 for display)
- **Motion** `--sv-transition .2s` · `--sv-transition-fast .12s`

### Fonts
`--sv-font-sans` = Plus Jakarta Sans · `--sv-font-mono` = JetBrains Mono. Loaded via the
Google Fonts `<link>` in `base.html` (and an `@import` fallback in `app.css`). Bengali /
South-Asian copy falls back to Hind Siliguri / Noto Sans where the OS provides it. The
original repo shipped no webfont (Pico system stack); this pairing is the recommended
upgrade — swap the `<link>`/`@import` for self-hosted `@font-face` for offline/GDPR builds.

---

## Component gallery (HTML snippets)

### Buttons
```html
<button class="sv-btn sv-btn-primary"><i class="ti ti-check"></i> Save</button>
<button class="sv-btn sv-btn-secondary">Cancel</button>
<button class="sv-btn sv-btn-ghost"><i class="ti ti-dots"></i> More</button>
<button class="sv-btn sv-btn-danger"><i class="ti ti-plug-off"></i> Disconnect</button>
<button class="sv-btn sv-btn-hero"><i class="ti ti-rocket"></i> Start for free</button>  <!-- hero ONLY -->
<button class="sv-icon-btn" aria-label="More"><i class="ti ti-dots-vertical"></i></button>
<!-- sizes: add .sv-btn-sm / .sv-btn-lg ; loading: add aria-busy="true" -->
```

### Status pills (semantic)
```html
<span class="sv-pill sv-pill-success"><span class="sv-dot is-live"></span> AI online</span>
<span class="sv-pill sv-pill-success">Paid</span>
<span class="sv-pill sv-pill-warning">Pending</span>
<span class="sv-pill sv-pill-danger">Webhook failed</span>
<span class="sv-pill sv-pill-neutral"><span class="sv-dot"></span> Draft</span>
```

### Platform chips & cards
```html
<span class="sv-chip sv-chip-whatsapp"><i class="sv-chip-icon ti ti-brand-whatsapp"></i> WhatsApp</span>

<div class="sv-platform sv-platform-telegram">
  <span class="sv-platform-logo"><i class="ti ti-brand-telegram"></i></span>
  <div class="sv-platform-meta"><p class="sv-platform-name">Telegram Bot</p><p class="sv-platform-sub">Not connected</p></div>
  <button class="sv-btn sv-btn-primary sv-btn-sm"><i class="ti ti-plug-connected"></i> Connect</button>
</div>
```

### Card + stat tile
```html
<section class="sv-card">
  <header class="sv-card-header">
    <h3 class="sv-card-title">Recent orders</h3>
    <button class="sv-btn sv-btn-ghost sv-btn-sm">View all <i class="ti ti-chevron-right"></i></button>
  </header>
  <div class="sv-card-body"> … </div>
  <footer class="sv-card-footer"><button class="sv-btn sv-btn-secondary sv-btn-sm">Export CSV</button></footer>
</section>

<article class="sv-stat">
  <div class="sv-stat-head"><span class="sv-stat-label">Conversations today</span>
    <span class="sv-stat-icon"><i class="ti ti-messages"></i></span></div>
  <div class="sv-stat-value sv-tnum">248</div>
  <span class="sv-stat-delta is-up"><i class="ti ti-trending-up"></i> +12%</span>
</article>
```

### Data table
```html
<div class="sv-table-wrap">
  <table class="sv-table">
    <thead><tr><th>Order</th><th>Customer</th><th class="sv-tnum">Total</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>#ORD-10482</td><td>Tanvir Ahmed</td><td class="sv-tnum">৳ 2,400</td>
          <td><span class="sv-pill sv-pill-success">Paid</span></td></tr>
    </tbody>
  </table>
</div>
```

### Forms (extends `.sv-form` / `.sv-form-error`)
```html
<form class="sv-form">
  <label class="sv-field"><span class="sv-field-label">Email</span>
    <input class="sv-input" type="email" placeholder="you@example.com" /></label>
  <label class="sv-field"><span class="sv-field-label">Phone<span class="sv-optional"> (optional)</span></span>
    <input class="sv-input" type="tel" /></label>
  <label class="sv-field"><span class="sv-field-label">Password</span>
    <input class="sv-input is-invalid" type="password" />
    <p class="sv-field-error">Min 8 characters.</p></label>
</form>
```

### Alerts (4 semantic tones) & empty / loading states
```html
<div class="sv-alert sv-alert-warning"><i class="ti ti-alert-triangle"></i>
  <div><p class="sv-alert-title">Token expiring</p><p>Reconnect WhatsApp within 3 days.</p></div></div>

<div class="sv-empty">
  <span class="sv-empty-icon"><i class="ti ti-messages-off"></i></span>
  <h3>No conversations yet</h3><p>Once you connect a platform, chats land here.</p>
  <button class="sv-btn sv-btn-primary"><i class="ti ti-plug-connected"></i> Connect a channel</button>
</div>

<!-- HTMX loading: Pico's spinner -->
<div hx-get="/health" hx-trigger="load, every 30s" class="sv-status-box"><span aria-busy="true">Checking status…</span></div>
<!-- or a shimmer block: --> <div class="sv-skeleton" style="height:1rem"></div>
```

### Dashboard shell
`.sv-shell` (grid) → `.sv-sidebar` (with `.sv-side-link` / `.is-active`) + content
(`.sv-topbar` + `.sv-content`). Collapses to single column under 900px. See
`ui_kits/dashboard/` for the full example.

---

## Theming & the toggle

`app.css` defines all tokens twice: under `:root` (light) and `[data-theme="dark"]`.
Set `data-theme` on `<html>` and everything re-themes. Wire the nav toggle and persist
to `localStorage` under `sv-theme` — exact markup + JS in `base.html.snippet.md`.

---

## How to add a new component

1. Add a `.sv-<name>` block to `app.css` under the **Component layer** section. Style only
   with `--sv-*` tokens — no hard-coded colors, so it themes for free.
2. Use Pico's semantic element underneath where one exists (button, input, table).
3. Reserve brand color/gradient for primary/hero only; use semantic/platform tokens for status.
4. Add an HTML snippet to this gallery so the next person can copy it.
