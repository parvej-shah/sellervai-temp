/**
 * auth.js — shared authentication helpers loaded on every page.
 * Token storage uses localStorage with a consistent key convention.
 */

const SV_TOKEN_KEY    = "bizzz_token";
const SV_STORE_ID_KEY = "bizzz_store_id";

function getToken()   { return localStorage.getItem(SV_TOKEN_KEY) || ""; }
function setToken(t)  { localStorage.setItem(SV_TOKEN_KEY, t); }
function getStoreId() { return localStorage.getItem(SV_STORE_ID_KEY) || ""; }
function setStoreId(s){ localStorage.setItem(SV_STORE_ID_KEY, s); }
function clearAuth()  {
  localStorage.removeItem(SV_TOKEN_KEY);
  localStorage.removeItem(SV_STORE_ID_KEY);
}
function logout() { clearAuth(); window.location.href = "/login"; }

function authHeaders() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { ...(options.headers || {}), ...authHeaders() },
  });
  const raw = await response.text();
  let data = {};
  if (raw) {
    try { data = JSON.parse(raw); } catch { data = { detail: raw }; }
  }
  if (!response.ok) {
    if (response.status === 401) { clearAuth(); window.location.href = "/login"; }
    const err = new Error(data.detail || response.statusText || `HTTP ${response.status}`);
    err.status = response.status;
    err.data   = data;
    throw err;
  }
  return data;
}

async function ensureSessionOrRedirect() {
  const token = getToken();
  if (!token) return null;
  try {
    return await fetchJson("/api/auth/session");
  } catch (error) {
    clearAuth();
    if (error && error.status === 401) { window.location.href = "/login"; return null; }
    return null;
  }
}
