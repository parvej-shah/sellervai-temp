Inline alert / toast for the four semantic outcomes — order paid, token expiring, webhook failed, info sync. Use semantic tone, never brand color.

```jsx
<Alert tone="success" title="Order paid">Payment confirmed via bKash.</Alert>
<Alert tone="warning" title="Token expiring">Reconnect WhatsApp within 3 days.</Alert>
<Alert tone="danger" title="Webhook failed">Meta returned 403 — verify your token.</Alert>
<Alert tone="info">Knowledge base re-indexed.</Alert>
```
