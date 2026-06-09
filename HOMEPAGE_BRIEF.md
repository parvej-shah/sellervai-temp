# Homepage Expansion Brief — Sellervai

> **Your task:** Add new marketing sections to the Sellervai homepage to turn it from a thin 3-section page into a complete, conversion-oriented SaaS landing page. Work within the existing repo: edit **`templates/index.html`** (Mako) and extend **`static/css/app.css`** using the existing design system. Do NOT introduce a framework, build step, or new dependency.

---

## 1. Product context (what we're selling)

Sellervai is a **B2B SaaS for small/mid store owners**. It connects a merchant's store to **WhatsApp, Facebook Messenger, Instagram, and Telegram**, and runs an **AI agent (DeepSeek + RAG)** that answers customers, recommends products, and helps close orders **24/7**.

- **Audience:** non-technical store owners, multilingual / South-Asian-and-global SMB market. They want to feel this tool is **trustworthy, easy to set up, and worth paying for**.
- **Primary conversion goal:** get the visitor to click **"Start for free" → `/register`**.
- **Tone:** confident and clear; benefit-led, not jargon. Avoid hype-y "AI startup" copy. Speak to outcomes: never miss a customer message, sell while you sleep, set up in minutes.

---

## 2. Tech constraints (read before writing)

- **Template:** `templates/index.html` is **Mako**, inheriting `base.html`. It overrides defs: `title`, `meta_description`, `nav_items`, `extra_scripts`. Add sections inside the body; keep the existing `<%def>` blocks working.
- **CSS:** [Pico CSS v2](https://picocss.com/) (CDN, semantic) + custom `static/css/app.css`. Style new sections with new `.sv-*` classes that match the existing naming/comment style.
- **Icons:** Tabler Icons webfont — `<i class="ti ti-xxx"></i>`.
- **Interactivity:** HTMX v2 only. No JS framework, no build step. Any interactivity (accordions, tabs) should be CSS-only or tiny vanilla JS in `extra_scripts`.
- **Design system:** Indigo + Purple. **Indigo (`--sv-accent`) = solid actions; purple = flourish; the `--sv-gradient` (indigo→purple) is for brand moments only** (hero accent word, badges, section eyebrows, final CTA). Reserve the lift+glow effect for primary CTAs — not every button. Use the semantic tokens (`--sv-success/-warning/-danger`) and platform brand colors (`--sv-whatsapp #25d366`, `--sv-messenger #0084ff`, `--sv-instagram #e1306c`, `--sv-telegram #229ed9`) where relevant. Support both light and dark via `data-theme`.
- **Responsive:** mobile-first; every new section must collapse cleanly to single-column on small screens (match the existing `@media (max-width: 640px)` pattern).
- **Accessibility:** real heading hierarchy, `aria-*` where needed, sufficient contrast in both themes, decorative icons `aria-hidden`.

### What already exists on the page (do NOT duplicate)
1. **Hero** (`#hero`, `.sv-hero`) — badge, headline with gradient `<em>`, subcopy, two CTAs, floating robot icon.
2. **Features** (`#features`, `.sv-feature-grid`) — 6 feature cards.
3. **Platform status** (`#status-section`, `.sv-status-box`) — live HTMX `/health` widget.

Keep these. Insert the new sections **between Features and the live status widget**, and add a final CTA + footer-area sections after status as noted below.

---

## 3. New sections to add (in this order)

Write semantic, benefit-led copy for each (don't leave placeholders). Each section gets an `id`, a `.sv-section-title` (or new eyebrow+title pattern), and responsive CSS.

### 3a. Social proof strip (`#trust`)
A slim band directly under the hero: a short line like "Trusted by growing stores" + a row of the 4 platform logos/icons (WhatsApp, Messenger, Instagram, Telegram) using their brand colors, OR placeholder merchant logos. Keep it understated.

### 3b. How it works (`#how-it-works`)
3-step horizontal flow with numbered badges and Tabler icons:
1. **Connect your channels** — one-click OAuth for WhatsApp, Messenger, Instagram, Telegram (`ti-plug-connected`).
2. **Train your AI** — upload your catalogue, PDFs, and store info; RAG learns it automatically (`ti-brain` / `ti-upload`).
3. **Start selling 24/7** — the AI answers, recommends, and closes orders while you sleep (`ti-rocket`).
Use a connecting line/arrow between steps on desktop; stack vertically on mobile.

### 3c. Supported platforms (`#platforms`)
A dedicated grid/row of the 4 messaging platforms as branded cards (each using its `--sv-<platform>` color for the icon/accent), with a one-line value prop per platform. Reinforces the core promise visually.

### 3d. Deeper feature / benefit showcase (`#showcase`)
2–3 alternating image-left/text-right "feature spotlight" rows (text + a placeholder visual or a large Tabler icon / mock UI card). Pick the strongest differentiators:
- **AI that knows your catalogue** (RAG knowledge base).
- **One inbox, every channel** (unified multi-platform).
- **Set up in minutes, no code** (OAuth, no API keys).
Each row: eyebrow label (gradient text), heading, 2–3 sentence benefit, optional bullet list with check icons (`ti-check`), and a subtle CTA link.

### 3e. Stats / impact band (`#stats`)
A horizontal band with 3–4 metric tiles (large gradient number + label): e.g. "24/7 availability", "4 channels in 1", "Minutes to set up", "0 messages missed". Use placeholder-but-credible figures; mark clearly in a comment that they're illustrative.

### 3f. Testimonials (`#testimonials`)
2–3 testimonial cards (quote, avatar placeholder, name, store/role). Realistic SMB voices (e.g. a boutique owner, an electronics reseller). Clean cards using `--sv-surface`/`--sv-border`.

### 3g. Pricing (`#pricing`)
A 3-tier pricing grid — **Free**, **Pro** (highlighted/"Most popular" with gradient border or badge), **Business**. Each: price, short description, feature list with `ti-check`, and a CTA button (Free → `/register`, others → `/register` or "Contact sales"). Make the Pro card visually elevated. Add a small note about billing being illustrative in a comment.

### 3h. FAQ (`#faq`)
CSS-only or `<details>`-based accordion, 5–6 Q&A relevant to the audience:
- Do I need technical skills to set up?
- Which platforms are supported?
- How does the AI learn about my products?
- Is my data and my customers' data secure?
- Can I try it for free?
- What languages does the AI support? (multilingual — yes)
Use native `<details>/<summary>` styled with the design tokens (no JS needed).

### 3i. Final CTA (`#cta`)
A full-width gradient (or gradient-bordered) band: strong headline ("Start selling smarter today"), one line of subcopy, and a single prominent primary CTA → `/register`. This is the page's closing conversion moment — the one place to use the full gradient + glow treatment.

> Keep the existing **Platform status** widget (`#status-section`) — place it near the end (before or after Final CTA, your call) as a live "we're operational" trust signal.

---

## 4. CSS & quality requirements

- Add all new styles to `static/css/app.css` under clearly commented section headers matching the file's existing `/* ── … ── */` style.
- Reuse existing tokens (`--sv-accent`, `--sv-gradient`, `--sv-surface`, `--sv-border`, `--sv-radius`, `--sv-text-muted`, spacing/shadow scales). Do not hardcode colors that a token already covers.
- Consistent vertical rhythm between sections (use the spacing scale).
- All new sections must look correct in **both light and dark** themes.
- Subtle, tasteful motion only (respect `prefers-reduced-motion`); don't over-animate.
- Don't break the existing `extra_scripts` auth-redirect logic.

## 5. Output format

1. **Updated `templates/index.html`** — full file with new sections inserted in the order above, real copy, correct Mako structure.
2. **Appended `static/css/app.css`** — the new section styles (show as additions; don't rewrite existing rules unless necessary, and if so, explain why).
3. A short **summary** of what was added and any copy/figures that are illustrative placeholders the owner should replace.

Match the existing code's comment density, class-naming (`.sv-*`), and idiom. Explain any non-obvious choices briefly inline.
