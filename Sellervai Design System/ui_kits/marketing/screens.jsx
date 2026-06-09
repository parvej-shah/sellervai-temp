/* Sellervai — Marketing + Auth UI kit screens (self-contained demo).
   Mirrors the live Mako templates (index/login/register) restyled under
   the new tokens. Components emit the same .sv-* classes the system ships. */

function ThemeToggle() {
  const [theme, setTheme] = React.useState(
    () => document.documentElement.dataset.theme || "light"
  );
  React.useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("sv-theme", theme); } catch (e) {}
  }, [theme]);
  return (
    <button
      className="sv-theme-toggle"
      aria-label="Toggle theme"
      onClick={() => setTheme((t) => (t === "dark" ? "light" : "dark"))}
    >
      <i className="ti ti-sun" /><i className="ti ti-moon" />
    </button>
  );
}

function NavBar({ go, current }) {
  return (
    <nav className="container-fluid sv-nav" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
      <a className="sv-brand" href="#" onClick={(e) => { e.preventDefault(); go("home"); }}>
        <span className="sv-brand-mark"><i className="ti ti-robot" /></span>
        Sellervai
      </a>
      <div className="sv-nav-actions">
        <ThemeToggle />
        {current !== "login" && (
          <button className="sv-btn sv-btn-ghost" onClick={() => go("login")}>Sign in</button>
        )}
        {current !== "register" && (
          <button className="sv-btn sv-btn-hero" onClick={() => go("register")}>
            <i className="ti ti-rocket" /> Get started
          </button>
        )}
      </div>
    </nav>
  );
}

const FEATURES = [
  { icon: "messages", title: "Multi-platform messaging", body: "Handle WhatsApp, Messenger, Instagram DMs, and Telegram from one unified inbox." },
  { icon: "brain", title: "AI chat assistant", body: "DeepSeek-powered AI answers questions, suggests products, and closes sales 24/7." },
  { icon: "database", title: "Smart knowledge base", body: "Upload PDFs, product lists, and docs — the AI learns your catalogue automatically." },
  { icon: "chart-bar", title: "Live dashboard", body: "Monitor conversations, orders, and performance metrics in real time with HTMX updates." },
  { icon: "plug-connected", title: "One-click integrations", body: "Connect Facebook, Instagram, and WhatsApp via OAuth in seconds — no API keys needed." },
  { icon: "lock", title: "Secure & private", body: "All tokens are encrypted at rest. Your data never leaves your own database." },
];

