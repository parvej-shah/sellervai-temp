Card is the standard dashboard panel — a titled section with a body and optional header action / footer. Compose tables, forms, lists, and platform rows inside it.

```jsx
<Card title="Recent orders" action={<Button variant="ghost" size="sm" iconRight="chevron-right">View all</Button>}>
  <table className="sv-table">…</table>
</Card>
```

Pass `footer` for an action bar. Omit `title` + `action` for a plain body-only card.
