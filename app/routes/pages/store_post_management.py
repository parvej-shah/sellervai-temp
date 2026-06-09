from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .common import render_page
from app.lib.config import settings

router = APIRouter()

@router.get("/posts/{store_id}", response_class=HTMLResponse)
async def post_management(store_id: str):
    print(f"Rendering post management page for store {store_id} in {settings.ENVIRONMENT} environment")
    body = f"""
<section class="sv-page-header">
  <div class="sv-page-title">
    <h1>Post management</h1>
    <p class="sv-page-lead">Manage your published social posts and control how Sellervai replies to comments automatically.</p>
  </div>
  <div class="sv-page-actions">
    <a href="/stores/{store_id}" class="sv-btn sv-btn-secondary">Back to store</a>
    <a href="/dashboard" class="sv-btn sv-btn-ghost">Dashboard</a>
  </div>
</section>

<section class="sv-grid-auto">
  <article class="sv-card">
    <header class="sv-card-header">
      <h2 class="sv-card-title"><i class="ti ti-robot"></i> Autopilot control</h2>
    </header>
    <div class="sv-card-body sv-stack">
      <p class="sv-muted">When enabled, the bot will automatically reply to comments on your posts using the saved post knowledge.</p>
      <div class="sv-inline-actions">
        <label class="sv-choice">
          <input type="checkbox" id="autopilot-toggle">
          <span>
            <strong>Enable autopilot</strong>
            <p class="sv-muted">Turn automatic comment handling on or off for this store.</p>
          </span>
        </label>
        <button type="button" class="sv-btn sv-btn-primary" onclick="toggleAutopilot()">Save</button>
        <span id="autopilot-status" class="sv-pill sv-pill-neutral">Checking status...</span>
      </div>
    </div>
  </article>
</section>

<section class="sv-card">
  <header class="sv-card-header">
    <h2 class="sv-card-title"><i class="ti ti-photo"></i> Your posts</h2>
    <div class="sv-inline-actions">
      <button type="button" class="sv-btn sv-btn-primary" onclick="openCreatePostModal()"><i class="ti ti-edit"></i> New post</button>
      <button type="button" class="sv-btn sv-btn-secondary" onclick="loadPosts()">Refresh</button>
    </div>
  </header>
  <div class="sv-card-body sv-stack">
    <div class="sv-toolbar">
      <label class="sv-checkbox-row">
        <input type="checkbox" id="select-all-posts" onchange="toggleSelectAll()">
        <span>Select all</span>
      </label>
      <button type="button" class="sv-btn sv-btn-secondary sv-hidden" id="pause-selected-btn" onclick="bulkPauseSelected()">Pause selected</button>
      <button type="button" class="sv-btn sv-btn-secondary sv-hidden" id="resume-selected-btn" onclick="bulkResumeSelected()">Resume selected</button>
    </div>
    <div id="posts-container" class="sv-stack">
      <p class="sv-muted">Loading posts...</p>
    </div>
  </div>
</section>

<div id="post-detail-modal" class="sv-modal">
  <div class="sv-modal-dialog">
    <div class="sv-modal-header">
      <h3 id="modal-title">Post details</h3>
      <button type="button" class="sv-icon-btn" onclick="closePostDetail()" aria-label="Close"><i class="ti ti-x"></i></button>
    </div>
    <div id="post-detail-content" class="sv-modal-body"></div>
  </div>
</div>

<div id="create-post-modal" class="sv-modal">
  <div class="sv-modal-dialog">
    <div class="sv-modal-header">
      <h3>Create new post</h3>
      <button type="button" class="sv-icon-btn" onclick="closeCreatePostModal()" aria-label="Close"><i class="ti ti-x"></i></button>
    </div>
    
    <div id="create-post-content" class="sv-modal-body sv-stack">
      <div id="step1-post-type">
        <p>What type of post would you like to create?</p>
        <div class="sv-choice-grid">
        <label class="sv-choice">
          <input type="radio" name="post-type" value="product" onchange="updatePostTypeUI()">
          <div><strong>Product post</strong><p class="sv-muted">Create a post about one of your products.</p></div>
        </label>
        <label class="sv-choice">
          <input type="radio" name="post-type" value="content" onchange="updatePostTypeUI()">
          <div><strong>Content post</strong><p class="sv-muted">Create a meme, quote, or engagement post.</p></div>
        </label>
        </div>
      </div>
      
      <div id="step2-product" class="sv-hidden">
        <p>Select a product</p>
        <select id="product-selector">
          <option value="">Loading products...</option>
        </select>
      </div>
      
      <div id="step2-category" class="sv-hidden">
        <p>Select content category</p>
        <label class="sv-choice">
          <input type="radio" name="content-category" value="meme"> 😂 Meme
        </label>
        <label class="sv-choice">
          <input type="radio" name="content-category" value="quote"> ✨ Quote
        </label>
      </div>
      
      <div id="step3-generate" class="sv-hidden">
        <button type="button" class="sv-btn sv-btn-primary" onclick="generatePostContent()">Generate content</button>
      </div>
      
      <div id="step4-preview" class="sv-hidden">
        <p>Preview</p>
        <textarea id="generated-post-text" readonly rows="5"></textarea>
      </div>
      
      <div id="step5-platforms" class="sv-hidden">
        <p>Select platforms to publish to</p>
        <label class="sv-checkbox-row">
          <input type="checkbox" id="platform-facebook" checked> 📘 Facebook Pages
        </label>
        <div id="facebook-pages-list" class="sv-hidden"></div>
        
        <label class="sv-checkbox-row">
          <input type="checkbox" id="platform-instagram" checked> 📷 Instagram
        </label>
        <div id="instagram-accounts-list" class="sv-hidden"></div>
      </div>
      
      <div id="step6-actions" class="sv-inline-actions sv-hidden">
        <button type="button" class="sv-btn sv-btn-primary" onclick="publishPost()">Publish</button>
        <button type="button" class="sv-btn sv-btn-secondary" onclick="closeCreatePostModal()">Cancel</button>
      </div>
    </div>
  </div>
</div>


<script>
  const storeId = '{store_id}';
  let currentAutopilotState = false;
  let selectedPostIds = new Set();

  async function loadAutopilotStatus() {{
    try {{
      const data = await fetchJson(`/api/posts/autopilot/${{storeId}}`);
      currentAutopilotState = data.autopilot_enabled;
      document.getElementById('autopilot-toggle').checked = data.autopilot_enabled;
      updateAutopilotDisplay();
    }} catch(e) {{
      console.error('Error loading autopilot status:', e);
    }}
  }}

  async function toggleAutopilot() {{
    const newState = !document.getElementById('autopilot-toggle').checked;
    try {{
      const data = await fetchJson(`/api/posts/autopilot/${{storeId}}/toggle`, {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{enabled: newState}})
      }});
      currentAutopilotState = data.autopilot_enabled;
      document.getElementById('autopilot-toggle').checked = data.autopilot_enabled;
      updateAutopilotDisplay();
    }} catch(e) {{
      alert('Error toggling autopilot: ' + e);
      document.getElementById('autopilot-toggle').checked = !newState;
    }}
  }}

  function updateAutopilotDisplay() {{
    const statusEl = document.getElementById('autopilot-status');
    if (currentAutopilotState) {{
      statusEl.className = 'sv-pill sv-pill-success';
      statusEl.innerHTML = '<span class="sv-dot is-live"></span> Autopilot is on';
    }} else {{
      statusEl.className = 'sv-pill sv-pill-neutral';
      statusEl.textContent = 'Autopilot is off';
    }}
  }}

  async function loadPosts() {{
    try {{
      const data = await fetchJson(`/api/posts/store/${{storeId}}`);
      renderPostsList(data.posts, data.autopilot_enabled);
    }} catch(e) {{
      console.error('Error loading posts:', e);
      document.getElementById('posts-container').innerHTML = '<p class="sv-muted">Error loading posts</p>';
    }}
  }}

  function renderPostsList(posts, autopilotEnabled) {{
    const container = document.getElementById('posts-container');
    
    if (!posts || posts.length === 0) {{
      container.innerHTML = '<div class="sv-empty"><span class="sv-empty-icon"><i class="ti ti-photo-off"></i></span><h3>No posts yet</h3><p>Create your first post to start engaging customers across your connected channels.</p></div>';
      return;
    }}
    
    container.innerHTML = posts.map(post => {{
      const statusBadges = [];
      if (!post.knowledge_updated) statusBadges.push('<span class="sv-pill sv-pill-warning">Review knowledge</span>');
      if (post.autopilot_paused) {{
        statusBadges.push('<span class="sv-pill sv-pill-warning">Paused</span>');
      }} else if (autopilotEnabled) {{
        statusBadges.push('<span class="sv-pill sv-pill-success"><span class="sv-dot is-live"></span> Active</span>');
      }}
      
      return `
        <article class="sv-post-card">
          <div class="sv-post-head">
            <div class="sv-post-title">
            <input type="checkbox" class="post-checkbox" data-post-id="${{post.post_id}}" onchange="updateSelection()">
            <div class="sv-post-copy">
              <strong>${{post.message?.substring(0, 50) || '(No text)'}}...</strong>
              <p>${{statusBadges.join(' ')}}</p>
            </div>
          </div>
          </div>
          
          ${{post.image_url ? `<div class="sv-media-inline"><img src="${{post.image_url}}" alt="Post image" class="sv-post-thumb"></div>` : ''}}
          
          <p class="sv-muted">${{post.message || ''}}</p>
          
          <div class="sv-inline-actions">
            <button type="button" class="sv-btn sv-btn-secondary sv-btn-sm" onclick="showPostDetail('${{post.post_id}}', '${{post.message || ''}}', '${{post.knowledge || ''}}', '${{post.image_url || ''}}', ${{post.comment_count || 0}})">Edit knowledge</button>
            <button type="button" class="sv-btn sv-btn-ghost sv-btn-sm" onclick="showComments('${{post.post_id}}')">${{post.comment_count}} comments</button>
            <button type="button" class="sv-btn sv-btn-secondary sv-btn-sm" onclick="togglePostPause('${{post.post_id}}', ${{post.autopilot_paused}})">${{post.autopilot_paused ? 'Resume' : 'Pause'}}</button>
          </div>
        </article>
      `;
    }}).join('');
  }}

  function updateSelection() {{
    selectedPostIds.clear();
    document.querySelectorAll('.post-checkbox:checked').forEach(checkbox => {{
      selectedPostIds.add(checkbox.dataset.postId);
    }});
    
    const hasSelection = selectedPostIds.size > 0;
    document.getElementById('pause-selected-btn').classList.toggle('sv-hidden', !hasSelection);
    document.getElementById('resume-selected-btn').classList.toggle('sv-hidden', !hasSelection);
    
    const selectAllCheckbox = document.getElementById('select-all-posts');
    const allCheckboxes = document.querySelectorAll('.post-checkbox');
    selectAllCheckbox.checked = allCheckboxes.length > 0 && Array.from(allCheckboxes).every(cb => cb.checked);
  }}

  function toggleSelectAll() {{
    const checked = document.getElementById('select-all-posts').checked;
    document.querySelectorAll('.post-checkbox').forEach(cb => {{
      cb.checked = checked;
    }});
    updateSelection();
  }}

  async function bulkPauseSelected() {{
    if (selectedPostIds.size === 0) return;
    try {{
      await fetchJson(`/api/posts/posts/bulk-pause`, {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{ store_id: storeId, post_ids: Array.from(selectedPostIds) }})
      }});
      loadPosts();
      selectedPostIds.clear();
    }} catch(e) {{ alert('Error: ' + e); }}
  }}

  async function bulkResumeSelected() {{
    if (selectedPostIds.size === 0) return;
    try {{
      await fetchJson(`/api/posts/posts/bulk-resume`, {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{ store_id: storeId, post_ids: Array.from(selectedPostIds) }})
      }});
      loadPosts();
      selectedPostIds.clear();
    }} catch(e) {{ alert('Error: ' + e); }}
  }}

  async function togglePostPause(postId, isPaused) {{
    try {{
      const endpoint = isPaused ? 'resume' : 'pause';
      await fetchJson(`/api/posts/post/${{postId}}/${{endpoint}}`, {{ method: 'POST' }});
      loadPosts();
    }} catch(e) {{ alert('Error: ' + e); }}
  }}

  function showPostDetail(postId, message, knowledge, imageUrl, commentCount) {{
    const content = document.getElementById('post-detail-content');
    content.innerHTML = `
      <div class="sv-stack">
      <p><strong>Post message</strong></p>
      <textarea readonly rows="3">${{message}}</textarea>
      
      ${{imageUrl ? `<div class="sv-media-inline"><img src="${{imageUrl}}" class="sv-post-thumb"></div>` : ''}}
      
      <p><strong>Knowledge base</strong></p>
      <textarea id="knowledge-textarea" rows="5">${{knowledge || ''}}</textarea>
      
      <div class="sv-inline-actions"><button type="button" class="sv-btn sv-btn-primary" onclick="saveKnowledge('${{postId}}')">Save knowledge</button></div>
      <div class="sv-section-divider"><p>${{commentCount}} comment(s) <button type="button" class="sv-btn sv-btn-ghost sv-btn-sm" onclick="showComments('${{postId}}')">View comments</button></p></div>
      </div>
    `;
    document.getElementById('modal-title').textContent = 'Edit Post Knowledge';
    document.getElementById('post-detail-modal').style.display = 'block';
  }}

  async function saveKnowledge(postId) {{
    const knowledge = document.getElementById('knowledge-textarea').value;
    try {{
      await fetchJson(`/api/posts/post/${{postId}}/knowledge`, {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{knowledge}})
      }});
      alert('Saved!');
      closePostDetail();
      loadPosts();
    }} catch(e) {{ alert('Error: ' + e); }}
  }}

  async function showComments(postId) {{
    try {{
      const data = await fetchJson(`/api/posts/post/${{postId}}/comments`);
      const content = document.getElementById('post-detail-content');
      
      if (!data.comments || data.comments.length === 0) {{
        content.innerHTML = '<p class="sv-muted">No comments yet.</p>';
      }} else {{
        content.innerHTML = `<div class="sv-stack">${{data.comments.map(comment => `
          <div class="sv-section-divider">
            <strong>${{comment.sender_name || comment.sender_id}}</strong>: ${{comment.text}}
            ${{comment.replied ? `<p class="sv-muted">Reply: ${{comment.reply_text}}</p>` : ''}}
          </div>
        `).join('')}}</div>`;
      }}
      document.getElementById('modal-title').textContent = 'Comments';
      document.getElementById('post-detail-modal').style.display = 'block';
    }} catch(e) {{ alert('Error: ' + e); }}
  }}

  function closePostDetail() {{ document.getElementById('post-detail-modal').style.display = 'none'; }}

  let createPostState = {{ postType: null, productId: null, category: null, generatedText: '', selectedFacebookPages: [], selectedInstagramAccounts: [] }};

  async function openCreatePostModal() {{
    createPostState = {{ postType: null, productId: null, category: null, generatedText: '', selectedFacebookPages: [], selectedInstagramAccounts: [] }};
    document.querySelectorAll('[name="post-type"]').forEach(r => r.checked = false);
    document.querySelectorAll('[name="content-category"]').forEach(r => r.checked = false);
    
    document.getElementById('step1-post-type').classList.remove('sv-hidden');
    ['step2-product', 'step2-category', 'step3-generate', 'step4-preview', 'step5-platforms', 'step6-actions'].forEach(id => {{
      document.getElementById(id).classList.add('sv-hidden');
    }});
    document.getElementById('create-post-modal').style.display = 'block';
  }}

  function closeCreatePostModal() {{ document.getElementById('create-post-modal').style.display = 'none'; }}

  // Closes open modals if clicking outside the modal box
  window.onclick = function(event) {{
    const detailModal = document.getElementById('post-detail-modal');
    const createModal = document.getElementById('create-post-modal');
    if (event.target == detailModal) {{
      detailModal.style.display = 'none';
    }}
    if (event.target == createModal) {{
      createModal.style.display = 'none';
    }}
  }}

  function updatePostTypeUI() {{
    const selectedType = document.querySelector('[name="post-type"]:checked')?.value;
    createPostState.postType = selectedType;
    
    if (selectedType === 'product') {{
      document.getElementById('step2-product').classList.remove('sv-hidden');
      document.getElementById('step2-category').classList.add('sv-hidden');
      loadProducts();
      showNextStep();
    }} else if (selectedType === 'content') {{
      document.getElementById('step2-product').classList.add('sv-hidden');
      document.getElementById('step2-category').classList.remove('sv-hidden');
      showNextStep();
    }}
  }}

  async function loadProducts() {{
    try {{
      const products = await fetchJson(`/api/store/${{storeId}}/products`);
      const selector = document.getElementById('product-selector');
      if (!Array.isArray(products) || products.length === 0) {{
        selector.innerHTML = '<option value="">No products found</option>';
        return;
      }}
      selector.innerHTML = products.map(p => `<option value="${{p.id}}">${{p.name}} ($${{p.price}})</option>`).join('');
      selector.onchange = () => {{ createPostState.productId = selector.value; }};
    }} catch(e) {{ selector.innerHTML = '<option value="">Error</option>'; }}
  }}

  function showNextStep() {{
    if (createPostState.postType === 'product') {{
      document.getElementById('step3-generate').classList.remove('sv-hidden');
    }} else if (createPostState.postType === 'content') {{
      document.querySelectorAll('[name="content-category"]').forEach(radio => {{
        radio.onchange = () => {{
          createPostState.category = radio.value;
          document.getElementById('step3-generate').classList.remove('sv-hidden');
        }};
      }});
    }}
  }}

  async function generatePostContent() {{
    let endpoint = createPostState.postType === 'product' ? 'generate/product' : 'generate/content';
    let payload = createPostState.postType === 'product' 
      ? {{ product_id: document.getElementById('product-selector').value }} 
      : {{ category: createPostState.category }};
    
    try {{
      const response = await fetchJson(`/api/posts/${{endpoint}}?store_id=${{storeId}}`, {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify(payload)
      }});
      
      createPostState.generatedText = response.post_text;
      document.getElementById('generated-post-text').value = response.post_text;
      
      document.getElementById('step4-preview').classList.remove('sv-hidden');
      document.getElementById('step5-platforms').classList.remove('sv-hidden');
      document.getElementById('step6-actions').classList.remove('sv-hidden');
      await loadPlatformOptions();
    }} catch(e) {{ alert('Error: ' + e.message); }}
  }}

  async function loadPlatformOptions() {{
    try {{
      const fbData = await fetchJson(`/api/meta/connected-pages/${{storeId}}`);
      const fbList = document.getElementById('facebook-pages-list');
      if (fbData.pages?.length > 0) {{
        fbList.classList.remove('sv-hidden');
        fbList.innerHTML = fbData.pages.map(p => `<label class="sv-checkbox-row"><input type="checkbox" value="${{p.page_id}}" checked class="facebook-page-checkbox" onchange="updateSelectedPages()"> <span>${{p.page_name}}</span></label>`).join('');
        createPostState.selectedFacebookPages = fbData.pages.map(p => p.page_id);
      }}
    }} catch(e) {{}}
    
    try {{
      const igData = await fetchJson(`/api/meta/connected-instagram/${{storeId}}`);
      const igList = document.getElementById('instagram-accounts-list');
      if (igData.accounts?.length > 0) {{
        igList.classList.remove('sv-hidden');
        igList.innerHTML = igData.accounts.map(a => `<label class="sv-checkbox-row"><input type="checkbox" value="${{a.ig_user_id}}" checked class="instagram-account-checkbox" onchange="updateSelectedInstagram()"> <span>${{a.ig_username}}</span></label>`).join('');
        createPostState.selectedInstagramAccounts = igData.accounts.map(a => a.ig_user_id);
      }}
    }} catch(e) {{}}
  }}

  function updateSelectedPages() {{ createPostState.selectedFacebookPages = Array.from(document.querySelectorAll('.facebook-page-checkbox:checked')).map(cb => cb.value); }}
  function updateSelectedInstagram() {{ createPostState.selectedInstagramAccounts = Array.from(document.querySelectorAll('.instagram-account-checkbox:checked')).map(cb => cb.value); }}

  async function publishPost() {{
    const platforms = [];
    if (document.getElementById('platform-facebook').checked) platforms.push('facebook');
    if (document.getElementById('platform-instagram').checked) platforms.push('instagram');
    
    const payload = {{
      post_text: createPostState.generatedText,
      post_type: createPostState.postType === 'product' ? 'product' : createPostState.category,
      product_id: createPostState.productId || null,
      platforms: platforms,
      page_ids: createPostState.selectedFacebookPages,
      ig_user_ids: createPostState.selectedInstagramAccounts,
    }};
    
    try {{
      await fetchJson(`/api/posts/publish/${{storeId}}`, {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify(payload)
      }});
      alert('Published!');
      closeCreatePostModal();
      loadPosts();
    }} catch(e) {{ alert('Error: ' + e.message); }}
  }}

  document.addEventListener('DOMContentLoaded', () => {{
    loadAutopilotStatus();
    loadPosts();
    setInterval(loadPosts, 30000);
  }});

  function logout() {{
    fetch('/api/auth/logout', {{method: 'POST'}});
    window.location.href = '/';
  }}
</script>
"""

    return render_page("Post Management", body)
