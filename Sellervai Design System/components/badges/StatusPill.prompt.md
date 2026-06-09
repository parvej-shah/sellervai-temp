Status pills carry meaning through semantic color — order paid, AI online, token expiring, webhook failed — never brand indigo/purple. Platform chips show a connected channel tinted with its brand color.

```jsx
<StatusPill tone="success" dot live>AI online</StatusPill>
<StatusPill tone="success">Paid</StatusPill>
<StatusPill tone="warning">Pending</StatusPill>
<StatusPill tone="danger">Webhook failed</StatusPill>
<StatusPill tone="neutral" dot>Draft</StatusPill>

<PlatformChip platform="whatsapp" label="+880 1xxx" />
<PlatformChip platform="telegram" />
```

- `dot` + `live` = the pulsing online indicator for the AI-status widget.
- Omit `dot` to get an auto status icon (check / alert).
