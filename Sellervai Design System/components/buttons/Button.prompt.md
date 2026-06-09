Buttons drive every action in Sellervai — one solid indigo `primary` per view, neutral `secondary`/`ghost` for the rest, `danger` for destructive, and `hero` (gradient + glow) reserved for the marketing CTA.

```jsx
<Button variant="primary" icon="rocket">Start for free</Button>
<Button variant="secondary">Cancel</Button>
<Button variant="ghost" size="sm" icon="dots">More</Button>
<Button variant="danger" icon="trash">Disconnect</Button>
<Button variant="hero" as="a" href="/register" icon="rocket">Get started</Button>
<IconButton icon="dots-vertical" label="Row actions" />
```

- `busy` adds Pico's `aria-busy` spinner (great for HTMX submits).
- Use `as="a"` + `href` to render a link styled as a button.
- Never use `hero` inside the dashboard — it is brand noise in dense admin UI.
