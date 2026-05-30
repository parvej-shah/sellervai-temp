from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["Pages"])


PAGE_STYLE = """
<style>
  :root {
    color-scheme: light;
  }

  body {
    margin: 0;
    padding: 24px;
    font-family: Arial, Helvetica, sans-serif;
    color: #111;
    background: #fff;
  }

  main {
    max-width: 760px;
    margin: 0 auto;
    text-align: center;
  }

  section {
    margin: 24px auto;
    padding: 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
    text-align: left;
  }

  form {
    display: grid;
    gap: 12px;
  }

  label {
    display: grid;
    gap: 6px;
  }

  input,
  textarea,
  select,
  button {
    font: inherit;
    padding: 8px 10px;
  }

  input,
  textarea,
  select {
    width: 100%;
    box-sizing: border-box;
  }

  textarea {
    min-height: 92px;
    resize: vertical;
  }

  button,
  .button {
    display: inline-block;
    width: auto;
    text-decoration: none;
    border: 1px solid #111;
    background: #111;
    color: #fff;
    cursor: pointer;
  }

  .button.secondary,
  button.secondary {
    background: #fff;
    color: #111;
  }

  .actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .grid {
    display: grid;
    gap: 16px;
  }

  .store-list {
    display: grid;
    gap: 12px;
  }

  .store-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 12px;
  }

  .muted {
    color: #666;
  }

  .small {
    font-size: 0.92rem;
  }
</style>
"""


COMMON_SCRIPT = """
<script>
const BIZZZ_TOKEN_KEY = "bizzz_token";
const BIZZZ_STORE_KEY = "bizzz_store_id";

function getToken() {
  return localStorage.getItem(BIZZZ_TOKEN_KEY) || "";
}

function setToken(token) {
  localStorage.setItem(BIZZZ_TOKEN_KEY, token);
}

function getStoreId() {
  return localStorage.getItem(BIZZZ_STORE_KEY) || "";
}

function setStoreId(storeId) {
  localStorage.setItem(BIZZZ_STORE_KEY, storeId);
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

function setMessage(elementId, text) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = text;
  }
}

function requireTokenOrRedirect() {
  if (!getToken()) {
    window.location.href = "/";
    return false;
  }

  return true;
}

function parseJsonInput(value, fallback) {
  const trimmed = String(value || "").trim();
  if (!trimmed) {
    return fallback;
  }

  try {
    return JSON.parse(trimmed);
  } catch {
    return fallback;
  }
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...authHeaders(),
    },
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(data.detail || "Request failed");
    error.data = data;
    throw error;
  }

  return data;
}

async function fetchStores() {
  return fetchJson("/api/store/");
}

function renderStoreCards(containerId, stores) {
  const container = document.getElementById(containerId);
  if (!container) {
    return;
  }

  container.innerHTML = "";

  if (!stores.length) {
    container.innerHTML = '<p class="muted">No stores yet.</p>';
    return;
  }

  for (const store of stores) {
    const card = document.createElement("div");
    card.className = "store-card";

    const title = document.createElement("h3");
    title.textContent = store.name;
    card.appendChild(title);

    const description = document.createElement("p");
    description.className = "muted small";
    description.textContent = store.description || "No description yet.";
    card.appendChild(description);

    const actions = document.createElement("div");
    actions.className = "actions";

    const openLink = document.createElement("a");
    openLink.className = "button";
    openLink.href = `/stores/${store.id}`;
    openLink.textContent = "Open store";
    openLink.addEventListener("click", () => setStoreId(store.id));
    actions.appendChild(openLink);

    card.appendChild(actions);
    container.appendChild(card);
  }
}
</script>
"""


