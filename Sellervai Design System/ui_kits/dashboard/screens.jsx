/* Sellervai — Dashboard UI kit (proposed per the design brief — the live
   app does not yet ship a dashboard template). Shell + overview screen,
   built from the system's .sv-* component classes. */

function Sidebar({ active, go }) {
  const Item = ({ id, icon, label, badge }) => (
    <a className={`sv-side-link${active === id ? " is-active" : ""}`}
       onClick={(e) => { e.preventDefault(); go(id); }}>
      <i className={`ti ti-${icon}`} />{label}
      {badge != null && <span className={`sv-pill sv-pill-${badge.tone} sv-side-badge`}>{badge.text}</span>}
    </a>
  );
  return (
    <aside className="sv-sidebar">
      <a className="sv-brand"><span className="sv-brand-mark"><i className="ti ti-robot" /></span>Sellervai</a>
      <Item id="overview" icon="layout-dashboard" label="Overview" />
      <Item id="inbox" icon="messages" label="Conversations" badge={{ tone: "info", text: "6" }} />
      <Item id="orders" icon="shopping-bag" label="Orders" />
      <Item id="products" icon="package" label="Products" />
      <Item id="coupons" icon="ticket" label="Coupons" />
      <div className="sv-side-section">Setup</div>
      <Item id="channels" icon="plug-connected" label="Channels" />
      <Item id="kb" icon="database" label="Knowledge base" />
      <Item id="settings" icon="settings" label="Settings" />
      <div className="sv-side-foot">
        <span className="sv-avatar">AS</span>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div className="sv-convo-name">Acme Store</div>
          <div className="sv-convo-time">owner@acmestore.com</div>
        </div>
      </div>
    </aside>
  );
}

