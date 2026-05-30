from fastapi import APIRouter
from .common import render_page

router = APIRouter()


@router.get("/", response_class=None)
async def _root_redirect():
    # root is defined in main pages package; keep this placeholder minimal
    body = """
<section>
  <h1>Bizzz Backend</h1>
  <p class="muted">Use /login or /register</p>
  <div class="actions">
    <a class="button" href="/login">Sign in</a>
    <a class="button secondary" href="/register">Create account</a>
  </div>
</section>
"""
    script = """
<script>
ensureSessionOrRedirect().then((session) => { if (session) { window.location.href = "/dashboard"; } }).catch((error) => { showError(error.message || "Session check failed"); });
</script>
"""
    return render_page("Bizzz Backend", body, script)


@router.get("/login", response_class=None)
async def login_page():
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
ensureSessionOrRedirect().then((session) => { if (session) { window.location.href = "/dashboard"; } }).catch((error) => { showError(error.message || "Session check failed"); });
document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const body = new URLSearchParams();
  body.set("username", form.get("email"));
  body.set("password", form.get("password"));
  setMessage("login-message", "Signing in...");
  try {
    const response = await fetch("/api/auth/login/docs", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) { setMessage("login-message", data.detail || "Login failed"); return; }
    setToken(data.access_token);
    window.location.href = "/dashboard";
  } catch (error) { setMessage("login-message", "Login failed"); }
});
</script>
"""
    return render_page("Login", body, script)


@router.get("/register", response_class=None)
async def register_page():
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
ensureSessionOrRedirect().then((session) => { if (session) { window.location.href = "/dashboard"; } }).catch((error) => { showError(error.message || "Session check failed"); });
document.getElementById("register-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = { name: form.get("name"), email: form.get("email"), phone_number: form.get("phone_number")||null, password: form.get("password") };
  setMessage("register-message", "Creating account...");
  try {
    const registerResponse = await fetch("/api/auth/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const registerData = await registerResponse.json().catch(() => ({}));
    if (!registerResponse.ok && !String(registerData.detail||"").includes("already registered")) { setMessage("register-message", registerData.detail||"Registration failed"); return; }
    const loginData = new URLSearchParams(); loginData.set("username", payload.email); loginData.set("password", payload.password);
    const loginResponse = await fetch("/api/auth/login/docs", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: loginData });
    const loginJson = await loginResponse.json().catch(() => ({}));
    if (!loginResponse.ok) { setMessage("register-message", loginJson.detail||"Login failed"); return; }
    setToken(loginJson.access_token);
    window.location.href = "/dashboard";
  } catch (error) { setMessage("register-message", "Registration failed"); }
});
</script>
"""
    return render_page("Register", body, script)


@router.get("/create-account", response_class=None)
async def create_account():
    return await register_page()