def render_page(title: str, body: str, script: str = "") -> HTMLResponse:
    return HTMLResponse(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  {PAGE_STYLE}
</head>
<body>
  <main>
{body}
  </main>
  {COMMON_SCRIPT}
  {script}
</body>
</html>"""
    )


@router.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    body = """
<h1>Bizzz backend</h1>
<p class="muted">Temporary pages for testing. API routes stay under /api/.</p>
<div class="actions">
  <a class="button" href="/login">Login</a>
  <a class="button secondary" href="/register">Register</a>
</div>
<p class="small muted">If you are already logged in, this page will send you to the dashboard.</p>
"""
    script = """
<script>
if (getToken()) {
  window.location.href = "/dashboard";
}
</script>
"""
    return render_page("Bizzz Backend", body, script)


@router.get("/login", response_class=HTMLResponse)
async def login_page() -> HTMLResponse:
    body = """
<h1>Login</h1>
<section>
  <form id="login-form">
    <label>Email
      <input name="email" type="email" value="demo@example.com" required>
    </label>
    <label>Password
      <input name="password" type="password" value="Password123!" required>
    </label>
    <div class="actions">
      <button type="submit">Login</button>
      <a class="button secondary" href="/register">Register</a>
    </div>
  </form>
</section>
<p id="login-message" class="muted"></p>
<p><a href="/">Back</a></p>
"""
    script = """
<script>
if (getToken()) {
  window.location.href = "/dashboard";
}

document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const body = new URLSearchParams();
  body.set("username", form.get("email"));
  body.set("password", form.get("password"));

  setMessage("login-message", "Signing in...");

  try {
    const response = await fetch("/api/auth/login/docs", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      setMessage("login-message", data.detail || "Login failed");
      return;
    }

    setToken(data.access_token);
    window.location.href = "/dashboard";
  } catch (error) {
    setMessage("login-message", "Login failed");
  }
});
</script>
"""
    return render_page("Login", body, script)


@router.get("/register", response_class=HTMLResponse)
async def register_page() -> HTMLResponse:
    body = """
<h1>Register</h1>
<section>
  <form id="register-form">
    <label>Name
      <input name="name" value="Bizzz Test User" required>
    </label>
    <label>Email
      <input name="email" type="email" value="demo@example.com" required>
    </label>
    <label>Phone number
      <input name="phone_number" value="1234567890">
    </label>
    <label>Password
      <input name="password" type="password" value="Password123!" required>
    </label>
    <div class="actions">
      <button type="submit">Create account</button>
      <a class="button secondary" href="/login">Login</a>
    </div>
  </form>
</section>
<p id="register-message" class="muted"></p>
<p><a href="/">Back</a></p>
"""
    script = """
<script>
if (getToken()) {
  window.location.href = "/dashboard";
}

document.getElementById("register-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = {
    name: form.get("name"),
    email: form.get("email"),
    phone_number: form.get("phone_number") || null,
    password: form.get("password"),
  };

  setMessage("register-message", "Creating account...");

  try {
    const registerResponse = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const registerData = await registerResponse.json().catch(() => ({}));
    if (!registerResponse.ok && !String(registerData.detail || "").includes("already registered")) {
      setMessage("register-message", registerData.detail || "Registration failed");
      return;
    }

    const loginData = new URLSearchParams();
    loginData.set("username", payload.email);
    loginData.set("password", payload.password);

    const loginResponse = await fetch("/api/auth/login/docs", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: loginData,
    });

    const loginJson = await loginResponse.json().catch(() => ({}));
    if (!loginResponse.ok) {
      setMessage("register-message", loginJson.detail || "Login failed");
      return;
    }

    setToken(loginJson.access_token);
    window.location.href = "/dashboard";
  } catch (error) {
    setMessage("register-message", "Registration failed");
  }
});
</script>
"""
    return render_page("Register", body, script)


@router.get("/create-account", response_class=HTMLResponse)
async def create_account() -> HTMLResponse:
    return await register_page()


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    body = """
<h1>Dashboard</h1>
<p class="muted">Your stores live here. Open one to manage connections and store settings.</p>
<div class="actions">
  <a class="button" href="/create-store">Create store</a>
</div>
<section>
  <h2>Stores</h2>
  <div id="store-list" class="store-list"></div>
  <p id="dashboard-message" class="muted"></p>
</section>
"""
    script = """
<script>
if (!requireTokenOrRedirect()) {
  throw new Error("Missing token");
}

async function loadDashboard() {
  try {
    const stores = await fetchStores();
    renderStoreCards("store-list", stores);
    setMessage("dashboard-message", stores.length ? `Loaded ${stores.length} store(s).` : "No stores yet.");
  } catch (error) {
    setMessage("dashboard-message", error.message || "Could not load stores.");
  }
}

loadDashboard();
</script>
"""
    return render_page("Dashboard", body, script)


@router.get("/create-store", response_class=HTMLResponse)
async def create_store_page() -> HTMLResponse:
    body = """
