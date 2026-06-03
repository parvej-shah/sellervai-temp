from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .common import render_page

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def _dashboard_root():
    # placeholder
    return render_page("Dashboard", "<p>Go to /dashboard</p>")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    body = """
<h1>Dashboard</h1>
<p class="muted">Your stores live here. Open one to manage connections and store settings.</p>
<div class="actions">
  <a class="button" href="/create-store">Create store</a>
  <button type="button" class="secondary" onclick="logout()">Logout</button>
</div>
<section>
  <h2>Stores</h2>
  <div id="store-list" class="store-list"></div>
  <p id="dashboard-message" class="muted"></p>
</section>
"""
    script = """
<script>
ensureSessionOrRedirect().then((session) => { if (!session) { return; } loadDashboard(); }).catch((error) => { showError(error.message || "Session check failed"); });
async function loadDashboard(){ try{ const stores = await fetchStores(); renderStoreCards("store-list", stores); setMessage("dashboard-message", stores.length?`Loaded ${stores.length} store(s).`:"No stores yet."); }catch(e){ setMessage("dashboard-message", e.message||"Could not load stores."); } }
</script>
"""
    return render_page("Dashboard", body, script)


@router.get("/create-store", response_class=HTMLResponse)
async def create_store_page():
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
ensureSessionOrRedirect().then((session) => { if (!session) { return; } }).catch((error) => { showError(error.message || "Session check failed"); });
document.getElementById("create-store-form").addEventListener("submit", async (event)=>{ event.preventDefault(); const form=new FormData(event.target); const payload={ name: form.get("name"), description: form.get("description")||null, products_items: parseJsonInput(form.get("products_items"), []), tone: form.get("tone")||null, personality_prompt: form.get("personality_prompt")||null, welcome_message: form.get("welcome_message")||null, language: form.get("language")||null, }; setMessage("create-store-message","Creating store..."); try{ const store=await fetchJson("/api/store/",{ method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }); setStoreId(store.id); window.location.href=`/stores/${store.id}`; }catch(error){ setMessage("create-store-message", error.message||"Store creation failed"); } });
</script>
"""
    return render_page("Create store", body, script)
