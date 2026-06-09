from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .common import render_page

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def _dashboard_root():
    return render_page(
        "Dashboard",
        """
<section class="sv-card">
  <div class="sv-card-body sv-empty">
    <span class="sv-empty-icon"><i class="ti ti-layout-dashboard"></i></span>
    <h3>Open your dashboard</h3>
    <p>Your stores, connections, and automations live inside the main dashboard.</p>
    <a class="sv-btn sv-btn-primary" href="/dashboard">Go to dashboard</a>
  </div>
</section>
""",
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    body = """
<section class="sv-page-header">
  <div class="sv-page-title">
    <h1>Dashboard</h1>
    <p class="sv-page-lead">Your stores live here. Open one to manage connections, products, orders, and automations.</p>
  </div>
  <div class="sv-page-actions">
    <a class="sv-btn sv-btn-primary" href="/create-store"><i class="ti ti-building-store"></i> Create store</a>
  </div>
</section>

<section class="sv-card">
  <header class="sv-card-header">
    <h2 class="sv-card-title"><i class="ti ti-building-store"></i> Stores</h2>
  </header>
  <div class="sv-card-body sv-stack">
    <div id="store-list" class="sv-list"></div>
    <p id="dashboard-message" class="sv-muted"></p>
  </div>
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
<section class="sv-page-header">
  <div class="sv-page-title">
    <h1>Create store</h1>
    <p class="sv-page-lead">Use the starter values below to spin up a working store quickly, then fine-tune it from the store detail page.</p>
  </div>
  <div class="sv-page-actions">
    <a class="sv-btn sv-btn-secondary" href="/dashboard">Back to dashboard</a>
  </div>
</section>

<section class="sv-card">
  <header class="sv-card-header">
    <h2 class="sv-card-title"><i class="ti ti-plus"></i> Store setup</h2>
  </header>
  <div class="sv-card-body sv-stack">
    <form id="create-store-form" class="sv-form">
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
          <textarea name="description">A temporary test store.</textarea>
        </label>
        <label class="sv-field is-span-2">
          <span class="sv-field-label">Personality prompt</span>
          <textarea name="personality_prompt">Reply clearly, briefly, and helpfully.</textarea>
        </label>
        <label class="sv-field is-span-2">
          <span class="sv-field-label">Welcome message</span>
          <textarea name="welcome_message">Welcome to Demo Store.</textarea>
        </label>
        <label class="sv-field">
          <span class="sv-field-label">Language</span>
          <input name="language" value="english">
        </label>
        <label class="sv-field is-span-2">
          <span class="sv-field-label">Products items JSON</span>
          <textarea name="products_items">[{"name":"Sample Product","description":"Example item for testing","price":99}]</textarea>
        </label>
      </div>
      <div class="sv-page-actions">
        <button type="submit" class="sv-btn sv-btn-primary"><i class="ti ti-check"></i> Create store</button>
        <a class="sv-btn sv-btn-secondary" href="/dashboard">Cancel</a>
      </div>
    </form>
    <p id="create-store-message" class="sv-muted"></p>
  </div>
</section>
"""
    script = """
<script>
ensureSessionOrRedirect().then((session) => { if (!session) { return; } }).catch((error) => { showError(error.message || "Session check failed"); });
document.getElementById("create-store-form").addEventListener("submit", async (event)=>{ event.preventDefault(); const form=new FormData(event.target); const payload={ name: form.get("name"), description: form.get("description")||null, products_items: parseJsonInput(form.get("products_items"), []), tone: form.get("tone")||null, personality_prompt: form.get("personality_prompt")||null, welcome_message: form.get("welcome_message")||null, language: form.get("language")||null, }; setMessage("create-store-message","Creating store..."); try{ const store=await fetchJson("/api/store/",{ method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }); setStoreId(store.id); window.location.href=`/stores/${store.id}`; }catch(error){ setMessage("create-store-message", error.message||"Store creation failed"); } });
</script>
"""
    return render_page("Create store", body, script)
