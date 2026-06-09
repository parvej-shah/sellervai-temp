# Project Context — SalesVai Backend

This file summarizes the backend flow, current store-centric naming, and how RAG is implemented so other conversations and contributors can pick up context quickly.

## High-level flow
- Incoming requests:
  - API chat requests: handled by `POST /api/chat` and `POST /api/chat/stream` in `app/routes/chat.py`
  - Platform messages: handled by webhooks in `app/routes/webhooks.py`. 
    - **Meta:** A single global webhook (`/api/webhooks/meta`) handles all traffic for Facebook Messenger, Instagram, and WhatsApp. It utilizes `BackgroundTasks` for fast 200 OK responses.
    - **Telegram:** Remains as per-store webhooks.
- Routes validate user or platform config and obtain an `AsyncSession` from the DB dependency (`app/lib/database.py`).
- Messages are processed by `app/services/message_processor.py` which calls the AI layer (`app/ai/service.py`).
- The AI layer uses DeepSeek via `ChatOpenAI` and builds prompts with optional RAG context.

## RAG (Retrieval-Augmented Generation)
- Implemented in `app/lib/rag.py` via the `RAGManager` class.
- Embeddings: `langchain_community.embeddings.FastEmbedEmbeddings` with `intfloat/multilingual-e5-small`.
- Vector store: `langchain_community.vectorstores.PGVector`.
- What is embedded:
  - `Store.description`
  - Each entry in `Store.products_items` (product name, description, price)
  - Uploaded documents are created as `langchain_core.documents.Document` objects.

## Vector store (PGVector)
- Backed by PostgreSQL using the app's database URL converted to a sync connection string.
- Collection name: `store_{store_id}`.
- Write flow: `RAGManager.index_store_data(...)` and `RAGManager.index_file(...)` call `vector_store.add_documents(...)`.
- Read flow: `RAGManager.query(text, k)` calls `vector_store.similarity_search(text, k)` and returns the `page_content` as context.
- Startup is kept lighter by loading the embedding backend lazily.

## Where indexing happens
- Manual/seed indexing: `scripts/seed.py` calls `get_rag_manager(...).index_store_data(..., force=True)` after creating sample data.
- There is no automatic re-index on product/description updates in the webhook/setup flows—updates must call indexing explicitly or be added later.

## How chat uses RAG
- `AIService.chat_stream()` pre-fetches RAG context for the user message and appends it to the prompt as `[Knowledge Base Context]`.
- The RAG import is lazy so chat still starts even if the embedding/vector extras are unavailable locally.
- For count queries ("how many"), the service also invokes `DatabaseTools.count_products()` and appends `[Live Database Status]` to the prompt.

## Data split
- PostgreSQL: users, stores, configuration, webhooks, platform tokens (encrypted), and vector storage via PGVector.
- Meta integration uses multi-tenant lookup tables (`ConnectedPage`, `ConnectedInstagram`, `ConnectedWhatsapp`) tracking individual tokens by page/waba identifiers as well as their display names (e.g. `page_name`, `ig_username`, `name`).
- Added `Conversation` and `Message` tables for thread tracking and webhook message deduplication.
- No ChromaDB dependency in the current implementation.

## Important notes / Recommendations
- Add indexed update triggers (on product/description changes) or a background job to keep PGVector in sync.
- Consider storing metadata IDs with vectors so replies can include product references/citations.
- If you want true tool-driven streaming (agent runs tools live and streams results), implement a structured agent loop that can call tools and stream intermediate outputs.
- The store detail page at `/stores/{store_id}` manages store configuration, products, coupons, orders, and platform connections natively using `/api/store` and `/api/meta` endpoints.
- The page template uses escaped braces (`{{` and `}}`) for Javascript blocks so the Python f-string stays valid when the route is rendered.
- **Connection Mechanisms:** 
  - Facebook and Instagram are connected via standard Facebook Login (OAuth) using `FB.login` with expanded scopes (`pages_manage_posts`, `ads_management`, `instagram_manage_comments`, etc.) allowing full control over engagement and ad management.
  - The short-lived user token returned by the frontend is immediately exchanged on the backend for a **long-lived user token** using `grant_type=fb_exchange_token`. This ensures the derived Page Access Tokens are **permanent**.
  - WhatsApp is connected using Meta's official Embedded Signup flow via `FB.login` requiring a backend code exchange.
  - Active connections (with their specific names/identifiers) can be viewed and disconnected from the store dashboard.
- **Verification:** Meta webhooks use a single global `META_VERIFY_TOKEN` configured via `.env`. Telegram still utilizes the per-store `verification_token`.

## Naming Status
- Current active router is `app/routes/store.py` with `/api/store` endpoints.
- The old `business` router was removed; the codebase should use `store` terminology going forward.
- Some webhook/setup parameter names still use `store_id` already; docs should stay aligned with that.

## Server-side page rendering (Mako + HTMX + Pico CSS)

- **Template engine**: [Mako](https://www.makotemplates.org/) — compiled Python templates with inheritance.
- **Helper**: `app/lib/templates.py` exposes `render_template(name, **ctx) -> HTMLResponse`.
  - Uses `TemplateLookup` pointed at the `templates/` directory in the project root.
  - Compiled `.pyc` modules cached in `/tmp/mako_modules`.
- **Template directory**: `templates/`
  - `base.html` — base layout; all pages do `<%inherit file="base.html"/>`.
  - Child templates override named defs: `extra_head`, `nav_items`, `extra_scripts`.
- **CDN libraries loaded in `base.html`**:
  - **Pico CSS v2** — `https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css`
  - **Tabler Icons** — `https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css`
  - **HTMX v2** — `https://unpkg.com/htmx.org@2.0.4`
- **Shared static assets** served from `/static/`:
  - `static/css/app.css` — custom design tokens and component styles.
  - `static/js/auth.js` — `getToken`, `fetchJson`, `ensureSessionOrRedirect`, etc.
- **Adding a new page**:
  1. Create `templates/<page>.html` with `<%inherit file="base.html"/>`.
  2. Create or extend a route file in `app/routes/pages/`.
  3. Call `render_template("<page>.html", **kwargs)` and return the result.
  4. Register the router in `app/routes/pages/__init__.py`.
- **HTMX usage**: Use `hx-get`, `hx-post`, `hx-swap`, `hx-trigger` attributes directly in templates.
  No build step needed — all updates happen over fetch without full-page reload.
- **Route ownership**: `GET /` is served by `app/routes/pages/home_pages.py`.
  Auth routes (`/login`, `/register`) remain in `auth_pages.py`.

---

File generated for quick context in conversations and developer onboarding.


WEBHOOK_URL: https://neural-raising-hugh-holdem.trycloudflare.com/api/webhooks/meta
VERIFY_TOKEN: sellervai_meta_webhook_token