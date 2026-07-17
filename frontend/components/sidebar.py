import streamlit as st

def render_sidebar():
    """
    Renders the custom HTML/CSS glassmorphic sidebar inside the Streamlit sidebar block.
    Uses target="_self" query-parameter links to facilitate smooth SPA-like navigation.
    """
    # Read active page from query parameter (defaults to dashboard)
    active_page = st.query_params.get("page", "dashboard")
    
    # Navigation items setup (id, icon, display name)
    nav_items = [
        ("dashboard", "⚡", "Dashboard"),
        ("resume_analysis", "📊", "Resume Analysis"),
        ("ats_score", "🎯", "ATS Score Checker"),
        ("career_roadmap", "🗺️", "Career Roadmap"),
        ("interview_prep", "💬", "Interview Prep"),
        ("cover_letter", "✉️", "Cover Letter Gen"),
        ("linkedin_optimizer", "💼", "LinkedIn Optimizer"),
        ("career_chat", "🤖", "Career Chat Mentor"),
        ("resources", "📚", "Career Resources"),
        ("saved_reports", "💾", "Saved Reports")
    ]
    
    # Build sidebar HTML
    logo_html = """
    <div class="sidebar-logo">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
            <path d="M12 2L2 22H22L12 2Z" fill="url(#logo-grad)" stroke="#A855F7" stroke-width="2" stroke-linejoin="round"/>
            <defs>
                <linearGradient id="logo-grad" x1="2" y1="22" x2="22" y2="2" gradientUnits="userSpaceOnUse">
                    <stop offset="0" stop-color="#7C3AED"/>
                    <stop offset="1" stop-color="#3B82F6"/>
                </linearGradient>
            </defs>
        </svg>
        <span class="sidebar-logo-text">COPILOT.AI</span>
    </div>
    """
    
    nav_links_html = '<div class="sidebar-nav">'
    for page_id, icon, label in nav_items:
        active_class = "active" if active_page == page_id else ""
        nav_links_html += f"""
        <a href="/?page={page_id}" target="_self" class="sidebar-item {active_class}">
            <span style="font-size:1.1rem;">{icon}</span>
            <span>{label}</span>
        </a>
        """
    nav_links_html += '</div>'
    
    upgrade_card_html = """
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0.5rem; border-top: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06); margin-top: 1rem; margin-bottom: 1.5rem;">
        <span style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">Dark Mode</span>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 0.75rem; color: #A855F7; font-weight: 600;">Active</span>
            <div style="width: 32px; height: 18px; background: #7C3AED; border-radius: 9px; position: relative; box-shadow: 0 0 8px #7C3AED;">
                <div style="width: 12px; height: 12px; background: #FFFFFF; border-radius: 50%; position: absolute; right: 3px; top: 3px;"></div>
            </div>
        </div>
    </div>
    <div class="sidebar-upgrade-card">
        <div style="font-family:'Outfit', sans-serif; font-weight:700; font-size:0.95rem; color:#FFFFFF; margin-bottom: 4px;">Upgrade to Pro</div>
        <div style="font-size:0.75rem; color:#94A3B8; line-height:1.4;">Access advanced resume analytics and mock coding interviews.</div>
        <a href="#" class="sidebar-upgrade-btn">Go Premium</a>
    </div>
    """
    
    # Render all elements as a single HTML block
    sidebar_html = f"""
    {logo_html}
    {nav_links_html}
    {upgrade_card_html}
    """
    
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
