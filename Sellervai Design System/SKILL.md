---
name: sellervai-design
description: Use this skill to generate well-branded interfaces and assets for Sellervai, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the `readme.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out
and create static HTML files for the user to view. If working on production code, you can
copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to
build or design, ask some questions, and act as an expert designer who outputs HTML
artifacts _or_ production code, depending on the need.

## What's here

- `readme.md` — product context, content + visual foundations, iconography, manifest.
- `styles.css` — entry point; `@import`s the tokens + base + component layer.
- `tokens/` — `colors.css`, `typography.css`, `spacing.css`, `fonts.css` (`--sv-*` props).
- `base.css`, `components.css` — base element styles + the full `.sv-*` class layer.
- `components/` — React primitives (Button, IconButton, StatusPill, PlatformChip, Card,
  StatTile, Field, Alert, EmptyState) with `.d.ts` + `.prompt.md` each.
- `guidelines/` — foundation specimen cards (Colors, Type, Spacing, Brand).
- `ui_kits/` — `marketing/` (homepage + auth), `dashboard/`, `store_detail/`.
- `production/` — drop-in `static/css/app.css`, `DESIGN_SYSTEM.md`, `base.html.snippet.md`.

## The three rules (always enforce)

1. **Reserve the brand color** — only the primary action is indigo-solid; the gradient +
   glow is for hero brand moments only, never dense admin UI.
2. **Semantic, not decorative, color** — connection chips and status use semantic/platform
   tokens, never brand indigo/purple.
3. **Light is the default; dark is opt-in** — persist `sv-theme` to `localStorage`.

## Stack

Pico CSS v2 + Tabler Icons (`<i class="ti ti-…">`) + HTMX, server-rendered Mako templates.
No build step. Style with `--sv-*` tokens so everything themes for free. Plus Jakarta Sans
(UI) + JetBrains Mono (data) via Google Fonts.
