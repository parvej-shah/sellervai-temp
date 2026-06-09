from fastapi.responses import HTMLResponse

from app.lib.templates import render_template


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
function showError(text){const wrap=document.getElementById("page-error");const msg=document.getElementById("page-error-text");if(wrap&&msg){msg.textContent=text;wrap.classList.remove("sv-hidden")}}
function clearError(){const wrap=document.getElementById("page-error");const msg=document.getElementById("page-error-text");if(wrap&&msg){msg.textContent="";wrap.classList.add("sv-hidden")}}
function requireTokenOrRedirect(){if(!getToken()){window.location.href="/";return false}return true}
async function ensureSessionOrRedirect(){const token=getToken();if(!token){return null}try{return await fetchJson("/api/auth/session")}catch(error){clearAuth();if(error && error.status === 401){window.location.href="/login";return null}showError(error.message||"Session check failed");return null}}
function parseJsonInput(value,fallback){const t=String(value||"").trim();if(!t){return fallback}try{return JSON.parse(t)}catch{return fallback}}
async function copyText(text){const value=String(text||"");if(!value){return false}if(navigator.clipboard && window.isSecureContext){await navigator.clipboard.writeText(value);return true}const input=document.createElement("textarea");input.value=value;input.setAttribute("readonly","");input.style.position="absolute";input.style.left="-9999px";document.body.appendChild(input);input.select();document.execCommand("copy");document.body.removeChild(input);return true}
async function fetchJson(url,options={}){const response=await fetch(url,{...options,headers:{...(options.headers||{}),...authHeaders()}});const rawText=await response.text();let data={};if(rawText){try{data=JSON.parse(rawText)}catch{data={detail:rawText}}}if(!response.ok){if(response.status===401){clearAuth();window.location.href="/login";}const err=new Error(data.detail||response.statusText||`HTTP ${response.status}`);err.status=response.status;err.data=data;throw err}return data}
async function fetchStores(){return fetchJson("/api/store/")}
function renderStoreCards(containerId,stores){const c=document.getElementById(containerId);if(!c)return;c.innerHTML="";if(!stores.length){c.innerHTML='<div class="sv-empty"><span class="sv-empty-icon"><i class="ti ti-building-store"></i></span><h3>No stores yet</h3><p>Create your first store to start connecting channels and selling with AI.</p></div>';return}for(const store of stores){const card=document.createElement("article");card.className="sv-list-item";const main=document.createElement("div");main.className="sv-list-item-main";const title=document.createElement("p");title.innerHTML=`<strong>${store.name}</strong>`;main.appendChild(title);const description=document.createElement("p");description.className="sv-muted";description.textContent=store.description||"No description yet.";main.appendChild(description);const actions=document.createElement("div");actions.className="sv-list-item-actions";const openLink=document.createElement("a");openLink.className="sv-btn sv-btn-primary sv-btn-sm";openLink.href=`/stores/${store.id}`;openLink.innerHTML='<i class="ti ti-arrow-right"></i> Open store';openLink.addEventListener("click",()=>setStoreId(store.id));actions.appendChild(openLink);card.appendChild(main);card.appendChild(actions);c.appendChild(card)}}
</script>
"""


def render_page(title: str, body: str, script: str = "") -> HTMLResponse:
    nav_html = """
  <li><a href="/dashboard" class="sv-btn sv-btn-ghost">Dashboard</a></li>
  <li><button type="button" class="sv-btn sv-btn-secondary sv-btn-sm" onclick="logout()">Logout</button></li>
"""
    body_html = f"""
<div class="sv-page">
  <div id="page-error" class="sv-alert sv-alert-danger sv-hidden">
    <i class="ti ti-alert-circle"></i>
    <div>
      <p class="sv-alert-title">Something went wrong</p>
      <p id="page-error-text"></p>
    </div>
  </div>
  {body}
</div>
"""
    full_script = COMMON_SCRIPT + script
    return render_template(
        "app_page.html",
        page_title=title,
        body_html=body_html,
        script_html=full_script,
        meta_text=f"{title} — Sellervai application page.",
        nav_html=nav_html,
    )
