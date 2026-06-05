from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .common import render_page
from app.lib.config import settings

router = APIRouter()

@router.get("/posts/{store_id}", response_class=HTMLResponse)
async def post_management(store_id: str):
    print(f"Rendering post management page for store {store_id} in {settings.ENVIRONMENT} environment")
    body = f"""
<style>
  /* Basic layout styles */
  .actions {{ margin-bottom: 20px; }}
  
  /* Modal Overlay Background */
  .modal {{
    display: none; 
    position: fixed; 
    z-index: 1000; 
    left: 0;
    top: 0;
    width: 100%; 
    height: 100%; 
    overflow: auto; 
    background-color: rgba(0, 0, 0, 0.5); 
  }}

  /* Modal Body Box */
  .modal-content {{
    background-color: #fefefe;
    margin: 10% auto; 
    padding: 20px;
    border: 1px solid #888;
    width: 60%; 
    max-width: 600px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    position: relative;
  }}

  /* Modal Header Design */
  .modal-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
    margin-bottom: 15px;
  }}
  
  .modal-header h3 {{
    margin: 0;
  }}

  .close-btn {{
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #aaa;
  }}
  
  .close-btn:hover {{
    color: #000;
  }}
</style>

<h1>Post Management & Autopilot</h1>
<p>Manage your social media posts and enable automatic comment responses.</p>

<div class="actions">
  <a href="/stores/{store_id}">Back to store</a> | 
  <a href="/dashboard">Dashboard</a> | 
  <button type="button" onclick="logout()">Logout</button>
</div>

<hr>

<section>
  <h2>Autopilot Control</h2>
  <p>When enabled, the bot will automatically reply to comments on your posts using the post knowledge.</p>
  <div>
    <label>
      <input type="checkbox" id="autopilot-toggle">
      Enable Autopilot
    </label>
    <button type="button" onclick="toggleAutopilot()">Save</button>
    <span id="autopilot-status"></span>
  </div>
</section>

<hr>

<section>
  <h2>Your Posts</h2>
  
  <div>
    <button type="button" onclick="openCreatePostModal()">✏️ New Post</button>
    <button type="button" onclick="loadPosts()">Refresh</button>
  </div>
  
  <br>
  
  <div>
    <label>
      <input type="checkbox" id="select-all-posts" onchange="toggleSelectAll()">
      Select All
    </label>
    <button type="button" id="pause-selected-btn" onclick="bulkPauseSelected()" style="display:none;">⏸ Pause Selected</button>
    <button type="button" id="resume-selected-btn" onclick="bulkResumeSelected()" style="display:none;">▶ Resume Selected</button>
  </div>
  
  <div id="posts-container">
    <p>Loading posts...</p>
  </div>
</section>

<!-- Post Details / Comments Modal -->
<div id="post-detail-modal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h3 id="modal-title">Post Details</h3>
      <button type="button" class="close-btn" onclick="closePostDetail()">×</button>
    </div>
    <div id="post-detail-content"></div>
  </div>
</div>

<!-- Create New Post Modal -->
<div id="create-post-modal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Create New Post</h3>
      <button type="button" class="close-btn" onclick="closeCreatePostModal()">×</button>
    </div>
    
    <div id="create-post-content">
      <div id="step1-post-type">
        <p>What type of post would you like to create?</p>
        <label>
          <input type="radio" name="post-type" value="product" onchange="updatePostTypeUI()">
          <strong>📦 Product Post</strong> (Post about one of your products)
        </label>
        <br>
        <label>
          <input type="radio" name="post-type" value="content" onchange="updatePostTypeUI()">
          <strong>💡 Content Post</strong> (Meme, quote, or engagement post)
        </label>
      </div>
      
      <div id="step2-product" style="display:none;">
        <p>Select a product</p>
        <select id="product-selector">
          <option value="">Loading products...</option>
        </select>
      </div>
      
      <div id="step2-category" style="display:none;">
        <p>Select content category</p>
        <label>
          <input type="radio" name="content-category" value="meme"> 😂 Meme
        </label>
        <label>
          <input type="radio" name="content-category" value="quote"> ✨ Quote
        </label>
      </div>
      
      <div id="step3-generate" style="display:none;">
        <br>
        <button type="button" onclick="generatePostContent()">✨ Generate Content</button>
      </div>
      
      <div id="step4-preview" style="display:none;">
        <p>Preview</p>
        <textarea id="generated-post-text" readonly rows="5" style="width: 100%; box-sizing: border-box;"></textarea>
      </div>
      
      <div id="step5-platforms" style="display:none;">
        <p>Select platforms to publish to</p>
        <label>
          <input type="checkbox" id="platform-facebook" checked> 📘 Facebook Pages
        </label>
        <div id="facebook-pages-list" style="margin-left:20px; display:none;"></div>
        
        <br>
        <label>
          <input type="checkbox" id="platform-instagram" checked> 📷 Instagram
        </label>
        <div id="instagram-accounts-list" style="margin-left:20px; display:none;"></div>
      </div>
      
      <div id="step6-actions" style="display:none;">
        <br>
        <button type="button" onclick="publishPost()">📤 Publish</button>
        <button type="button" onclick="closeCreatePostModal()">Cancel</button>
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
      statusEl.textContent = ' ✓ Autopilot is ON';
    }} else {{
      statusEl.textContent = ' ✗ Autopilot is OFF';
    }}
  }}

  async function loadPosts() {{
    try {{
      const data = await fetchJson(`/api/posts/store/${{storeId}}`);
      renderPostsList(data.posts, data.autopilot_enabled);
    }} catch(e) {{
      console.error('Error loading posts:', e);
      document.getElementById('posts-container').innerHTML = '<p>Error loading posts</p>';
    }}
  }}

  function renderPostsList(posts, autopilotEnabled) {{
    const container = document.getElementById('posts-container');
    
    if (!posts || posts.length === 0) {{
      container.innerHTML = '<p>No posts yet.</p>';
      return;
    }}
    
    container.innerHTML = posts.map(post => {{
      const statusBadges = [];
      if (!post.knowledge_updated) statusBadges.push('[Review Knowledge]');
      if (post.autopilot_paused) {{
        statusBadges.push('[Paused]');
      }} else if (autopilotEnabled) {{
        statusBadges.push('[Active]');
      }}
      
      return `
        <div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
          <div>
            <input type="checkbox" class="post-checkbox" data-post-id="${{post.post_id}}" onchange="updateSelection()">
            <strong>${{post.message?.substring(0, 50) || '(No Text)'}}...</strong>
            <span>${{statusBadges.join(' ')}}</span>
          </div>
          
          ${{post.image_url ? `<p><img src="${{post.image_url}}" alt="Post image" style="max-width:150px;"></p>` : ''}}
          
          <p>${{post.message || ''}}</p>
          
          <div>
            <button type="button" onclick="showPostDetail('${{post.post_id}}', '${{post.message || ''}}', '${{post.knowledge || ''}}', '${{post.image_url || ''}}', ${{post.comment_count || 0}})">📝 Edit Knowledge</button>
            <button type="button" onclick="showComments('${{post.post_id}}')">${{post.comment_count}} 💬 Comments</button>
            <button type="button" onclick="togglePostPause('${{post.post_id}}', ${{post.autopilot_paused}})">${{post.autopilot_paused ? '▶ Resume' : '⏸ Pause'}}</button>
          </div>
        </div>
      `;
    }}).join('');
  }}

  function updateSelection() {{
    selectedPostIds.clear();
    document.querySelectorAll('.post-checkbox:checked').forEach(checkbox => {{
      selectedPostIds.add(checkbox.dataset.postId);
    }});
    
    const hasSelection = selectedPostIds.size > 0;
    document.getElementById('pause-selected-btn').style.display = hasSelection ? 'inline-block' : 'none';
    document.getElementById('resume-selected-btn').style.display = hasSelection ? 'inline-block' : 'none';
    
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
      <p><strong>Post Message:</strong></p>
      <textarea readonly rows="3" style="width: 100%; box-sizing: border-box;">${{message}}</textarea>
      
      ${{imageUrl ? `<p><img src="${{imageUrl}}" style="max-width:150px;"></p>` : ''}}
      
      <p><strong>Knowledge Base:</strong></p>
      <textarea id="knowledge-textarea" rows="5" style="width: 100%; box-sizing: border-box;">${{knowledge || ''}}</textarea>
      
      <p><button type="button" onclick="saveKnowledge('${{postId}}')">Save Knowledge</button></p>
      <hr>
      <p>${{commentCount}} comment(s) <button type="button" onclick="showComments('${{postId}}')">View Comments</button></p>
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
        content.innerHTML = '<p>No comments yet.</p>';
      }} else {{
        content.innerHTML = data.comments.map(comment => `
          <div style="border-bottom: 1px dashed #ccc; padding: 5px 0;">
            <strong>${{comment.sender_name || comment.sender_id}}</strong>: ${{comment.text}}
            ${{comment.replied ? `<p style="margin-left:20px; color:green;">↳ Bot: ${{comment.reply_text}}</p>` : ''}}
          </div>
        `).join('');
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
    
    document.getElementById('step1-post-type').style.display = 'block';
    ['step2-product', 'step2-category', 'step3-generate', 'step4-preview', 'step5-platforms', 'step6-actions'].forEach(id => {{
      document.getElementById(id).style.display = 'none';
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
      document.getElementById('step2-product').style.display = 'block';
      document.getElementById('step2-category').style.display = 'none';
      loadProducts();
      showNextStep();
    }} else if (selectedType === 'content') {{
      document.getElementById('step2-product').style.display = 'none';
      document.getElementById('step2-category').style.display = 'block';
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
      document.getElementById('step3-generate').style.display = 'block';
    }} else if (createPostState.postType === 'content') {{
      document.querySelectorAll('[name="content-category"]').forEach(radio => {{
        radio.onchange = () => {{
          createPostState.category = radio.value;
          document.getElementById('step3-generate').style.display = 'block';
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
      
      document.getElementById('step4-preview').style.display = 'block';
      document.getElementById('step5-platforms').style.display = 'block';
      document.getElementById('step6-actions').style.display = 'block';
      await loadPlatformOptions();
    }} catch(e) {{ alert('Error: ' + e.message); }}
  }}

  async function loadPlatformOptions() {{
    try {{
      const fbData = await fetchJson(`/api/meta/connected-pages/${{storeId}}`);
      const fbList = document.getElementById('facebook-pages-list');
      if (fbData.pages?.length > 0) {{
        fbList.style.display = 'block';
        fbList.innerHTML = fbData.pages.map(p => `<label><input type="checkbox" value="${{p.page_id}}" checked class="facebook-page-checkbox" onchange="updateSelectedPages()"> ${{p.page_name}}</label><br>`).join('');
        createPostState.selectedFacebookPages = fbData.pages.map(p => p.page_id);
      }}
    }} catch(e) {{}}
    
    try {{
      const igData = await fetchJson(`/api/meta/connected-instagram/${{storeId}}`);
      const igList = document.getElementById('instagram-accounts-list');
      if (igData.accounts?.length > 0) {{
        igList.style.display = 'block';
        igList.innerHTML = igData.accounts.map(a => `<label><input type="checkbox" value="${{a.ig_user_id}}" checked class="instagram-account-checkbox" onchange="updateSelectedInstagram()"> ${{a.ig_username}}</label><br>`).join('');
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