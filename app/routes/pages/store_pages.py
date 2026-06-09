from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .common import render_page
from app.lib.config import settings

router = APIRouter()

@router.get("/stores/{store_id}", response_class=HTMLResponse)
async def store_detail(store_id: str):
    body = f"""
<section class="sv-page-header">
  <div class="sv-page-title">
    <h1>Store workspace</h1>
    <p id="store-summary" class="sv-page-lead">Loading store details...</p>
  </div>
  <div class="sv-page-actions">
    <a class="sv-btn sv-btn-secondary" href="/dashboard">Back to dashboard</a>
    <a class="sv-btn sv-btn-secondary" href="/orders">Orders placeholder</a>
    <a class="sv-btn sv-btn-primary" href="/posts/{store_id}"><i class="ti ti-brand-instagram"></i> Post management</a>
  </div>
</section>

<section class="sv-card">
  <header class="sv-card-header">
    <h2 class="sv-card-title"><i class="ti ti-settings"></i> Store settings</h2>
  </header>
  <div class="sv-card-body sv-stack">
    <form id="store-settings-form" class="sv-form">
      <div class="sv-form-grid">
        <label class="sv-field">
          <span class="sv-field-label">Name</span>
          <input name="name" value="Demo Store" required>
        </label>
        <label class="sv-field">
          <span class="sv-field-label">Tone</span>
          <input name="tone" value="friendly">
        </label>
        <label class="sv-field is-span-2">
          <span class="sv-field-label">Description</span>
          <textarea name="description">What this store sells or does.</textarea>
        </label>
        <label class="sv-field is-span-2">
          <span class="sv-field-label">Personality prompt</span>
          <textarea name="personality_prompt">Reply clearly and briefly.</textarea>
        </label>
        <label class="sv-field is-span-2">
          <span class="sv-field-label">Welcome message</span>
          <textarea name="welcome_message">Welcome message for customers.</textarea>
        </label>
        <label class="sv-field">
          <span class="sv-field-label">Language</span>
          <select name="language">
            <option value="adaptive">Adaptive (auto-detect)</option>
            <option value="english">English</option>
            <option value="bangla">Bangla</option>
          </select>
        </label>
        <label class="sv-field">
          <span class="sv-field-label">Orders</span>
          <span class="sv-toggle-row">
            <input type="checkbox" name="orders_enabled" id="orders-enabled-toggle">
            <span>Accept orders automatically</span>
          </span>
        </label>
      </div>
      <div class="sv-page-actions">
        <button type="submit" class="sv-btn sv-btn-primary"><i class="ti ti-device-floppy"></i> Save store</button>
      </div>
    </form>
    <p id="store-settings-message" class="sv-muted"></p>
  </div>
</section>

<section class="sv-card">
  <header class="sv-card-header">
    <h2 class="sv-card-title"><i class="ti ti-package"></i> Products</h2>
    <button type="button" class="sv-btn sv-btn-primary sv-btn-sm" id="btn-add-product"><i class="ti ti-plus"></i> Add product</button>
  </header>
  <div class="sv-card-body sv-stack">
    <p class="sv-muted">Manage the products available in your store.</p>
    <div id="product-form-wrap" class="sv-card sv-hidden">
      <div class="sv-card-body">
        <form id="product-form" class="sv-form">
      <input type="hidden" name="product_id">
          <div class="sv-form-grid">
            <label class="sv-field"><span class="sv-field-label">Product code</span><input name="product_code" placeholder="e.g. SKU-001" required></label>
            <label class="sv-field"><span class="sv-field-label">Name</span><input name="name" placeholder="Product name" required></label>
            <label class="sv-field is-span-2"><span class="sv-field-label">Description</span><textarea name="description" placeholder="Optional description"></textarea></label>
            <label class="sv-field"><span class="sv-field-label">Image URL</span><input name="image" placeholder="https://..."></label>
            <label class="sv-field"><span class="sv-field-label">Price</span><input name="price" type="number" step="0.01" min="0" required></label>
            <label class="sv-field"><span class="sv-field-label">Discount</span><input name="discount" type="number" step="0.01" min="0" placeholder="0"></label>
            <label class="sv-field"><span class="sv-field-label">Stock count</span><input name="available_count" type="number" min="0" value="0" required></label>
            <label class="sv-field"><span class="sv-field-label">Availability</span><span class="sv-toggle-row"><input type="checkbox" name="enabled" checked><span>Enabled</span></span></label>
          </div>
          <div class="sv-page-actions">
            <button type="submit" class="sv-btn sv-btn-primary">Save product</button>
            <button type="button" class="sv-btn sv-btn-secondary" id="btn-cancel-product">Cancel</button>
          </div>
        </form>
        <p id="product-form-msg" class="sv-muted"></p>
      </div>
    </div>
    <div id="products-list"><p class="sv-muted">Loading products...</p></div>
  </div>
</section>

<section class="sv-card">
  <header class="sv-card-header">
    <h2 class="sv-card-title"><i class="ti ti-ticket"></i> Coupons</h2>
    <button type="button" class="sv-btn sv-btn-primary sv-btn-sm" id="btn-add-coupon"><i class="ti ti-plus"></i> Add coupon</button>
  </header>
  <div class="sv-card-body sv-stack">
    <p class="sv-muted">Create discount coupons for your customers.</p>
    <div id="coupon-form-wrap" class="sv-card sv-hidden">
      <div class="sv-card-body">
        <form id="coupon-form" class="sv-form">
      <input type="hidden" name="coupon_id">
          <div class="sv-form-grid">
            <label class="sv-field"><span class="sv-field-label">Code</span><input name="code" placeholder="e.g. SAVE10" required></label>
            <label class="sv-field"><span class="sv-field-label">Description</span><input name="description" placeholder="Optional"></label>
            <label class="sv-field"><span class="sv-field-label">Discount amount</span><input name="discount_amount" type="number" step="0.01" min="0" placeholder="0"></label>
            <label class="sv-field"><span class="sv-field-label">Discount %</span><input name="discount_percent" type="number" step="0.01" min="0" max="100" placeholder="0"></label>
            <label class="sv-field"><span class="sv-field-label">Min order amount</span><input name="min_order_amount" type="number" step="0.01" min="0" placeholder="0"></label>
            <label class="sv-field"><span class="sv-field-label">Max uses</span><input name="max_uses" type="number" min="1" placeholder="Unlimited"></label>
            <label class="sv-field"><span class="sv-field-label">Expires at</span><input name="expires_at" type="datetime-local"></label>
            <label class="sv-field"><span class="sv-field-label">Availability</span><span class="sv-toggle-row"><input type="checkbox" name="enabled" checked><span>Enabled</span></span></label>
          </div>
          <div class="sv-page-actions">
            <button type="submit" class="sv-btn sv-btn-primary">Save coupon</button>
            <button type="button" class="sv-btn sv-btn-secondary" id="btn-cancel-coupon">Cancel</button>
          </div>
        </form>
        <p id="coupon-form-msg" class="sv-muted"></p>
      </div>
    </div>
    <div id="coupons-list"><p class="sv-muted">Loading coupons...</p></div>
  </div>
</section>

<section class="sv-card">
  <header class="sv-card-header">
    <h2 class="sv-card-title"><i class="ti ti-shopping-cart"></i> Orders</h2>
  </header>
  <div class="sv-card-body sv-stack">
    <p class="sv-muted">View and manage orders placed through chatbot.</p>
    <div class="sv-toolbar">
      <select id="order-status-filter">
      <option value="">All statuses</option>
      <option value="PENDING">Pending</option>
      <option value="CONFIRMED">Confirmed</option>
      <option value="PROCESSING">Processing</option>
      <option value="SHIPPED">Shipped</option>
      <option value="DELIVERED">Delivered</option>
      <option value="CANCELLED">Cancelled</option>
    </select>
      <button type="button" id="btn-refresh-orders" class="sv-btn sv-btn-secondary">Refresh</button>
    </div>
    <div id="orders-list"><p class="sv-muted">Loading orders...</p></div>
  </div>
</section>

<section class="sv-grid-auto">
  <article class="sv-card">
    <header class="sv-card-header">
      <h2 class="sv-card-title"><i class="ti ti-brand-messenger"></i> Meta connections</h2>
    </header>
    <div class="sv-card-body sv-stack">
      <div class="sv-stack-sm">
        <h3>Facebook Messenger</h3>
        <p class="sv-muted">Connect your Facebook Page for Messenger.</p>
        <div id="facebook-connections-list"></div>
        <div class="sv-inline-actions">
          <button type="button" class="sv-btn sv-btn-primary" id="btn-connect-facebook">Connect Facebook</button>
        </div>
      </div>

      <div class="sv-section-divider sv-stack-sm">
        <h3>Instagram</h3>
        <p class="sv-muted">Connect your Instagram Business account. It must already be linked to a Facebook Page.</p>
        <div id="instagram-connections-list"></div>
        <form id="form-connect-instagram" class="sv-form">
          <label class="sv-field">
            <span class="sv-field-label">User access token <span class="sv-optional">(optional manual fallback)</span></span>
            <input name="user_access_token" placeholder="Paste Graph API Explorer token if OAuth fails...">
          </label>
          <div class="sv-inline-actions">
            <button type="button" class="sv-btn sv-btn-primary" id="btn-connect-instagram-oauth">Connect via OAuth</button>
            <button type="submit" class="sv-btn sv-btn-secondary">Connect with token</button>
          </div>
        </form>
      </div>
    </div>
  </article>

  <article class="sv-card">
    <header class="sv-card-header">
      <h2 class="sv-card-title"><i class="ti ti-brand-whatsapp"></i> WhatsApp</h2>
    </header>
    <div class="sv-card-body sv-stack">
      <p class="sv-muted">Connect WhatsApp Business using Embedded Signup credentials.</p>
      <div id="whatsapp-connections-list"></div>
      <div class="sv-inline-actions">
        <button type="button" class="sv-btn sv-btn-primary" id="btn-connect-whatsapp">Connect WhatsApp</button>
      </div>
    </div>
  </article>
</section>

<section class="sv-grid-auto">
  <article class="sv-card">
    <header class="sv-card-header">
      <h2 class="sv-card-title"><i class="ti ti-webhook"></i> Global Meta webhook</h2>
    </header>
    <div class="sv-card-body sv-stack">
      <p class="sv-muted">Configure this single webhook URL in your Meta App Dashboard. It handles Messenger, Instagram, and WhatsApp.</p>
      <label class="sv-field">
        <span class="sv-field-label">Webhook URL</span>
        <input id="webhook-url-meta" readonly>
      </label>
      <div class="sv-inline-actions">
        <button type="button" class="sv-btn sv-btn-secondary" data-copy-webhook="meta">Copy webhook URL</button>
      </div>
    </div>
  </article>

  <article class="sv-card">
    <header class="sv-card-header">
      <h2 class="sv-card-title"><i class="ti ti-brand-telegram"></i> Telegram</h2>
    </header>
    <div class="sv-card-body sv-stack">
      <div id="telegram-connections-list"></div>
      <form class="connection-form sv-form" data-platform="telegram">
        <div class="sv-form-grid">
          <label class="sv-field">
            <span class="sv-field-label">Telegram bot token</span>
            <input name="bot_token" value="demo-telegram-token" required>
          </label>
          <label class="sv-field">
            <span class="sv-field-label">Bot username</span>
            <input name="bot_username" value="demo_bot">
          </label>
          <label class="sv-field is-span-2">
            <span class="sv-field-label">Webhook URL</span>
            <input id="webhook-url-telegram" readonly>
          </label>
        </div>
        <div class="sv-inline-actions">
          <button type="button" class="sv-btn sv-btn-secondary" data-copy-webhook="telegram">Copy webhook URL</button>
          <button type="submit" class="sv-btn sv-btn-primary">Save Telegram</button>
          <button type="button" class="sv-btn sv-btn-secondary" data-webhook="telegram">Verify webhook</button>
        </div>
      </form>
      <p id="connection-message" class="sv-muted"></p>
    </div>
  </article>
</section>
"""
    script = f"""
<script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js"></script>
<script>
  window.fbAsyncInit = function() {{
    FB.init({{
      appId      : '{settings.META_APP_ID}',
      cookie     : true,
      xfbml      : true,
      version    : 'v25.0'
    }});
  }};
</script>
<script>
setStoreId("{store_id}");
const webhookPlatforms = ["telegram"];
function webhookUrl(platform) {{ 
    if (platform === "meta") return `${{window.location.origin}}/api/webhooks/meta`;
    return `${{window.location.origin}}/api/webhooks/${{platform}}/{store_id}`; 
}}
function renderWebhookUrls() {{ 
    webhookPlatforms.forEach((platform) => {{ const input = document.getElementById(`webhook-url-${{platform}}`); if (input) {{ input.value = webhookUrl(platform); }} }}); 
    const metaInput = document.getElementById("webhook-url-meta");
    if (metaInput) metaInput.value = webhookUrl("meta");
}}
ensureSessionOrRedirect().then((session) => {{ if (!session) {{ return; }} renderWebhookUrls(); loadStore(); loadProducts(); loadCoupons(); loadOrders(); loadConnections(); }}).catch((error) => {{ showError(error.message || "Session check failed"); }});

// ---- Store settings ----
async function loadStore() {{
  try {{
    const store = await fetchJson(`/api/store/{store_id}`);
    document.getElementById("store-summary").textContent = `${{store.name}} - ${{store.description || "No description yet."}}`;
    const f = document.getElementById("store-settings-form");
    f.elements.name.value = store.name || "";
    f.elements.description.value = store.description || "";
    f.elements.tone.value = store.tone || "";
    f.elements.personality_prompt.value = store.personality_prompt || "";
    f.elements.welcome_message.value = store.welcome_message || "";
    f.elements.language.value = store.language || "adaptive";
    f.elements.orders_enabled.checked = store.orders_enabled !== false;
    const tokenInput = document.getElementById("store-verification-token");
    if (tokenInput) tokenInput.value = store.verification_token || "";
  }} catch (error) {{ setMessage("store-summary", error.message || "Could not load store"); }}
}}
document.getElementById("store-settings-form").addEventListener("submit", async (event) => {{
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = {{
    name: form.get("name"),
    description: form.get("description") || null,
    tone: form.get("tone") || null,
    personality_prompt: form.get("personality_prompt") || null,
    welcome_message: form.get("welcome_message") || null,
    language: form.get("language") || "adaptive",
    orders_enabled: form.get("orders_enabled") === "on",
  }};
  setMessage("store-settings-message", "Saving store...");
  try {{
    await fetchJson(`/api/store/{store_id}`, {{ method: "PUT", headers: {{"Content-Type":"application/json"}}, body: JSON.stringify(payload) }});
    setMessage("store-settings-message", "Store saved.");
  }} catch (error) {{ setMessage("store-settings-message", error.message || "Could not save store"); }}
}});
/*
document.getElementById("copy-store-verification-token").addEventListener("click", async () => {{
  const tokenInput = document.getElementById("store-verification-token");
  const button = document.getElementById("copy-store-verification-token");
  try {{
    await copyText(tokenInput?.value || "");
    const label = button.querySelector("span:last-child");
    if (label) {{ label.textContent = "Copied"; setTimeout(() => {{ label.textContent = "Copy token"; }}, 1500); }}
    setMessage("connection-message", "Verification token copied.");
  }} catch (error) {{ setMessage("connection-message", error.message || "Could not copy"); }}
}});
*/
document.querySelectorAll("button[data-copy-webhook]").forEach((button) => {{
  button.addEventListener("click", async () => {{
    const url = webhookUrl(button.dataset.copyWebhook);
    try {{
      await copyText(url);
      button.textContent = "Copied"; setTimeout(() => {{ button.textContent = "Copy webhook URL"; }}, 1500);
    }} catch (error) {{ setMessage("connection-message", error.message || "Could not copy"); }}
  }});
}});
document.querySelectorAll(".connection-form").forEach((form) => {{
  form.addEventListener("submit", async (event) => {{
    event.preventDefault();
    const platform = form.dataset.platform;
    const payload = Object.fromEntries(new FormData(form).entries());
    setMessage("connection-message", `Saving ${{platform}}...`);
    try {{
      await fetchJson(`/api/setup/${{platform}}/{store_id}/api-key`, {{ method: "POST", headers: {{"Content-Type":"application/json"}}, body: JSON.stringify(payload) }});
      setMessage("connection-message", `${{platform}} saved.`);
      if (platform === "telegram") loadConnections();
    }} catch (error) {{ setMessage("connection-message", error.message || `Saving ${{platform}} failed`); }}
  }});
}});
document.querySelectorAll("button[data-webhook]").forEach((button) => {{
  button.addEventListener("click", async () => {{
    const platform = button.dataset.webhook;
    setMessage("connection-message", `Verifying ${{platform}} webhook...`);
    try {{
      await fetchJson(`/api/setup/${{platform}}/{store_id}/webhook`, {{ method: "POST", headers: {{"Content-Type":"application/json"}} }});
      setMessage("connection-message", `${{platform}} webhook verified.`);
    }} catch (error) {{ setMessage("connection-message", error.message || `Webhook verification failed`); }}
  }});
}});

// ---- Products ----
let editingProductId = null;
async function loadProducts() {{
  try {{
    const products = await fetchJson(`/api/store/{store_id}/products/`);
    const el = document.getElementById("products-list");
    if (!products.length) {{ el.innerHTML = '<div class="sv-empty"><span class="sv-empty-icon"><i class="ti ti-package-off"></i></span><h3>No products yet</h3><p>Add your first product to help the AI recommend and sell it.</p></div>'; return; }}
    el.innerHTML = `<div class="sv-table-wrap"><table class="sv-table">
      <thead><tr>
        <th>Code</th><th>Name</th><th class="sv-tnum">Price</th>
        <th class="sv-tnum">Discount</th><th class="sv-tnum">Stock</th><th>Status</th><th>Actions</th>
      </tr></thead>
      <tbody>${{products.map(p => `<tr>
        <td><code class="sv-code">${{p.product_code}}</code></td>
        <td>${{p.name}}</td>
        <td class="sv-tnum">${{p.price}}</td>
        <td class="sv-tnum">${{p.discount || '-'}}</td>
        <td class="sv-tnum">${{p.available_count}}</td>
        <td><span class="sv-pill ${{p.enabled ? 'sv-pill-success' : 'sv-pill-neutral'}}">${{p.enabled ? 'Enabled' : 'Disabled'}}</span></td>
        <td><div class="sv-inline-actions">
          <button class="sv-btn sv-btn-secondary sv-btn-sm" onclick='editProduct(${{JSON.stringify(p)}})'>Edit</button>
          <button class="sv-btn sv-btn-danger sv-btn-sm" onclick="deleteProduct('${{p.id}}')">Delete</button>
        </div></td>
      </tr>`).join('')}}</tbody></table></div>`;
  }} catch(e) {{ document.getElementById("products-list").innerHTML = `<p class="sv-muted">${{e.message}}</p>`; }}
}}
function editProduct(p) {{
  editingProductId = p.id;
  const form = document.getElementById("product-form");
  form.elements.product_id.value = p.id;
  form.elements.product_code.value = p.product_code;
  form.elements.product_code.readOnly = true;
  form.elements.name.value = p.name;
  form.elements.description.value = p.description || "";
  form.elements.image.value = p.image || "";
  form.elements.price.value = p.price;
  form.elements.discount.value = p.discount || "";
  form.elements.available_count.value = p.available_count;
  form.elements.enabled.checked = p.enabled;
  document.getElementById("product-form-wrap").classList.remove("sv-hidden");
}}
document.getElementById("btn-add-product").addEventListener("click", () => {{
  editingProductId = null;
  document.getElementById("product-form").reset();
  document.getElementById("product-form").elements.product_code.readOnly = false;
  document.getElementById("product-form").elements.enabled.checked = true;
  document.getElementById("product-form-wrap").classList.remove("sv-hidden");
}});
document.getElementById("btn-cancel-product").addEventListener("click", () => {{
  document.getElementById("product-form-wrap").classList.add("sv-hidden");
}});
document.getElementById("product-form").addEventListener("submit", async (e) => {{
  e.preventDefault();
  const form = new FormData(e.target);
  const payload = {{
    product_code: form.get("product_code"),
    name: form.get("name"),
    description: form.get("description") || null,
    image: form.get("image") || null,
    price: parseFloat(form.get("price")),
    discount: form.get("discount") ? parseFloat(form.get("discount")) : null,
    available_count: parseInt(form.get("available_count")),
    enabled: form.get("enabled") === "on",
  }};
  setMessage("product-form-msg", "Saving...");
  try {{
    if (editingProductId) {{
      await fetchJson(`/api/store/{store_id}/products/${{editingProductId}}`, {{ method:"PUT", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify(payload) }});
    }} else {{
      await fetchJson(`/api/store/{store_id}/products/`, {{ method:"POST", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify(payload) }});
    }}
    setMessage("product-form-msg", "Saved.");
    document.getElementById("product-form-wrap").classList.add("sv-hidden");
    loadProducts();
  }} catch(err) {{ setMessage("product-form-msg", err.message || "Error saving product"); }}
}});
async function deleteProduct(id) {{
  if (!confirm("Delete this product?")) return;
  try {{
    await fetchJson(`/api/store/{store_id}/products/${{id}}`, {{ method:"DELETE" }});
    loadProducts();
  }} catch(e) {{ alert(e.message || "Error deleting product"); }}
}}

// ---- Coupons ----
let editingCouponId = null;
async function loadCoupons() {{
  try {{
    const coupons = await fetchJson(`/api/store/{store_id}/coupons/`);
    const el = document.getElementById("coupons-list");
    if (!coupons.length) {{ el.innerHTML = '<div class="sv-empty"><span class="sv-empty-icon"><i class="ti ti-ticket-off"></i></span><h3>No coupons yet</h3><p>Create a coupon when you want to drive campaigns or reward loyal customers.</p></div>'; return; }}
    el.innerHTML = `<div class="sv-table-wrap"><table class="sv-table">
      <thead><tr>
        <th>Code</th><th>Discount</th>
        <th class="sv-tnum">Used</th><th>Status</th><th>Actions</th>
      </tr></thead>
      <tbody>${{coupons.map(c => `<tr>
        <td><strong>${{c.code}}</strong></td>
        <td>${{c.discount_percent ? c.discount_percent + '%' : (c.discount_amount ? '-' + c.discount_amount : 'None')}}</td>
        <td class="sv-tnum">${{c.used_count}}/${{c.max_uses || '∞'}}</td>
        <td><span class="sv-pill ${{c.enabled ? 'sv-pill-success' : 'sv-pill-neutral'}}">${{c.enabled ? 'Enabled' : 'Disabled'}}</span></td>
        <td><div class="sv-inline-actions">
          <button class="sv-btn sv-btn-secondary sv-btn-sm" onclick='editCoupon(${{JSON.stringify(c)}})'>Edit</button>
          <button class="sv-btn sv-btn-danger sv-btn-sm" onclick="deleteCoupon('${{c.id}}')">Delete</button>
        </div></td>
      </tr>`).join('')}}</tbody></table></div>`;
  }} catch(e) {{ document.getElementById("coupons-list").innerHTML = `<p class="sv-muted">${{e.message}}</p>`; }}
}}
function editCoupon(c) {{
  editingCouponId = c.id;
  const f = document.getElementById("coupon-form");
  f.elements.coupon_id.value = c.id;
  f.elements.code.value = c.code;
  f.elements.description.value = c.description || "";
  f.elements.discount_amount.value = c.discount_amount || "";
  f.elements.discount_percent.value = c.discount_percent || "";
  f.elements.min_order_amount.value = c.min_order_amount || "";
  f.elements.max_uses.value = c.max_uses || "";
  f.elements.expires_at.value = c.expires_at ? c.expires_at.slice(0,16) : "";
  f.elements.enabled.checked = c.enabled;
  document.getElementById("coupon-form-wrap").classList.remove("sv-hidden");
}}
document.getElementById("btn-add-coupon").addEventListener("click", () => {{
  editingCouponId = null;
  document.getElementById("coupon-form").reset();
  document.getElementById("coupon-form").elements.enabled.checked = true;
  document.getElementById("coupon-form-wrap").classList.remove("sv-hidden");
}});
document.getElementById("btn-cancel-coupon").addEventListener("click", () => {{
  document.getElementById("coupon-form-wrap").classList.add("sv-hidden");
}});
document.getElementById("coupon-form").addEventListener("submit", async (e) => {{
  e.preventDefault();
  const form = new FormData(e.target);
  const payload = {{
    code: form.get("code"),
    description: form.get("description") || null,
    discount_amount: form.get("discount_amount") ? parseFloat(form.get("discount_amount")) : null,
    discount_percent: form.get("discount_percent") ? parseFloat(form.get("discount_percent")) : null,
    min_order_amount: form.get("min_order_amount") ? parseFloat(form.get("min_order_amount")) : null,
    max_uses: form.get("max_uses") ? parseInt(form.get("max_uses")) : null,
    expires_at: form.get("expires_at") ? new Date(form.get("expires_at")).toISOString() : null,
    enabled: form.get("enabled") === "on",
  }};
  setMessage("coupon-form-msg", "Saving...");
  try {{
    if (editingCouponId) {{
      await fetchJson(`/api/store/{store_id}/coupons/${{editingCouponId}}`, {{ method:"PUT", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify(payload) }});
    }} else {{
      await fetchJson(`/api/store/{store_id}/coupons/`, {{ method:"POST", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify(payload) }});
    }}
    setMessage("coupon-form-msg", "Saved.");
    document.getElementById("coupon-form-wrap").classList.add("sv-hidden");
    loadCoupons();
  }} catch(err) {{ setMessage("coupon-form-msg", err.message || "Error"); }}
}});
async function deleteCoupon(id) {{
  if (!confirm("Delete this coupon?")) return;
  try {{
    await fetchJson(`/api/store/{store_id}/coupons/${{id}}`, {{ method:"DELETE" }});
    loadCoupons();
  }} catch(e) {{ alert(e.message || "Error"); }}
}}

// ---- Orders ----
async function loadOrders() {{
  const filter = document.getElementById("order-status-filter").value;
  const url = `/api/store/{store_id}/orders/${{filter ? '?status='+filter : ''}}`;
  try {{
    const orders = await fetchJson(url);
    const el = document.getElementById("orders-list");
    if (!orders.length) {{ el.innerHTML = '<div class="sv-empty"><span class="sv-empty-icon"><i class="ti ti-shopping-cart-off"></i></span><h3>No orders found</h3><p>Orders created through your chat channels will appear here.</p></div>'; return; }}
    const statuses = ['PENDING','CONFIRMED','PROCESSING','SHIPPED','DELIVERED','CANCELLED'];
    el.innerHTML = `<div class="sv-table-wrap"><table class="sv-table">
      <thead><tr>
        <th>Order ID</th><th>Product</th><th>Customer</th>
        <th class="sv-tnum">Total</th><th>Date</th><th>Status</th>
      </tr></thead>
      <tbody>${{orders.map(o => `<tr>
        <td><code class="sv-code">${{o.order_number}}</code></td>
        <td>${{o.product_name}} x${{o.quantity}}</td>
        <td>${{o.customer_name}}<br><small class="sv-muted">${{o.customer_phone}}</small></td>
        <td class="sv-tnum">${{o.total_amount}}</td>
        <td>${{o.order_date ? o.order_date.slice(0,16).replace('T',' ') : ''}}</td>
        <td>
          <select onchange="updateOrderStatus('${{o.id}}', this.value)">
            ${{statuses.map(s => `<option value="${{s}}" ${{s===o.status?'selected':''}}>${{s}}</option>`).join('')}}
          </select>
        </td>
      </tr>`).join('')}}</tbody></table></div>`;
  }} catch(e) {{ document.getElementById("orders-list").innerHTML = `<p class="sv-muted">${{e.message}}</p>`; }}
}}
async function updateOrderStatus(id, newStatus) {{
  try {{
    await fetchJson(`/api/store/{store_id}/orders/${{id}}`, {{ method:"PUT", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{status:newStatus}}) }});
  }} catch(e) {{ alert("Failed to update order status: " + e.message); loadOrders(); }}
}}
document.getElementById("order-status-filter").addEventListener("change", loadOrders);
document.getElementById("btn-refresh-orders").addEventListener("click", loadOrders);

// ---- Connections Listing ----
async function loadConnections() {{
    try {{
        const fbRes = await fetchJson(`/api/meta/connected-pages/{store_id}`);
        const fbList = document.getElementById("facebook-connections-list");
        if (fbRes.pages && fbRes.pages.length) {{
            fbList.innerHTML = `<div class="sv-list">${{fbRes.pages.map(p => `<div class="sv-list-item"><div class="sv-list-item-main"><p><strong>${{p.page_name}}</strong></p><p class="sv-muted">Messenger page</p></div><div class="sv-list-item-actions"><button class="sv-btn sv-btn-danger sv-btn-sm" onclick="disconnectFacebook('${{p.page_id}}')">Disconnect</button></div></div>`).join("")}}</div>`;
        }} else {{
            fbList.innerHTML = `<p class="sv-muted">No pages connected.</p>`;
        }}
        
        const igRes = await fetchJson(`/api/meta/connected-instagram/{store_id}`);
        const igList = document.getElementById("instagram-connections-list");
        if (igRes.accounts && igRes.accounts.length) {{
            igList.innerHTML = `<div class="sv-list">${{igRes.accounts.map(p => `<div class="sv-list-item"><div class="sv-list-item-main"><p><strong>${{p.ig_username}}</strong></p><p class="sv-muted">Instagram business account</p></div><div class="sv-list-item-actions"><button class="sv-btn sv-btn-danger sv-btn-sm" onclick="disconnectInstagram('${{p.ig_user_id}}')">Disconnect</button></div></div>`).join("")}}</div>`;
        }} else {{
            igList.innerHTML = `<p class="sv-muted">No Instagram accounts connected.</p>`;
        }}
        
        const waRes = await fetchJson(`/api/meta/connected-whatsapp/{store_id}`);
        const waList = document.getElementById("whatsapp-connections-list");
        if (waRes.accounts && waRes.accounts.length) {{
            waList.innerHTML = `<div class="sv-list">${{waRes.accounts.map(p => `<div class="sv-list-item"><div class="sv-list-item-main"><p><strong>${{p.name}}</strong></p><p class="sv-muted">${{p.phone_number_id}}</p></div><div class="sv-list-item-actions"><button class="sv-btn sv-btn-danger sv-btn-sm" onclick="disconnectWhatsApp('${{p.phone_number_id}}')">Disconnect</button></div></div>`).join("")}}</div>`;
        }} else {{
            waList.innerHTML = `<p class="sv-muted">No WhatsApp accounts connected.</p>`;
        }}

        const tgRes = await fetchJson(`/api/setup/telegram/{store_id}`);
        const tgList = document.getElementById("telegram-connections-list");
        if (tgRes.connections && tgRes.connections.length) {{
            tgList.innerHTML = `<div class="sv-list">${{tgRes.connections.map(p => `<div class="sv-list-item"><div class="sv-list-item-main"><p><strong>${{p.bot_username}}</strong></p><p class="sv-muted">Telegram bot</p></div><div class="sv-list-item-actions"><button class="sv-btn sv-btn-danger sv-btn-sm" onclick="disconnectTelegram('${{p.id}}')">Disconnect</button></div></div>`).join("")}}</div>`;
        }} else {{
            tgList.innerHTML = `<p class="sv-muted">No Telegram bots connected.</p>`;
        }}
    }} catch(e) {{
        console.error("Error loading connections", e);
    }}
}}

async function disconnectFacebook(page_id) {{
    if(!confirm("Disconnect this Facebook Page?")) return;
    try {{
        await fetchJson(`/api/meta/disconnect-facebook/{store_id}/${{page_id}}`, {{method: 'DELETE'}});
        loadConnections();
    }} catch(e) {{ alert(e.message); }}
}}
async function disconnectInstagram(ig_user_id) {{
    if(!confirm("Disconnect this Instagram Account?")) return;
    try {{
        await fetchJson(`/api/meta/disconnect-instagram/{store_id}/${{ig_user_id}}`, {{method: 'DELETE'}});
        loadConnections();
    }} catch(e) {{ alert(e.message); }}
}}
async function disconnectWhatsApp(phone_number_id) {{
    if(!confirm("Disconnect this WhatsApp Account?")) return;
    try {{
        await fetchJson(`/api/meta/disconnect-whatsapp/{store_id}/${{phone_number_id}}`, {{method: 'DELETE'}});
        loadConnections();
    }} catch(e) {{ alert(e.message); }}
}}
async function disconnectTelegram(telegram_id) {{
    if(!confirm("Disconnect this Telegram Bot?")) return;
    try {{
        await fetchJson(`/api/setup/telegram/{store_id}/${{telegram_id}}`, {{method: 'DELETE'}});
        loadConnections();
    }} catch(e) {{ alert(e.message); }}
}}


// Meta Connect JS - Facebook
document.getElementById("btn-connect-facebook")?.addEventListener("click", async (event) => {{
    console.log("Connect Facebook button clicked");
    if (typeof FB === 'undefined') {{
        alert("Facebook SDK is not loaded. Please disable ad-blockers and try again.");
        return;
    }}
    if (!'{settings.META_APP_ID}') {{
        alert("META_APP_ID is not configured in the backend .env file!");
        return;
    }}

    FB.login(function(response) {{
        if (response.authResponse) {{
            const payload = {{
                user_access_token: response.authResponse.accessToken,
                connect_instagram: false
            }};
            setMessage("connection-message", "Connecting Facebook Page...");
            fetchJson(`/api/meta/connect-facebook/{store_id}`, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify(payload)
            }}).then(() => {{
                setMessage("connection-message", "Facebook connected successfully.");
                loadConnections();
            }}).catch((error) => {{
                setMessage("connection-message", error.message || "Failed to connect Facebook.");
            }});
        }} else {{
            setMessage("connection-message", "Facebook login cancelled or failed.");
        }}
    }}, {{
      scope: 'public_profile,pages_show_list,pages_messaging,pages_read_engagement,pages_manage_posts,pages_manage_metadata,pages_read_user_content,pages_manage_engagement'
    }});
    // TODO: ads_management should be added later
}});

// Meta Connect JS - Instagram (OAuth)
document.getElementById("btn-connect-instagram-oauth")?.addEventListener("click", async (event) => {{
    if (typeof FB === 'undefined') {{
        alert("Facebook SDK is not loaded. Please disable ad-blockers and try again.");
        return;
    }}
    if (!'{settings.META_APP_ID}') {{
        alert("META_APP_ID is not configured in the backend .env file!");
        return;
    }}

    FB.login(function(response) {{
        if (response.authResponse) {{
            const payload = {{
                user_access_token: response.authResponse.accessToken,
                connect_instagram: true
            }};
            setMessage("connection-message", "Connecting Instagram via OAuth...");
            fetchJson(`/api/meta/connect-facebook/{store_id}`, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify(payload)
            }}).then(() => {{
                setMessage("connection-message", "Instagram connected successfully.");
                loadConnections();
            }}).catch((error) => {{
                setMessage("connection-message", error.message || "Failed to connect Instagram.");
            }});
        }} else {{
            setMessage("connection-message", "Instagram login cancelled or failed.");
        }}
    }}, {{scope: 'pages_show_list,pages_messaging,pages_read_engagement,instagram_basic,instagram_manage_messages,instagram_manage_comments,instagram_content_publish,public_profile,pages_manage_posts,pages_manage_engagement'}});
    // TODO: ads_management will be added later
}});

// Meta Connect JS - Instagram (Manual Token Fallback)
document.getElementById("form-connect-instagram")?.addEventListener("submit", async (event) => {{
    event.preventDefault();
    const form = new FormData(event.target);
    const token = form.get("user_access_token");
    if (!token) {{
        alert("Please paste a User Access Token or use the OAuth button.");
        return;
    }}
    const payload = {{
        user_access_token: token,
        connect_instagram: true
    }};
    setMessage("connection-message", "Connecting Instagram with manual token...");
    try {{
        await fetchJson(`/api/meta/connect-facebook/{store_id}`, {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify(payload)
        }});
        setMessage("connection-message", "Instagram connected successfully via manual token.");
        loadConnections();
    }} catch (error) {{
        setMessage("connection-message", error.message || "Failed to connect Instagram.");
    }}
}});

// Meta Connect JS - WhatsApp Embedded Signup
document.getElementById("btn-connect-whatsapp")?.addEventListener("click", async (event) => {{
    if (typeof FB === 'undefined') {{
        alert("Facebook SDK is not loaded. Please disable ad-blockers and try again.");
        return;
    }}
    if (!'{settings.META_WHATSAPP_CONFIG_ID}') {{
        alert("META_WHATSAPP_CONFIG_ID is not configured in the backend .env file!");
        return;
    }}

    FB.login(function(response) {{
        if (response.authResponse && response.authResponse.code) {{
            const payload = {{ 
              code: response.authResponse.code,
              redirect_uri: window.location.href
            }};
            setMessage("connection-message", "Connecting WhatsApp...");
            fetchJson(`/api/meta/connect-whatsapp/{store_id}`, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify(payload)
            }}).then(() => {{
                setMessage("connection-message", "WhatsApp connected successfully.");
                loadConnections();
            }}).catch((error) => {{
                setMessage("connection-message", error.message || "Failed to connect WhatsApp.");
            }});
        }} else {{
            setMessage("connection-message", "WhatsApp login cancelled or failed.");
        }}
    }}, {{
        config_id: '{settings.META_WHATSAPP_CONFIG_ID}',
        response_type: 'code',
        override_default_response_type: true,
        extras: {{
            setup: {{}},
            featureType: '',
            sessionInfoVersion: '3'
        }}
    }});
}});

</script>
"""
    return render_page(f"Store {store_id}", body, script)


