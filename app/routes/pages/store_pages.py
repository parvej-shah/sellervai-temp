from fastapi import APIRouter
from .common import render_page

router = APIRouter()


@router.get("/stores/{store_id}", response_class=None)
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
      <input name="language" value="english">
    </label>
    <label>Products items JSON
      <textarea name="products_items">[{{"name":"Sample Product","description":"Example item for testing","price":99}}]</textarea>
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
  <h2>Connections</h2>

  <form class="connection-form" data-platform="messenger">
    <label>Messenger API key
      <input name="api_key" value="demo-messenger-token" required>
    </label>
    <label>Page ID
      <input name="page_id" value="1234567890">
    </label>
    <label>Webhook URL
      <input id="webhook-url-messenger" readonly>
    </label>
    <div class="actions">
      <button type="button" class="secondary" data-copy-webhook="messenger">Copy webhook URL</button>
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
    <label>Webhook URL
      <input id="webhook-url-whatsapp" readonly>
    </label>
    <div class="actions">
      <button type="button" class="secondary" data-copy-webhook="whatsapp">Copy webhook URL</button>
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
    <label>Webhook URL
      <input id="webhook-url-telegram" readonly>
    </label>
    <div class="actions">
      <button type="button" class="secondary" data-copy-webhook="telegram">Copy webhook URL</button>
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
    <label>Webhook URL
      <input id="webhook-url-instagram" readonly>
    </label>
    <div class="actions">
      <button type="button" class="secondary" data-copy-webhook="instagram">Copy webhook URL</button>
      <button type="submit">Save Instagram</button>
      <button type="button" class="secondary" data-webhook="instagram">Verify webhook</button>
    </div>
  </form>

  <p id="connection-message" class="muted"></p>
</section>
"""
    script = f"""
<script>
setStoreId("{store_id}");
const webhookPlatforms = ["messenger", "whatsapp", "telegram", "instagram"];
function webhookUrl(platform) {{ return `${{window.location.origin}}/api/webhooks/${{platform}}/{store_id}`; }}
function renderWebhookUrls() {{ webhookPlatforms.forEach((platform) => {{ const input = document.getElementById(`webhook-url-${{platform}}`); if (input) {{ input.value = webhookUrl(platform); }} }}); }}
ensureSessionOrRedirect().then((session) => {{ if (!session) {{ return; }} renderWebhookUrls(); loadStore(); }}).catch((error) => {{ showError(error.message || "Session check failed"); }});
async function loadStore() {{ try {{ const store = await fetchJson(`/api/store/{store_id}`); document.getElementById("store-summary").textContent = `${{store.name}} - ${{store.description || "No description yet."}}`; const settingsForm = document.getElementById("store-settings-form"); settingsForm.elements.name.value = store.name || ""; settingsForm.elements.description.value = store.description || ""; settingsForm.elements.tone.value = store.tone || ""; settingsForm.elements.personality_prompt.value = store.personality_prompt || ""; settingsForm.elements.welcome_message.value = store.welcome_message || ""; settingsForm.elements.language.value = store.language || "english"; settingsForm.elements.products_items.value = JSON.stringify(store.products_items || [], null, 2); const tokenInput = document.getElementById("store-verification-token"); if (tokenInput) {{ tokenInput.value = store.verification_token || ""; }} }} catch (error) {{ setMessage("store-summary", error.message || "Could not load store"); }} }}
document.getElementById("store-settings-form").addEventListener("submit", async (event) => {{ event.preventDefault(); const form = new FormData(event.target); const payload = {{ name: form.get("name"), description: form.get("description") || null, products_items: parseJsonInput(form.get("products_items"), []), tone: form.get("tone") || null, personality_prompt: form.get("personality_prompt") || null, welcome_message: form.get("welcome_message") || null, language: form.get("language") || null, }}; setMessage("store-settings-message", "Saving store..."); try {{ await fetchJson(`/api/store/{store_id}`, {{ method: "PUT", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify(payload), }}); setMessage("store-settings-message", "Store saved."); }} catch (error) {{ setMessage("store-settings-message", error.message || "Could not save store"); }} }});
document.getElementById("copy-store-verification-token").addEventListener("click", async () => {{ const tokenInput = document.getElementById("store-verification-token"); const button = document.getElementById("copy-store-verification-token"); try {{ await copyText(tokenInput?.value || ""); const label = button.querySelector("span:last-child"); if (label) {{ label.textContent = "Copied"; setTimeout(() => {{ label.textContent = "Copy token"; }}, 1500); }} setMessage("connection-message", "Verification token copied."); }} catch (error) {{ setMessage("connection-message", error.message || "Could not copy verification token"); }} }});
document.querySelectorAll("button[data-copy-webhook]").forEach((button) => {{ button.addEventListener("click", async () => {{ const platform = button.dataset.copyWebhook; const url = webhookUrl(platform); try {{ await copyText(url); const label = button.querySelector("span:last-child"); if (label) {{ label.textContent = "Copied"; setTimeout(() => {{ label.textContent = "Copy webhook URL"; }}, 1500); }} else {{ button.textContent = "Copied"; setTimeout(() => {{ button.textContent = "Copy webhook URL"; }}, 1500); }} }} catch (error) {{ setMessage("connection-message", error.message || "Could not copy webhook URL"); }} }}); }});
document.querySelectorAll(".connection-form").forEach((form) => {{ form.addEventListener("submit", async (event) => {{ event.preventDefault(); const platform = form.dataset.platform; const formData = new FormData(form); const payload = Object.fromEntries(formData.entries()); setMessage("connection-message", `Saving ${{platform}}...`); try {{ await fetchJson(`/api/setup/${{platform}}/{store_id}/api-key`, {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify(payload), }}); setMessage("connection-message", `${{platform}} saved.`); }} catch (error) {{ setMessage("connection-message", error.message || `Saving ${{platform}} failed`); }} }}); }});
document.querySelectorAll("button[data-webhook]").forEach((button) => {{ button.addEventListener("click", async () => {{ const platform = button.dataset.webhook; setMessage("connection-message", `Verifying ${{platform}} webhook...`); try {{ await fetchJson(`/api/setup/${{platform}}/{store_id}/webhook`, {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, }}); setMessage("connection-message", `${{platform}} webhook verified.`); }} catch (error) {{ setMessage("connection-message", error.message || `Webhook verification failed for ${{platform}}`); }} }}); }});
loadStore();
</script>
"""
    return render_page(f"Store {store_id}", body, script)


@router.get("/connections", response_class=None)
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


@router.get("/orders", response_class=None)
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
