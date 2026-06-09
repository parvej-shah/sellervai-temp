# `templates/base.html` — required edits

Three changes: (1) default to light + restore saved theme before paint, (2) add the
Google Fonts link, (3) add the theme-toggle button in `.sv-nav`. Everything else in
`base.html` stays as-is. The single `app.css` link you already have keeps working.

---

## 1. `<html>` tag — default to light, restore saved theme before first paint

Replace the opening tag and add a tiny inline script as the **first** thing in `<head>`
so there is no theme flash (FOUC). It reads `sv-theme` from `localStorage` (separate
from the existing `bizzz_token` key).

```html
<!doctype html>
<html lang="en" data-theme="light">   <!-- was data-theme="dark" -->

<head>
  <meta charset="utf-8" />
  <!-- Restore saved theme before paint (avoids flash). Keep this first. -->
  <script>
    (function () {
      try {
        var t = localStorage.getItem("sv-theme");
        if (t) document.documentElement.dataset.theme = t;
      } catch (e) {}
    })();
  </script>
  <!-- …rest of head… -->
```

## 2. Google Fonts — add inside `<head>` (before the `app.css` link)

```html
  <!-- Fonts: Plus Jakarta Sans (UI) + JetBrains Mono (data) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" />
```

> `app.css` also `@import`s these fonts as a fallback, but the `<link>` is faster — keep both.

## 3. Theme toggle — add to the right-hand `<ul>` in `.sv-nav`

```html
  <nav class="container-fluid sv-nav">
    <ul>
      <li>
        <a href="/" class="sv-brand">
          <span class="sv-brand-mark"><i class="ti ti-robot"></i></span>
          <strong>Sellervai</strong>
        </a>
      </li>
    </ul>
    <ul class="sv-nav-actions">
      <li>
        <button id="sv-theme-toggle" class="sv-theme-toggle" aria-label="Toggle theme" type="button">
          <i class="ti ti-sun"></i><i class="ti ti-moon"></i>
        </button>
      </li>
      ${self.nav_items()}
    </ul>
  </nav>
```

## 4. Toggle handler — add to the `extra_scripts` block at the bottom of `base.html`

```html
  <script>
    (function () {
      var btn = document.getElementById("sv-theme-toggle");
      if (!btn) return;
      btn.addEventListener("click", function () {
        var root = document.documentElement;
        var next = root.dataset.theme === "dark" ? "light" : "dark";
        root.dataset.theme = next;
        try { localStorage.setItem("sv-theme", next); } catch (e) {}
      });
    })();
  </script>
```

The CSS already swaps the sun/moon icon by theme (`.sv-theme-toggle .ti-sun/.ti-moon`),
so the button shows the correct glyph automatically.
