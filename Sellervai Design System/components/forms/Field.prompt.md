Labeled form control wrapping Pico inputs, with the Sellervai focus ring, optional marker, and inline validation. Use inside `.sv-form` grids.

```jsx
<form className="sv-form">
  <Field label="Email" type="email" placeholder="you@example.com" />
  <Field label="Phone" type="tel" optional placeholder="+880…" />
  <Field label="Platform" as="select" options={[{value:'wa',label:'WhatsApp'}]} />
  <Field label="Password" type="password" error="Min 8 characters" />
</form>
```

`error` switches the control to the danger ring and prints the message. `optional` adds the muted "(optional)" tag.
