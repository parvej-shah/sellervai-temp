from fastapi.responses import HTMLResponse


PAGE_STYLE = """
<style>
  :root { color-scheme: light; }
  body { margin: 0; padding: 24px; font-family: Arial, Helvetica, sans-serif; color: #111; background: #fff; }
  main { max-width: 760px; margin: 0 auto; text-align: center; }
  section { margin: 24px auto; padding: 16px; border: 1px solid #ddd; border-radius: 8px; text-align: left; }
  form { display: grid; gap: 12px; }
  label { display: grid; gap: 6px; }
  input, textarea, select, button { font: inherit; padding: 8px 10px; }
  input, textarea, select { width: 100%; box-sizing: border-box; }
  textarea { min-height: 92px; resize: vertical; }
  button, .button { display: inline-block; width: auto; text-decoration: none; border: 1px solid #111; background: #111; color: #fff; cursor: pointer; }
  .button.secondary, button.secondary { background: #fff; color: #111; }
  .actions { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
  .grid { display: grid; gap: 16px; }
  .store-list { display: grid; gap: 12px; }
  .store-card { border: 1px solid #ddd; border-radius: 8px; padding: 12px; }
  .muted { color: #666; }
  .small { font-size: 0.92rem; }
  .error-banner { display: none; margin: 0 auto 16px; padding: 12px 14px; border: 1px solid #c62828; border-radius: 8px; background: #fdecec; color: #8b1e1e; text-align: left; }
  .error-banner.visible { display: block; }
</style>
"""


COMMON_SCRIPT = """
<script>
const BIZZZ_TOKEN_KEY = "bizzz_token";
const BIZZZ_STORE_KEY = "bizzz_store_id";
function getToken(){return localStorage.getItem(BIZZZ_TOKEN_KEY)||""}
function setToken(t){localStorage.setItem(BIZZZ_TOKEN_KEY,t)}
function getStoreId(){return localStorage.getItem(BIZZZ_STORE_KEY)||""}
function setStoreId(s){localStorage.setItem(BIZZZ_STORE_KEY,s)}
function authHeaders(){const t=getToken();return t?{Authorization:`Bearer ${t}`}:{}}
function clearAuth(){localStorage.removeItem(BIZZZ_TOKEN_KEY);localStorage.removeItem(BIZZZ_STORE_KEY)}
function logout(){clearAuth();window.location.href="/login"}
function setMessage(id,text){const e=document.getElementById(id);if(e){e.textContent=text}}
function showError(text){const e=document.getElementById("page-error");if(e){e.textContent=text;e.classList.add("visible")}}
function clearError(){const e=document.getElementById("page-error");if(e){e.textContent="";e.classList.remove("visible")}}
function requireTokenOrRedirect(){if(!getToken()){window.location.href="/";return false}return true}
async function ensureSessionOrRedirect(){const token=getToken();if(!token){return null}try{return await fetchJson("/api/auth/session")}catch(error){clearAuth();if(error && error.status === 401){window.location.href="/login";return null}showError(error.message||"Session check failed");return null}}
function parseJsonInput(value,fallback){const t=String(value||"").trim();if(!t){return fallback}try{return JSON.parse(t)}catch{return fallback}}
async function fetchJson(url,options={}){const response=await fetch(url,{...options,headers:{...(options.headers||{}),...authHeaders()}});const rawText=await response.text();let data={};if(rawText){try{data=JSON.parse(rawText)}catch{data={detail:rawText}}}if(!response.ok){if(response.status===401){clearAuth();window.location.href="/login";}const err=new Error(data.detail||response.statusText||`HTTP ${response.status}`);err.status=response.status;err.data=data;throw err}return data}
async function fetchStores(){return fetchJson("/api/store/")}
function renderStoreCards(containerId,stores){const c=document.getElementById(containerId);if(!c)return;c.innerHTML="";if(!stores.length){c.innerHTML='<p class="muted">No stores yet.</p>';return}for(const store of stores){const card=document.createElement("div");card.className="store-card";const title=document.createElement("h3");title.textContent=store.name;card.appendChild(title);const description=document.createElement("p");description.className="muted small";description.textContent=store.description||"No description yet.";card.appendChild(description);const actions=document.createElement("div");actions.className="actions";const openLink=document.createElement("a");openLink.className="button";openLink.href=`/stores/${store.id}`;openLink.textContent="Open store";openLink.addEventListener("click",()=>setStoreId(store.id));actions.appendChild(openLink);card.appendChild(actions);c.appendChild(card)}}
</script>
"""


def render_page(title: str, body: str, script: str = "") -> HTMLResponse:
    return HTMLResponse(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  {PAGE_STYLE}
</head>
<body>
  <main>
    <div id="page-error" class="error-banner"></div>
{body}
  </main>
  {COMMON_SCRIPT}
  {script}
</body>
</html>""")
