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
ensureSessionOrRedirect().then((session) => {{ if (!session) {{ return; }} renderWebhookUrls(); loadStore(); }}).catch((error) => {{ showError(error.message || "Session check failed"); }});
async function loadStore() {{ try {{ const store = await fetchJson(`/api/store/{store_id}`); document.getElementById("store-summary").textContent = `${{store.name}} - ${{store.description || "No description yet."}}`; const settingsForm = document.getElementById("store-settings-form"); settingsForm.elements.name.value = store.name || ""; settingsForm.elements.description.value = store.description || ""; settingsForm.elements.tone.value = store.tone || ""; settingsForm.elements.personality_prompt.value = store.personality_prompt || ""; settingsForm.elements.welcome_message.value = store.welcome_message || ""; settingsForm.elements.language.value = store.language || "english"; settingsForm.elements.products_items.value = JSON.stringify(store.products_items || [], null, 2); const tokenInput = document.getElementById("store-verification-token"); if (tokenInput) {{ tokenInput.value = store.verification_token || ""; }} }} catch (error) {{ setMessage("store-summary", error.message || "Could not load store"); }} }}
document.getElementById("store-settings-form").addEventListener("submit", async (event) => {{ event.preventDefault(); const form = new FormData(event.target); const payload = {{ name: form.get("name"), description: form.get("description") || null, products_items: parseJsonInput(form.get("products_items"), []), tone: form.get("tone") || null, personality_prompt: form.get("personality_prompt") || null, welcome_message: form.get("welcome_message") || null, language: form.get("language") || null, }}; setMessage("store-settings-message", "Saving store..."); try {{ await fetchJson(`/api/store/{store_id}`, {{ method: "PUT", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify(payload), }}); setMessage("store-settings-message", "Store saved."); }} catch (error) {{ setMessage("store-settings-message", error.message || "Could not save store"); }} }});
document.getElementById("copy-store-verification-token").addEventListener("click", async () => {{ const tokenInput = document.getElementById("store-verification-token"); const button = document.getElementById("copy-store-verification-token"); try {{ await copyText(tokenInput?.value || ""); const label = button.querySelector("span:last-child"); if (label) {{ label.textContent = "Copied"; setTimeout(() => {{ label.textContent = "Copy token"; }}, 1500); }} setMessage("connection-message", "Verification token copied."); }} catch (error) {{ setMessage("connection-message", error.message || "Could not copy verification token"); }} }});
document.querySelectorAll("button[data-copy-webhook]").forEach((button) => {{ button.addEventListener("click", async () => {{ const platform = button.dataset.copyWebhook; const url = webhookUrl(platform); try {{ await copyText(url); const label = button.querySelector("span:last-child"); if (label) {{ label.textContent = "Copied"; setTimeout(() => {{ label.textContent = "Copy webhook URL"; }}, 1500); }} else {{ button.textContent = "Copied"; setTimeout(() => {{ button.textContent = "Copy webhook URL"; }}, 1500); }} }} catch (error) {{ setMessage("connection-message", error.message || "Could not copy webhook URL"); }} }}); }});
document.querySelectorAll(".connection-form").forEach((form) => {{ form.addEventListener("submit", async (event) => {{ event.preventDefault(); const platform = form.dataset.platform; const formData = new FormData(form); const payload = Object.fromEntries(formData.entries()); setMessage("connection-message", `Saving ${{platform}}...`); try {{ await fetchJson(`/api/setup/${{platform}}/{store_id}/api-key`, {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify(payload), }}); setMessage("connection-message", `${{platform}} saved.`); }} catch (error) {{ setMessage("connection-message", error.message || `Saving ${{platform}} failed`); }} }}); }});
document.querySelectorAll("button[data-webhook]").forEach((button) => {{ button.addEventListener("click", async () => {{ const platform = button.dataset.webhook; setMessage("connection-message", `Verifying ${{platform}} webhook...`); try {{ await fetchJson(`/api/setup/${{platform}}/{store_id}/webhook`, {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, }}); setMessage("connection-message", `${{platform}} webhook verified.`); }} catch (error) {{ setMessage("connection-message", error.message || `Webhook verification failed for ${{platform}}`); }} }}); }});

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

loadStore();
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