function HomeScreen({ go }) {
  return (
    <main className="container sv-main">
      <section className="sv-hero">
        <div>
          <span className="sv-badge"><i className="ti ti-sparkles" /> AI-Powered</span>
          <h1>Automate your store with&nbsp;<em>intelligent</em>&nbsp;AI</h1>
          <p>
            Sellervai connects your store to WhatsApp, Facebook, Instagram, and
            Telegram — letting your AI assistant handle messages, orders, and
            customer support around the clock.
          </p>
          <div className="sv-hero-actions">
            <button className="sv-btn sv-btn-hero" onClick={() => go("register")}>
              <i className="ti ti-rocket" /> Start for free
            </button>
            <button className="sv-btn sv-btn-secondary sv-btn-lg" onClick={() => go("login")}>Sign in</button>
          </div>
        </div>
        <div className="sv-hero-visual" aria-hidden="true">
          <i className="ti ti-robot sv-hero-icon" />
        </div>
      </section>

      <section>
        <h2 className="sv-section-title">Everything you need to sell smarter</h2>
        <div className="sv-feature-grid">
          {FEATURES.map((f) => (
            <article className="sv-feature-card" key={f.title}>
              <span className="sv-feature-icon"><i className={`ti ti-${f.icon}`} /></span>
              <h3>{f.title}</h3>
              <p>{f.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2 className="sv-section-title">Platform status</h2>
        <div className="sv-status-box">
          <span className="sv-pill sv-pill-success"><span className="sv-dot is-live" /> All systems operational</span>
          <span>Webhooks, AI agent, and database responding normally.</span>
        </div>
      </section>
    </main>
  );
}

function AuthShell({ children }) {
  return <main className="container"><div className="sv-auth-wrap">{children}</div></main>;
}

function LoginScreen({ go }) {
  const [err, setErr] = React.useState(false);
  return (
    <AuthShell>
      <div className="sv-auth-card">
        <div className="sv-auth-header">
          <span className="sv-auth-logo"><i className="ti ti-robot" /></span>
          <h1>Welcome back</h1>
          <p>Sign in to your Sellervai account</p>
        </div>
        <div className="sv-google-btn-wrap">
          <button className="sv-google-btn"><i className="ti ti-brand-google" /> Sign in with Google</button>
        </div>
        <div className="sv-divider"><span>or continue with email</span></div>
        <form className="sv-form" onSubmit={(e) => { e.preventDefault(); setErr(true); }}>
          <label className="sv-field">
            <span className="sv-field-label">Email</span>
            <input className="sv-input" type="email" placeholder="you@example.com" defaultValue="owner@acmestore.com" />
          </label>
          <label className="sv-field">
            <span className="sv-field-label">Password</span>
            <input className={`sv-input${err ? " is-invalid" : ""}`} type="password" placeholder="••••••••" />
          </label>
          {err && <p className="sv-field-error">Incorrect email or password. Please try again.</p>}
          <button className="sv-btn sv-btn-primary" type="submit" style={{ width: "100%", marginTop: 4 }}>
            <i className="ti ti-login" /> Sign in
          </button>
        </form>
        <p className="sv-auth-footer">
          No account? <a href="#" onClick={(e) => { e.preventDefault(); go("register"); }}>Create one</a>
        </p>
      </div>
    </AuthShell>
  );
}

function RegisterScreen({ go }) {
  return (
    <AuthShell>
      <div className="sv-auth-card">
        <div className="sv-auth-header">
          <span className="sv-auth-logo"><i className="ti ti-rocket" /></span>
          <h1>Get started</h1>
          <p>Create your free Sellervai account</p>
        </div>
        <div className="sv-google-btn-wrap">
          <button className="sv-google-btn"><i className="ti ti-brand-google" /> Sign up with Google</button>
        </div>
        <div className="sv-divider"><span>or register with email</span></div>
        <form className="sv-form" onSubmit={(e) => { e.preventDefault(); go("home"); }}>
          <label className="sv-field"><span className="sv-field-label">Name</span><input className="sv-input" placeholder="Your name" /></label>
          <label className="sv-field"><span className="sv-field-label">Email</span><input className="sv-input" type="email" placeholder="you@example.com" /></label>
          <label className="sv-field"><span className="sv-field-label">Phone<span className="sv-optional"> (optional)</span></span><input className="sv-input" type="tel" placeholder="+880…" /></label>
          <label className="sv-field"><span className="sv-field-label">Password</span><input className="sv-input" type="password" placeholder="Min 8 characters" /></label>
          <button className="sv-btn sv-btn-primary" type="submit" style={{ width: "100%", marginTop: 4 }}>
            <i className="ti ti-user-plus" /> Create account
          </button>
        </form>
        <p className="sv-auth-footer">
          Already have an account? <a href="#" onClick={(e) => { e.preventDefault(); go("login"); }}>Sign in</a>
        </p>
      </div>
    </AuthShell>
  );
}

function MarketingApp() {
  const [screen, setScreen] = React.useState("home");
  const go = (s) => setScreen(s);
  return (
    <>
      <NavBar go={go} current={screen} />
      {screen === "home" && <HomeScreen go={go} />}
      {screen === "login" && <LoginScreen go={go} />}
      {screen === "register" && <RegisterScreen go={go} />}
      <footer className="container sv-footer">
        <small>© 2025 Sellervai — AI-powered store automation</small>
      </footer>
    </>
  );
}

Object.assign(window, { MarketingApp });
