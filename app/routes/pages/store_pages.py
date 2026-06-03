from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .common import render_page
from app.lib.config import settings

router = APIRouter()


@router.get("/stores/{store_id}", response_class=HTMLResponse)
async def store_detail(store_id: str):
    body = f"""
<h1>Store</h1>
<p id="store-summary" class="muted"></p>
<div class="actions">
  <a class="button secondary" href="/dashboard">Back to dashboard</a>
  <a class="button secondary" href="/orders">Orders placeholder</a>
  <button type="button" class="secondary" onclick="logout()">Logout</button>
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
      <select name="language">
        <option value="adaptive">Adaptive (auto-detect)</option>
        <option value="english">English</option>
        <option value="bangla">Bangla</option>
      </select>
    </label>
    <label style="display:flex;align-items:center;gap:12px;cursor:pointer;">
      <span>Accept Orders</span>
      <input type="checkbox" name="orders_enabled" id="orders-enabled-toggle" style="width:20px;height:20px;cursor:pointer;">
    </label>
    <div class="actions">
      <button type="submit">Save store</button>
    </div>
  </form>
  <p id="store-settings-message" class="muted"></p>
</section>

<section>
  <h2>Verification token</h2>
  <p class="muted">Use this token when configuring Facebook webhook verification for this store.</p>
  <div class="actions" style="justify-content:flex-start;">
    <input id="store-verification-token" readonly style="max-width:520px;">
    <button type="button" class="secondary copy-button" id="copy-store-verification-token"><span aria-hidden="true">📋</span><span>Copy token</span></button>
  </div>
</section>

<section>
  <h2>Products</h2>
  <p class="muted">Manage the products available in your store.</p>
  <div class="actions" style="justify-content:flex-start;margin-bottom:16px;">
    <button type="button" id="btn-add-product">+ Add Product</button>
  </div>
  <div id="product-form-wrap" style="display:none;margin-bottom:16px;">
    <form id="product-form" style="background:var(--surface,#1e1e2e);padding:16px;border-radius:8px;display:grid;gap:10px;">
      <input type="hidden" name="product_id">
      <label>Product Code <input name="product_code" placeholder="e.g. SKU-001" required></label>
      <label>Name <input name="name" placeholder="Product name" required></label>
      <label>Description <textarea name="description" placeholder="Optional description"></textarea></label>
      <label>Image URL <input name="image" placeholder="https://..."></label>
      <label>Price <input name="price" type="number" step="0.01" min="0" required></label>
      <label>Discount <input name="discount" type="number" step="0.01" min="0" placeholder="0"></label>
      <label>Stock Count <input name="available_count" type="number" min="0" value="0" required></label>
      <label style="display:flex;align-items:center;gap:10px;"><span>Enabled</span><input type="checkbox" name="enabled" checked style="width:18px;height:18px;"></label>
      <div class="actions">
        <button type="submit">Save Product</button>
        <button type="button" class="secondary" id="btn-cancel-product">Cancel</button>
      </div>
    </form>
    <p id="product-form-msg" class="muted"></p>
  </div>
  <div id="products-list"><p class="muted">Loading products...</p></div>
</section>

<section>
  <h2>Coupons</h2>
  <p class="muted">Create discount coupons for your customers.</p>
  <div class="actions" style="justify-content:flex-start;margin-bottom:16px;">
    <button type="button" id="btn-add-coupon">+ Add Coupon</button>
  </div>
  <div id="coupon-form-wrap" style="display:none;margin-bottom:16px;">
    <form id="coupon-form" style="background:var(--surface,#1e1e2e);padding:16px;border-radius:8px;display:grid;gap:10px;">
      <input type="hidden" name="coupon_id">
      <label>Code <input name="code" placeholder="e.g. SAVE10" required></label>
      <label>Description <input name="description" placeholder="Optional"></label>
      <label>Discount Amount (fixed) <input name="discount_amount" type="number" step="0.01" min="0" placeholder="0"></label>
      <label>Discount % <input name="discount_percent" type="number" step="0.01" min="0" max="100" placeholder="0"></label>
      <label>Min Order Amount <input name="min_order_amount" type="number" step="0.01" min="0" placeholder="0"></label>
      <label>Max Uses <input name="max_uses" type="number" min="1" placeholder="Unlimited"></label>
      <label>Expires At <input name="expires_at" type="datetime-local"></label>
      <label style="display:flex;align-items:center;gap:10px;"><span>Enabled</span><input type="checkbox" name="enabled" checked style="width:18px;height:18px;"></label>
      <div class="actions">
        <button type="submit">Save Coupon</button>
        <button type="button" class="secondary" id="btn-cancel-coupon">Cancel</button>
      </div>
    </form>
    <p id="coupon-form-msg" class="muted"></p>
  </div>
  <div id="coupons-list"><p class="muted">Loading coupons...</p></div>
</section>

<section>
  <h2>Orders</h2>
  <p class="muted">View and manage orders placed through chatbot.</p>
  <div class="actions" style="justify-content:flex-start;margin-bottom:12px;">
    <select id="order-status-filter">
      <option value="">All statuses</option>
      <option value="PENDING">Pending</option>
      <option value="CONFIRMED">Confirmed</option>
      <option value="PROCESSING">Processing</option>
      <option value="SHIPPED">Shipped</option>
      <option value="DELIVERED">Delivered</option>
      <option value="CANCELLED">Cancelled</option>
    </select>
    <button type="button" id="btn-refresh-orders" class="secondary">Refresh</button>
  </div>
  <div id="orders-list"><p class="muted">Loading orders...</p></div>
</section>

<section>
  <h2>Meta Connections</h2>
  
  <div style="margin-bottom: 24px;">
    <h3>Facebook Messenger</h3>
    <p class="muted">Connect your Facebook Page for Messenger.</p>
    <div class="actions" style="margin-top:8px;">
      <button type="button" id="btn-connect-facebook">Connect Facebook</button>
    </div>
  </div>

  <div>
    <h3>Instagram</h3>
    <p class="muted">Connect your Instagram Business account (must be linked to a Facebook Page).</p>
    <form id="form-connect-instagram">
      <label>User Access Token (Optional Manual Fallback)
        <input name="user_access_token" placeholder="Paste Graph API Explorer token if OAuth fails...">
      </label>
      <div class="actions" style="margin-top:8px;">
        <button type="button" id="btn-connect-instagram-oauth">Connect via OAuth</button>
        <button type="submit" class="secondary">Connect with Token</button>
      </div>
    </form>
  </div>
</section>

<section>
  <h2>WhatsApp Connection</h2>
  <p class="muted">Connect WhatsApp Business using Embedded Signup credentials.</p>
  <div class="actions" style="margin-top:8px;">
    <button type="button" id="btn-connect-whatsapp">Connect WhatsApp</button>
  </div>
</section>

<section>
  <h2>Global Meta Webhook</h2>
  <p class="muted">Configure this single Webhook URL in your Meta App Dashboard. It handles Messenger, Instagram, and WhatsApp.</p>
  <label>Webhook URL
    <input id="webhook-url-meta" readonly>
  </label>
  <div class="actions">
    <button type="button" class="secondary" data-copy-webhook="meta">Copy webhook URL</button>
  </div>
</section>

<section>
  <h2>Telegram Connection</h2>
  <form class="connection-form" data-platform="telegram">
    <label>Telegram bot token
      <input name="bot_token" value="demo-telegram-token" required>
    </label>
    <label>Bot username
      <input name="bot_username" value="demo_bot">
    </label>
    <label>Webhook URL
      <input id="webhook-url-telegram" readonly>
    </label>
    <div class="actions">
      <button type="button" class="secondary" data-copy-webhook="telegram">Copy webhook URL</button>
      <button type="submit">Save Telegram</button>
      <button type="button" class="secondary" data-webhook="telegram">Verify webhook</button>
    </div>
  </form>

  <p id="connection-message" class="muted"></p>
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
      version    : 'v18.0'
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
ensureSessionOrRedirect().then((session) => {{ if (!session) {{ return; }} renderWebhookUrls(); loadStore(); loadProducts(); loadCoupons(); loadOrders(); }}).catch((error) => {{ showError(error.message || "Session check failed"); }});

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
    if (!products.length) {{ el.innerHTML = "<p class=\'muted\'>No products yet.</p>"; return; }}
    el.innerHTML = `<table style="width:100%;border-collapse:collapse;font-size:14px;">
      <thead><tr style="text-align:left;border-bottom:1px solid #333;">
        <th style="padding:8px;">Code</th><th style="padding:8px;">Name</th><th style="padding:8px;">Price</th>
        <th style="padding:8px;">Discount</th><th style="padding:8px;">Stock</th><th style="padding:8px;">Status</th><th style="padding:8px;">Actions</th>
      </tr></thead>
      <tbody>${{products.map(p => `<tr style="border-bottom:1px solid #222;">
        <td style="padding:8px;"><code>${{p.product_code}}</code></td>
        <td style="padding:8px;">${{p.name}}</td>
        <td style="padding:8px;">${{p.price}}</td>
        <td style="padding:8px;">${{p.discount || '-'}}</td>
        <td style="padding:8px;">${{p.available_count}}</td>
        <td style="padding:8px;">${{p.enabled ? '✅' : '❌'}}</td>
        <td style="padding:8px;display:flex;gap:6px;">
          <button class="secondary" style="padding:4px 10px;font-size:12px;" onclick="editProduct(${{JSON.stringify(p)}})">Edit</button>
          <button class="secondary" style="padding:4px 10px;font-size:12px;color:#f66;" onclick="deleteProduct('${{p.id}}')">Del</button>
        </td>
      </tr>`).join('')}}</tbody></table>`;
  }} catch(e) {{ document.getElementById("products-list").innerHTML = `<p class="muted">${{e.message}}</p>`; }}
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
  document.getElementById("product-form-wrap").style.display = "block";
}}
document.getElementById("btn-add-product").addEventListener("click", () => {{
  editingProductId = null;
  document.getElementById("product-form").reset();
  document.getElementById("product-form").elements.product_code.readOnly = false;
  document.getElementById("product-form").elements.enabled.checked = true;
  document.getElementById("product-form-wrap").style.display = "block";
}});
document.getElementById("btn-cancel-product").addEventListener("click", () => {{
  document.getElementById("product-form-wrap").style.display = "none";
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
    document.getElementById("product-form-wrap").style.display = "none";
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
    if (!coupons.length) {{ el.innerHTML = "<p class=\'muted\'>No coupons yet.</p>"; return; }}
    el.innerHTML = `<table style="width:100%;border-collapse:collapse;font-size:14px;">
      <thead><tr style="text-align:left;border-bottom:1px solid #333;">
        <th style="padding:8px;">Code</th><th style="padding:8px;">Discount</th>
        <th style="padding:8px;">Used</th><th style="padding:8px;">Status</th><th style="padding:8px;">Actions</th>
      </tr></thead>
      <tbody>${{coupons.map(c => `<tr style="border-bottom:1px solid #222;">
        <td style="padding:8px;"><b>${{c.code}}</b></td>
        <td style="padding:8px;">${{c.discount_percent ? c.discount_percent+'%' : (c.discount_amount ? '-'+c.discount_amount : 'None')}}</td>
        <td style="padding:8px;">${{c.used_count}}/${{c.max_uses || '∞'}}</td>
        <td style="padding:8px;">${{c.enabled ? '✅' : '❌'}}</td>
        <td style="padding:8px;display:flex;gap:6px;">
          <button class="secondary" style="padding:4px 10px;font-size:12px;" onclick="editCoupon(${{JSON.stringify(c)}})">Edit</button>
          <button class="secondary" style="padding:4px 10px;font-size:12px;color:#f66;" onclick="deleteCoupon('${{c.id}}')">Del</button>
        </td>
      </tr>`).join('')}}</tbody></table>`;
  }} catch(e) {{ document.getElementById("coupons-list").innerHTML = `<p class="muted">${{e.message}}</p>`; }}
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
  document.getElementById("coupon-form-wrap").style.display = "block";
}}
document.getElementById("btn-add-coupon").addEventListener("click", () => {{
  editingCouponId = null;
  document.getElementById("coupon-form").reset();
  document.getElementById("coupon-form").elements.enabled.checked = true;
  document.getElementById("coupon-form-wrap").style.display = "block";
}});
document.getElementById("btn-cancel-coupon").addEventListener("click", () => {{
  document.getElementById("coupon-form-wrap").style.display = "none";
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
    document.getElementById("coupon-form-wrap").style.display = "none";
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
    if (!orders.length) {{ el.innerHTML = "<p class=\'muted\'>No orders found.</p>"; return; }}
    const statuses = ['PENDING','CONFIRMED','PROCESSING','SHIPPED','DELIVERED','CANCELLED'];
    el.innerHTML = `<table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead><tr style="text-align:left;border-bottom:1px solid #333;">
        <th style="padding:8px;">Order ID</th><th style="padding:8px;">Product</th><th style="padding:8px;">Customer</th>
        <th style="padding:8px;">Total</th><th style="padding:8px;">Date</th><th style="padding:8px;">Status</th>
      </tr></thead>
      <tbody>${{orders.map(o => `<tr style="border-bottom:1px solid #222;">
        <td style="padding:8px;"><code style="font-size:11px;">${{o.order_number}}</code></td>
        <td style="padding:8px;">${{o.product_name}} x${{o.quantity}}</td>
        <td style="padding:8px;">${{o.customer_name}}<br><small class="muted">${{o.customer_phone}}</small></td>
        <td style="padding:8px;">${{o.total_amount}}</td>
        <td style="padding:8px;">${{o.order_date ? o.order_date.slice(0,16).replace('T',' ') : ''}}</td>
        <td style="padding:8px;">
          <select onchange="updateOrderStatus('${{o.id}}', this.value)" style="font-size:12px;padding:3px;">
            ${{statuses.map(s => `<option value="${{s}}" ${{s===o.status?'selected':''}}>${{s}}</option>`).join('')}}
          </select>
        </td>
      </tr>`).join('')}}</tbody></table>`;
  }} catch(e) {{ document.getElementById("orders-list").innerHTML = `<p class="muted">${{e.message}}</p>`; }}
}}
async function updateOrderStatus(id, newStatus) {{
  try {{
    await fetchJson(`/api/store/{store_id}/orders/${{id}}`, {{ method:"PUT", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{status:newStatus}}) }});
  }} catch(e) {{ alert("Failed to update order status: " + e.message); loadOrders(); }}
}}
document.getElementById("order-status-filter").addEventListener("change", loadOrders);
document.getElementById("btn-refresh-orders").addEventListener("click", loadOrders);

// Meta Connect JS - Facebook
document.getElementById("btn-connect-facebook")?.addEventListener("click", async (event) => {{
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
            }}).catch((error) => {{
                setMessage("connection-message", error.message || "Failed to connect Facebook.");
            }});
        }} else {{
            setMessage("connection-message", "Facebook login cancelled or failed.");
        }}
    }}, {{scope: 'pages_show_list,pages_messaging'}});
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
            }}).catch((error) => {{
                setMessage("connection-message", error.message || "Failed to connect Instagram.");
            }});
        }} else {{
            setMessage("connection-message", "Instagram login cancelled or failed.");
        }}
    }}, {{scope: 'pages_show_list,pages_messaging,pages_read_engagement,instagram_basic,instagram_manage_messages,instagram_manage_comments'}});
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
            const payload = {{ code: response.authResponse.code }};
            setMessage("connection-message", "Connecting WhatsApp...");
            fetchJson(`/api/meta/connect-whatsapp/{store_id}`, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify(payload)
            }}).then(() => {{
                setMessage("connection-message", "WhatsApp connected successfully.");
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
<h1>Connections</h1>
<p class="muted">Open a store from the dashboard, then manage its platform connections here.</p>
<div class="actions">
  <a class="button" href="/dashboard">Go to dashboard</a>
  <button type="button" class="secondary" onclick="logout()">Logout</button>
</div>
<p class="small muted">This page will jump to the last selected store if one is saved.</p>
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
<h1>Orders</h1>
<p class="muted">Placeholder for now. The order flow can be added later in the separate frontend.</p>
<div class="actions">
  <a class="button" href="/dashboard">Back to dashboard</a>
  <button type="button" class="secondary" onclick="logout()">Logout</button>
</div>
"""
    return render_page("Orders", body)