@router.get("/connections", response_class=HTMLResponse)
async def connections():
    body = """
<section class="sv-card">
  <div class="sv-card-body sv-empty">
    <span class="sv-empty-icon"><i class="ti ti-plug-connected"></i></span>
    <h3>Connections follow your current store</h3>
    <p>Open a store from the dashboard, then manage its platform connections there. If you recently opened one, this page will redirect you automatically.</p>
    <a class="sv-btn sv-btn-primary" href="/dashboard">Go to dashboard</a>
    <p class="sv-muted">This page will jump to the last selected store if one is saved.</p>
  </div>
</section>
"""
    script = """
<script>
ensureSessionOrRedirect().then((session) => {{ if (!session) {{ return; }} }}).catch((error) => {{ showError(error.message || "Session check failed"); }});
const storeId = getStoreId();
if (storeId) { window.location.href = `/stores/${storeId}`; }
</script>
"""
    return render_page("Connections", body, script)


@router.get("/orders", response_class=HTMLResponse)
async def orders():
    body = """
<section class="sv-card">
  <div class="sv-card-body sv-empty">
    <span class="sv-empty-icon"><i class="ti ti-shopping-cart"></i></span>
    <h3>Orders page is still a placeholder</h3>
    <p>The live order management experience currently lives inside each store workspace.</p>
    <a class="sv-btn sv-btn-primary" href="/dashboard">Back to dashboard</a>
  </div>
</section>
"""
    return render_page("Orders", body)
