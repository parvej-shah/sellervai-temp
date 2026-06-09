/* Sellervai — Store detail UI kit (/stores/{id}). Store config, products,
   coupons, orders, and platform connect/disconnect — composed from .sv-* classes. */

function StoreTheme() {
  const [theme, setTheme] = React.useState(() => document.documentElement.dataset.theme || "light");
  React.useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("sv-theme", theme); } catch (e) {}
  }, [theme]);
  return (
    <button className="sv-theme-toggle" aria-label="Toggle theme"
      onClick={() => setTheme((t) => (t === "dark" ? "light" : "dark"))}>
      <i className="ti ti-sun" /><i className="ti ti-moon" />
    </button>
  );
}

const PRODUCTS = [
  { name: "Hand-block Cotton Kurti", sku: "KRT-014", price: "৳ 1,250", stock: 24, status: ["success", "Active"] },
  { name: "Silk Scarf — Indigo", sku: "SCF-007", price: "৳ 690", stock: 8, status: ["warning", "Low stock"] },
  { name: "Leather Sandals", sku: "SND-031", price: "৳ 2,100", stock: 0, status: ["danger", "Out of stock"] },
  { name: "Embroidered Tote Bag", sku: "BAG-019", price: "৳ 950", stock: 41, status: ["success", "Active"] },
];

const COUPONS = [
  { code: "EID25", off: "25% off", uses: "142 / 500", status: ["success", "Active"] },
  { code: "WELCOME10", off: "৳ 100 off", uses: "1,024 / ∞", status: ["success", "Active"] },
  { code: "MONSOON", off: "15% off", uses: "300 / 300", status: ["neutral", "Ended"] },
];

const CHANNELS = [
  { p: "whatsapp", name: "WhatsApp Business", sub: "+880 1712-xxxxxx", state: "connected" },
  { p: "messenger", name: "Facebook Messenger", sub: "Acme Store Page", state: "connected" },
  { p: "instagram", name: "Instagram Direct", sub: "Webhook returned 403", state: "error" },
  { p: "telegram", name: "Telegram Bot", sub: "Not connected", state: "disconnected" },
];
const PMETA = {
  whatsapp: "brand-whatsapp", messenger: "brand-messenger",
  instagram: "brand-instagram", telegram: "brand-telegram",
};

function ChannelCard({ c }) {
  return (
    <div className={`sv-platform sv-platform-${c.p}`}>
      <span className="sv-platform-logo"><i className={`ti ti-${PMETA[c.p]}`} /></span>
      <div className="sv-platform-meta">
        <p className="sv-platform-name">{c.name}</p>
        <p className="sv-platform-sub">{c.sub}</p>
      </div>
      {c.state === "connected" && <>
        <span className="sv-pill sv-pill-success"><span className="sv-dot" />Connected</span>
        <button className="sv-btn sv-btn-ghost sv-btn-sm"><i className="ti ti-plug-off" />Disconnect</button>
      </>}
      {c.state === "error" && <>
        <span className="sv-pill sv-pill-danger"><span className="sv-dot" />Error</span>
        <button className="sv-btn sv-btn-secondary sv-btn-sm"><i className="ti ti-refresh" />Reconnect</button>
      </>}
      {c.state === "disconnected" && (
        <button className="sv-btn sv-btn-primary sv-btn-sm"><i className="ti ti-plug-connected" />Connect</button>
      )}
    </div>
  );
}

