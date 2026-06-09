Stat tiles head the dashboard — one metric each (conversations today, orders, AI status), with a big tabular figure and an optional trend delta.

```jsx
<StatTile label="Conversations today" value="248" icon="messages" delta="+12%" trend="up" />
<StatTile label="Orders" value="37" icon="shopping-bag" delta="-4%" trend="down" />
<StatTile label="Revenue" value="৳ 84,200" icon="coin" />
```

Lay them out in a responsive grid (e.g. `repeat(auto-fit, minmax(200px, 1fr))`). Keep figures concrete — no filler numbers.
