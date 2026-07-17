import streamlit as st
import textwrap

def render_topbar():
    """
    Renders a unified top navbar with search features and a dynamic 
    hover profile menu featuring profile configurations and logout endpoints.
    """
    user = st.session_state.get("user", {})
    user_name = user.get("name", "Yaksh Jindal")
    user_email = user.get("email", "candidate@copilot.ai")
    user_avatar = user.get("avatar", "https://api.dicebear.com/7.x/identicon/svg?seed=CopilotUser")
    
    topbar_html = f"""
<div class="topbar">
    <div class="topbar-search">
        <span style="font-size: 0.85rem; margin-right: 8px;">🔍</span>
        <span style="font-size: 0.85rem; color:#64748B;">Search features, tools, roadmaps...</span>
    </div>
    <div class="topbar-actions">
        <div class="notification-bell">
            <span style="font-size: 1.1rem;">🔔</span>
            <div class="notification-dot"></div>
        </div>
        <div style="width: 1px; height: 24px; background: rgba(255,255,255,0.08); margin: 0 4px;"></div>
        
        <!-- User Dropdown Menu -->
        <div class="profile-dropdown-container">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="profile-avatar" style="background-image: url('{user_avatar}'); width: 32px; height: 32px; border: 2px solid #7C3AED;"></div>
                <div style="display: flex; flex-direction: column; text-align: left;">
                    <span style="font-size:0.8rem; font-weight:600; color:#FFFFFF; line-height: 1.1;">{user_name}</span>
                    <span style="font-size:0.65rem; color:#94A3B8;">{user_email}</span>
                </div>
                <span style="font-size: 0.55rem; color: #94A3B8; margin-left: 2px;">▼</span>
            </div>
            <div class="profile-dropdown-menu">
                <a href="/?page=profile" target="_self" class="profile-dropdown-item">
                    <span>👤</span> My Profile
                </a>
                <a href="/?page=settings" target="_self" class="profile-dropdown-item">
                    <span>⚙️</span> Settings
                </a>
                <div style="height: 1px; background: rgba(255,255,255,0.08); margin: 6px 0;"></div>
                <a href="/?logout=true" target="_self" class="profile-dropdown-item" style="color: #EF4444 !important; font-weight: 600;">
                    <span>🚪</span> Logout
                </a>
            </div>
        </div>
        
    </div>
</div>
"""
    st.html(topbar_html)