function Products() {
  return (
    <section className="sv-card">
      <header className="sv-card-header">
        <h3 className="sv-card-title">Products <span className="sv-pill sv-pill-neutral">4</span></h3>
        <button className="sv-btn sv-btn-primary sv-btn-sm"><i className="ti ti-plus" />Add product</button>
      </header>
      <div className="sv-table-wrap" style={{ border: "none", borderRadius: 0 }}>
        <table className="sv-table">
          <thead><tr><th>Product</th><th>SKU</th><th className="sv-tnum">Price</th><th className="sv-tnum">Stock</th><th>Status</th><th></th></tr></thead>
          <tbody>
            {PRODUCTS.map((p) => (
              <tr key={p.sku}>
                <td style={{ fontWeight: 600 }}>{p.name}</td>
                <td style={{ fontFamily: "var(--sv-font-mono)", fontSize: "var(--sv-fs-xs)", color: "var(--sv-text-muted)" }}>{p.sku}</td>
                <td className="sv-tnum">{p.price}</td>
                <td className="sv-tnum">{p.stock}</td>
                <td><span className={`sv-pill sv-pill-${p.status[0]}`}>{p.status[1]}</span></td>
                <td style={{ textAlign: "right" }}><button className="sv-icon-btn" aria-label="Edit"><i className="ti ti-pencil" /></button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Coupons() {
  return (
    <section className="sv-card">
      <header className="sv-card-header">
        <h3 className="sv-card-title">Coupons</h3>
        <button className="sv-btn sv-btn-primary sv-btn-sm"><i className="ti ti-plus" />New coupon</button>
      </header>
      <div className="sv-table-wrap" style={{ border: "none", borderRadius: 0 }}>
        <table className="sv-table">
          <thead><tr><th>Code</th><th>Discount</th><th>Redeemed</th><th>Status</th></tr></thead>
          <tbody>
            {COUPONS.map((c) => (
              <tr key={c.code}>
                <td style={{ fontFamily: "var(--sv-font-mono)", fontWeight: 600 }}>{c.code}</td>
                <td>{c.off}</td>
                <td className="sv-tnum">{c.uses}</td>
                <td><span className={`sv-pill sv-pill-${c.status[0]}`}>{c.status[1]}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Channels() {
  return (
    <section className="sv-card">
      <header className="sv-card-header">
        <h3 className="sv-card-title">Connected channels</h3>
      </header>
      <div className="sv-card-body" style={{ display: "grid", gap: "var(--sv-space-3)" }}>
        {CHANNELS.map((c) => <ChannelCard c={c} key={c.p} />)}
      </div>
    </section>
  );
}

function Settings() {
  return (
    <section className="sv-card">
      <header className="sv-card-header"><h3 className="sv-card-title">Store details</h3></header>
      <div className="sv-card-body">
        <form className="sv-form" style={{ maxWidth: 520 }} onSubmit={(e) => e.preventDefault()}>
          <label className="sv-field"><span className="sv-field-label">Store name</span><input className="sv-input" defaultValue="Acme Store" /></label>
          <label className="sv-field"><span className="sv-field-label">Description<span className="sv-optional"> (used by the AI knowledge base)</span></span>
            <textarea className="sv-input" rows="3" defaultValue="Handcrafted clothing & accessories from Dhaka. Fast delivery across Bangladesh." /></label>
          <label className="sv-field"><span className="sv-field-label">Default currency</span>
            <select className="sv-input"><option>BDT (৳)</option><option>USD ($)</option><option>INR (₹)</option></select></label>
          <div style={{ display: "flex", gap: "var(--sv-space-3)" }}>
            <button className="sv-btn sv-btn-primary" type="submit"><i className="ti ti-check" />Save changes</button>
            <button className="sv-btn sv-btn-ghost" type="button">Cancel</button>
          </div>
        </form>
      </div>
    </section>
  );
}

const TABS = [
  { id: "products", label: "Products", icon: "package" },
  { id: "coupons", label: "Coupons", icon: "ticket" },
  { id: "channels", label: "Channels", icon: "plug-connected" },
  { id: "settings", label: "Settings", icon: "settings" },
];

function StoreApp() {
  const [tab, setTab] = React.useState("products");
  return (
    <main className="container" style={{ maxWidth: 960, paddingTop: "var(--sv-space-6)", paddingBottom: "var(--sv-space-8)" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "var(--sv-space-5)" }}>
        <a className="sv-brand"><span className="sv-brand-mark"><i className="ti ti-robot" /></span>Sellervai</a>
        <StoreTheme />
      </div>

      <header style={{ display: "flex", alignItems: "center", gap: "var(--sv-space-4)", marginBottom: "var(--sv-space-5)" }}>
        <span className="sv-platform-logo" style={{ background: "var(--sv-gradient)", width: "3.25rem", height: "3.25rem", borderRadius: "var(--sv-radius)" }}><i className="ti ti-building-store" /></span>
        <div style={{ flex: 1 }}>
          <h1 style={{ margin: 0 }}>Acme Store</h1>
          <p style={{ margin: 0, color: "var(--sv-text-muted)", fontSize: "var(--sv-fs-sm)" }}>store #a1f9 · 4 products · 3 channels live</p>
        </div>
        <span className="sv-pill sv-pill-success"><span className="sv-dot is-live" />AI online</span>
      </header>

      <nav style={{ display: "flex", gap: "var(--sv-space-2)", borderBottom: "1px solid var(--sv-border)", marginBottom: "var(--sv-space-5)" }}>
        {TABS.map((t) => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`sv-btn ${tab === t.id ? "sv-btn-ghost" : "sv-btn-ghost"}`}
            style={{ borderRadius: 0, borderBottom: tab === t.id ? "2px solid var(--sv-accent)" : "2px solid transparent", color: tab === t.id ? "var(--sv-accent)" : "var(--sv-text-muted)", paddingBottom: "0.75rem" }}>
            <i className={`ti ti-${t.icon}`} />{t.label}
          </button>
        ))}
      </nav>

      {tab === "products" && <Products />}
      {tab === "coupons" && <Coupons />}
      {tab === "channels" && <Channels />}
      {tab === "settings" && <Settings />}
    </main>
  );
}

Object.assign(window, { StoreApp });