<h1>Create store</h1>
<p class="muted">Use the placeholders below to create a starter store quickly.</p>
<section>
  <form id="create-store-form">
    <label>Name
      <input name="name" value="Demo Store" required>
    </label>
    <label>Description
      <textarea name="description">A temporary test store.</textarea>
    </label>
    <label>Tone
      <input name="tone" value="friendly">
    </label>
    <label>Personality prompt
      <textarea name="personality_prompt">Reply clearly, briefly, and helpfully.</textarea>
    </label>
    <label>Welcome message
      <textarea name="welcome_message">Welcome to Demo Store.</textarea>
    </label>
    <label>Language
      <input name="language" value="english">
    </label>
    <label>Products items JSON
      <textarea name="products_items">[{"name":"Sample Product","description":"Example item for testing","price":99}]</textarea>
    </label>
    <div class="actions">
      <button type="submit">Create store</button>
      <a class="button secondary" href="/dashboard">Back to dashboard</a>
    </div>
  </form>
</section>
<p id="create-store-message" class="muted"></p>
"""
    script = """
<script>
if (!requireTokenOrRedirect()) {
  throw new Error("Missing token");
}

document.getElementById("create-store-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);

  const payload = {
    name: form.get("name"),
    description: form.get("description") || null,
    products_items: parseJsonInput(form.get("products_items"), []),
    tone: form.get("tone") || null,
    personality_prompt: form.get("personality_prompt") || null,
    welcome_message: form.get("welcome_message") || null,
    language: form.get("language") || null,
  };

  setMessage("create-store-message", "Creating store...");

  try {
    const store = await fetchJson("/api/store/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    setStoreId(store.id);
    window.location.href = `/stores/${store.id}`;
  } catch (error) {
    setMessage("create-store-message", error.message || "Store creation failed");
  }
});
</script>
"""
    return render_page("Create store", body, script)


@router.get("/stores/{store_id}", response_class=HTMLResponse)
async def store_detail(store_id: str) -> HTMLResponse:
    body = f"""
<h1>Store</h1>
<p id="store-summary" class="muted"></p>
<div class="actions">
  <a class="button secondary" href="/dashboard">Back to dashboard</a>
  <a class="button secondary" href="/orders">Orders placeholder</a>
</div>

<section>
  <h2>Store settings</h2>
  <form id="store-settings-form">
    <label>Name
      <input name="name" value="Demo Store" required>
    </label>
    <label>Description
      <textarea name="description">What this store sells or does.</textarea>
    </label>
    <label>Tone
      <input name="tone" value="friendly">
    </label>
    <label>Personality prompt
      <textarea name="personality_prompt">Reply clearly and briefly.</textarea>
    </label>
    <label>Welcome message
      <textarea name="welcome_message">Welcome message for customers.</textarea>
    </label>
    <label>Language
      <input name="language" value="english">
    </label>
    <label>Products items JSON
      <textarea name="products_items">[{"name":"Sample Product","description":"Example item for testing","price":99}]</textarea>
    </label>
    <div class="actions">
      <button type="submit">Save store</button>
    </div>
  </form>
  <p id="store-settings-message" class="muted"></p>
</section>

<section>
  <h2>Connections</h2>

  <form class="connection-form" data-platform="messenger">
    <label>Messenger API key
      <input name="api_key" value="demo-messenger-token" required>
    </label>
    <label>Page ID
      <input name="page_id" value="1234567890">
    </label>
    <div class="actions">
      <button type="submit">Save Messenger</button>
      <button type="button" class="secondary" data-webhook="messenger">Verify webhook</button>
    </div>
  </form>

  <form class="connection-form" data-platform="whatsapp">
    <label>WhatsApp API key
      <input name="api_key" value="demo-whatsapp-token" required>
    </label>
    <label>Phone number ID
      <input name="phone_number_id" value="1234567890">
    </label>
    <label>Business account ID
      <input name="business_account_id" value="0987654321">
    </label>
    <div class="actions">
      <button type="submit">Save WhatsApp</button>
      <button type="button" class="secondary" data-webhook="whatsapp">Verify webhook</button>
    </div>
  </form>

  <form class="connection-form" data-platform="telegram">
    <label>Telegram bot token
      <input name="bot_token" value="demo-telegram-token" required>
    </label>
    <label>Bot username
      <input name="bot_username" value="demo_bot">
    </label>
    <div class="actions">
      <button type="submit">Save Telegram</button>
      <button type="button" class="secondary" data-webhook="telegram">Verify webhook</button>
    </div>
  </form>

  <form class="connection-form" data-platform="instagram">
    <label>Instagram API key
      <input name="api_key" value="demo-instagram-token" required>
    </label>
    <label>Instagram account ID
      <input name="instagram_account_id" value="1234567890">
    </label>
    <div class="actions">
      <button type="submit">Save Instagram</button>
      <button type="button" class="secondary" data-webhook="instagram">Verify webhook</button>
    </div>
  </form>

  <p id="connection-message" class="muted"></p>