function DashTheme() {
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

const PLAT = {
  whatsapp: { v: "var(--sv-whatsapp)", icon: "brand-whatsapp" },
  messenger: { v: "var(--sv-messenger)", icon: "brand-messenger" },
  instagram: { v: "var(--sv-instagram)", icon: "brand-instagram" },
  telegram: { v: "var(--sv-telegram)", icon: "brand-telegram" },
};
function PlatDot({ p }) {
  const m = PLAT[p];
  return <span className="sv-plat-dot" style={{ background: m.v }}><i className={`ti ti-${m.icon}`} /></span>;
}

const CONVOS = [
  { p: "whatsapp", name: "Rahima K.", msg: "Do you have the blue kurti in medium?", time: "2m" },
  { p: "messenger", name: "Tanvir A.", msg: "Order #10482 — when will it ship?", time: "11m" },
  { p: "instagram", name: "@sadia.styles", msg: "Is the discount code still valid?", time: "23m" },
  { p: "telegram", name: "Imran H.", msg: "Thanks! The AI answered everything 👍", time: "1h" },
];

const ORDERS = [
  { id: "#ORD-10482", cust: "Tanvir Ahmed", items: 2, total: "৳ 2,400", status: ["success", "Paid"] },
  { id: "#ORD-10481", cust: "Rahima Khatun", items: 1, total: "৳ 890", status: ["warning", "Pending"] },
  { id: "#ORD-10480", cust: "Sadia R.", items: 4, total: "৳ 5,120", status: ["success", "Paid"] },
  { id: "#ORD-10479", cust: "Imran Hossain", items: 1, total: "৳ 1,250", status: ["danger", "Failed"] },
];

function Overview() {
  return (
    <div className="sv-content">
      <div className="sv-stat-grid">
        <article className="sv-stat">
          <div className="sv-stat-head"><span className="sv-stat-label">Conversations today</span><span className="sv-stat-icon"><i className="ti ti-messages" /></span></div>
          <div className="sv-stat-value sv-tnum">248</div>
          <span className="sv-stat-delta is-up"><i className="ti ti-trending-up" />+12% vs yesterday</span>
        </article>
        <article className="sv-stat">
          <div className="sv-stat-head"><span className="sv-stat-label">Orders today</span><span className="sv-stat-icon"><i className="ti ti-shopping-bag" /></span></div>
          <div className="sv-stat-value sv-tnum">37</div>
          <span className="sv-stat-delta is-down"><i className="ti ti-trending-down" />-4% vs yesterday</span>
        </article>
        <article className="sv-stat">
          <div className="sv-stat-head"><span className="sv-stat-label">Revenue today</span><span className="sv-stat-icon"><i className="ti ti-coin" /></span></div>
          <div className="sv-stat-value sv-tnum">৳ 84,200</div>
          <span className="sv-stat-delta is-up"><i className="ti ti-trending-up" />+8%</span>
        </article>
        <article className="sv-stat">
          <div className="sv-stat-head"><span className="sv-stat-label">AI agent</span><span className="sv-stat-icon"><i className="ti ti-robot" /></span></div>
          <div className="sv-stat-value" style={{ fontSize: "var(--sv-fs-lg)" }}>
            <span className="sv-pill sv-pill-success"><span className="sv-dot is-live" />Online</span>
          </div>
          <span className="sv-convo-time">RAG synced · 1,204 docs indexed</span>
        </article>
      </div>

      <div className="sv-alert sv-alert-warning">
        <i className="ti ti-alert-triangle" />
        <div><p className="sv-alert-title">WhatsApp token expires in 3 days</p><p>Reconnect the channel to keep automated replies running.</p></div>
      </div>

      <div className="sv-grid-2">
        <section className="sv-card">
          <header className="sv-card-header">
            <h3 className="sv-card-title">Recent conversations</h3>
            <button className="sv-btn sv-btn-ghost sv-btn-sm">Open inbox<i className="ti ti-chevron-right" /></button>
          </header>
          <div className="sv-card-body" style={{ paddingTop: 0, paddingBottom: 0 }}>
            {CONVOS.map((c) => (
              <div className="sv-convo" key={c.name}>
                <PlatDot p={c.p} />
                <div className="sv-convo-body">
                  <div className="sv-convo-name">{c.name}</div>
                  <div className="sv-convo-msg">{c.msg}</div>
                </div>
                <span className="sv-convo-time">{c.time}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="sv-card">
          <header className="sv-card-header">
            <h3 className="sv-card-title">Channels</h3>
            <button className="sv-btn sv-btn-ghost sv-btn-sm">Manage<i className="ti ti-chevron-right" /></button>
          </header>
          <div className="sv-card-body" style={{ display: "grid", gap: "var(--sv-space-3)" }}>
            <div className="sv-platform sv-platform-whatsapp" style={{ boxShadow: "none", padding: "var(--sv-space-3) var(--sv-space-4)" }}>
              <span className="sv-platform-logo"><i className="ti ti-brand-whatsapp" /></span>
              <div className="sv-platform-meta"><p className="sv-platform-name">WhatsApp</p><p className="sv-platform-sub">+880 1712-xxxxxx</p></div>
              <span className="sv-pill sv-pill-success"><span className="sv-dot" />Connected</span>
            </div>
            <div className="sv-platform sv-platform-messenger" style={{ boxShadow: "none", padding: "var(--sv-space-3) var(--sv-space-4)" }}>
              <span className="sv-platform-logo"><i className="ti ti-brand-messenger" /></span>
              <div className="sv-platform-meta"><p className="sv-platform-name">Messenger</p><p className="sv-platform-sub">Acme Store Page</p></div>
              <span className="sv-pill sv-pill-success"><span className="sv-dot" />Connected</span>
            </div>
            <div className="sv-platform sv-platform-instagram" style={{ boxShadow: "none", padding: "var(--sv-space-3) var(--sv-space-4)" }}>
              <span className="sv-platform-logo"><i className="ti ti-brand-instagram" /></span>
              <div className="sv-platform-meta"><p className="sv-platform-name">Instagram</p><p className="sv-platform-sub">Webhook returned 403</p></div>
              <span className="sv-pill sv-pill-danger"><span className="sv-dot" />Error</span>
            </div>
            <div className="sv-platform sv-platform-telegram" style={{ boxShadow: "none", padding: "var(--sv-space-3) var(--sv-space-4)" }}>
              <span className="sv-platform-logo"><i className="ti ti-brand-telegram" /></span>
              <div className="sv-platform-meta"><p className="sv-platform-name">Telegram</p><p className="sv-platform-sub">Not connected</p></div>
              <button className="sv-btn sv-btn-primary sv-btn-sm"><i className="ti ti-plug-connected" />Connect</button>
            </div>
          </div>
        </section>
      </div>

      <section className="sv-card">
        <header className="sv-card-header">
          <h3 className="sv-card-title">Recent orders</h3>
          <button className="sv-btn sv-btn-secondary sv-btn-sm"><i className="ti ti-download" />Export CSV</button>
        </header>
        <div className="sv-table-wrap" style={{ border: "none", borderRadius: 0 }}>
          <table className="sv-table">
            <thead><tr><th>Order</th><th>Customer</th><th>Items</th><th className="sv-tnum">Total</th><th>Status</th><th></th></tr></thead>
            <tbody>
              {ORDERS.map((o) => (
                <tr key={o.id}>
                  <td style={{ fontFamily: "var(--sv-font-mono)", fontSize: "var(--sv-fs-xs)" }}>{o.id}</td>
                  <td>{o.cust}</td>
                  <td className="sv-tnum">{o.items}</td>
                  <td className="sv-tnum">{o.total}</td>
                  <td><span className={`sv-pill sv-pill-${o.status[0]}`}>{o.status[1]}</span></td>
                  <td style={{ textAlign: "right" }}><button className="sv-icon-btn" aria-label="Actions"><i className="ti ti-dots-vertical" /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

const PLACEHOLDER = {
  inbox: "Conversations", orders: "Orders", products: "Products", coupons: "Coupons",
  channels: "Channels", kb: "Knowledge base", settings: "Settings",
};

function DashboardApp() {
  const [active, setActive] = React.useState("overview");
  const title = active === "overview" ? "Overview" : PLACEHOLDER[active];
  return (
    <div className="sv-shell">
      <Sidebar active={active} go={setActive} />
      <div>
        <header className="sv-topbar">
          <h1>{title}</h1>
          <div className="sv-topbar-actions">
            <button className="sv-icon-btn" aria-label="Search"><i className="ti ti-search" /></button>
            <button className="sv-icon-btn" aria-label="Notifications"><i className="ti ti-bell" /></button>
            <DashTheme />
            <button className="sv-btn sv-btn-primary sv-btn-sm"><i className="ti ti-plus" />New product</button>
          </div>
        </header>
        {active === "overview" ? <Overview /> : (
          <div className="sv-content">
            <div className="sv-card"><div className="sv-empty">
              <span className="sv-empty-icon"><i className="ti ti-layout-grid" /></span>
              <h3>{title}</h3>
              <p>This screen is part of the dashboard shell. The Overview screen demonstrates the full component set.</p>
              <button className="sv-btn sv-btn-secondary" onClick={() => setActive("overview")}>Back to Overview</button>
            </div></div>
          </div>
        )}
      </div>
    </div>
  );
}

Object.assign(window, { DashboardApp });