</section>
"""
    script = f"""
<script>
if (!requireTokenOrRedirect()) {{
  throw new Error("Missing token");
}}

setStoreId("{store_id}");

async function loadStore() {{
  try {{
    const store = await fetchJson(`/api/store/{store_id}`);
    document.getElementById("store-summary").textContent = `${{store.name}} - ${{store.description || "No description yet."}}`;

    const settingsForm = document.getElementById("store-settings-form");
    settingsForm.elements.name.value = store.name || "";
    settingsForm.elements.description.value = store.description || "";
    settingsForm.elements.tone.value = store.tone || "";
    settingsForm.elements.personality_prompt.value = store.personality_prompt || "";
    settingsForm.elements.welcome_message.value = store.welcome_message || "";
    settingsForm.elements.language.value = store.language || "english";
    settingsForm.elements.products_items.value = JSON.stringify(store.products_items || [], null, 2);
  }} catch (error) {{
    setMessage("store-summary", error.message || "Could not load store");
  }}
}}

document.getElementById("store-settings-form").addEventListener("submit", async (event) => {{
  event.preventDefault();
  const form = new FormData(event.target);

  const payload = {{
    name: form.get("name"),
    description: form.get("description") || null,
    products_items: parseJsonInput(form.get("products_items"), []),
    tone: form.get("tone") || null,
    personality_prompt: form.get("personality_prompt") || null,
    welcome_message: form.get("welcome_message") || null,
    language: form.get("language") || null,
  }};

  setMessage("store-settings-message", "Saving store...");

  try {{
    await fetchJson(`/api/store/{store_id}`, {{
      method: "PUT",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(payload),
    }});

    setMessage("store-settings-message", "Store saved.");
  }} catch (error) {{
    setMessage("store-settings-message", error.message || "Could not save store");
  }}
}});

document.querySelectorAll(".connection-form").forEach((form) => {{
  form.addEventListener("submit", async (event) => {{
    event.preventDefault();
    const platform = form.dataset.platform;
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    setMessage("connection-message", `Saving ${{platform}}...`);

    try {{
      await fetchJson(`/api/setup/${{platform}}/{store_id}/api-key`, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify(payload),
      }});

      setMessage("connection-message", `${{platform}} saved.`);
    }} catch (error) {{
      setMessage("connection-message", error.message || `Saving ${{platform}} failed`);
    }}
  }});
}});

document.querySelectorAll("button[data-webhook]").forEach((button) => {{
  button.addEventListener("click", async () => {{
    const platform = button.dataset.webhook;

    setMessage("connection-message", `Verifying ${{platform}} webhook...`);

    try {{
      await fetchJson(`/api/setup/${{platform}}/{store_id}/webhook`, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
      }});

      setMessage("connection-message", `${{platform}} webhook verified.`);
    }} catch (error) {{
      setMessage("connection-message", error.message || `Webhook verification failed for ${{platform}}`);
    }}
  }});
}});

loadStore();
</script>
"""
    return render_page(f"Store {store_id}", body, script)


@router.get("/connections", response_class=HTMLResponse)
async def connections() -> HTMLResponse:
    body = """
<h1>Connections</h1>
<p class="muted">Open a store from the dashboard, then manage its platform connections here.</p>
<div class="actions">
  <a class="button" href="/dashboard">Go to dashboard</a>
</div>
<p class="small muted">This page will jump to the last selected store if one is saved.</p>
"""
    script = """
<script>
if (!requireTokenOrRedirect()) {
  throw new Error("Missing token");
}

const storeId = getStoreId();
if (storeId) {
  window.location.href = `/stores/${storeId}`;
}
</script>
"""
    return render_page("Connections", body, script)


@router.get("/orders", response_class=HTMLResponse)
async def orders() -> HTMLResponse:
    body = """
<h1>Orders</h1>
<p class="muted">Placeholder for now. The order flow can be added later in the separate frontend.</p>
<div class="actions">
  <a class="button" href="/dashboard">Back to dashboard</a>
</div>
"""
    return render_page("Orders", body)