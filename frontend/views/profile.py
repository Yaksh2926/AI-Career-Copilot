import streamlit as st
from frontend.config import SESSION_KEYS

def show_profile():
    """
    Renders the Profile settings and user analysis statistics.
    """
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 class="hero-title" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 0.25rem;">Candidate Profile</h1>
        <p style="color: #94A3B8; font-size: 0.95rem;">Manage your sandbox account credentials and review uploaded resume history.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 7], gap="large")
    
    user = st.session_state.get("user", {})
    user_name = user.get("name", "Yaksh Jindal")
    user_email = user.get("email", "candidate@copilot.ai")
    user_avatar = user.get("avatar", "https://api.dicebear.com/7.x/identicon/svg?seed=CopilotUser")
    
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="padding: 2.5rem 2rem; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.01);">
            <div class="profile-avatar" style="background-image: url('{user_avatar}'); width: 96px; height: 96px; margin: 0 auto 1.5rem auto; border: 3px solid #7C3AED; box-shadow: 0 0 20px rgba(124, 58, 237, 0.3);"></div>
            <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.5rem; color: #FFFFFF; margin-bottom: 0.25rem;">{user_name}</h3>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 1.5rem;">{user_email}</div>
            <div class="chip chip-primary" style="margin: 0; font-size: 0.75rem; font-weight: 600;">SaaS Candidate Sandbox</div>
            
            <div style="width: 100%; height: 1px; background: rgba(255,255,255,0.06); margin: 2rem 0;"></div>
            
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div>
                    <div style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 800; color: #7C3AED;">1</div>
                    <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">Active Resume</div>
                </div>
                <div style="width: 1px; height: 30px; background: rgba(255,255,255,0.06);"></div>
                <div>
                    <div style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 800; color: #3B82F6;">4</div>
                    <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">Reports Saved</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card' style='padding: 2.25rem 2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size: 1.25rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1.5rem;'>Workspace Details</h3>", unsafe_allow_html=True)
        
        # Check active resume upload
        filename = st.session_state.get(SESSION_KEYS["filename"])
        if filename:
            st.markdown(f"""
            <div style="background: rgba(34, 197, 94, 0.04); border: 1px solid rgba(34, 197, 94, 0.2); border-radius: 10px; padding: 1.25rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.8rem; color: #94A3B8;">Active Resume Attachment</div>
                    <div style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 1rem; color: #FFFFFF; margin-top: 2px;">📄 {filename}</div>
                </div>
                <span class="chip chip-success" style="margin: 0; font-size: 0.7rem;">✓ Active</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(245, 158, 11, 0.04); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 10px; padding: 1.25rem; margin-bottom: 1.5rem;">
                <div style="font-size: 0.8rem; color: #94A3B8;">Active Resume Attachment</div>
                <div style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 0.95rem; color: #FFFFFF; margin-top: 2px;">No active resume uploaded.</div>
                <a href="/?page=dashboard" target="_self" style="font-size: 0.8rem; color: #3B82F6; text-decoration: underline; display: inline-block; margin-top: 6px;">Upload a PDF to analyze ➔</a>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 1rem;">
            <div>
                <span style="font-size: 0.8rem; color: #94A3B8; display: block;">Session Security Mode</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: #FFFFFF; font-weight: 600;">Simulated Secure OAuth Tokens</span>
            </div>
            <div>
                <span style="font-size: 0.8rem; color: #94A3B8; display: block;">Account Authorization Scope</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: #FFFFFF; font-weight: 600;">Global Read-Write User Sandbox</span>
            </div>
            <div>
                <span style="font-size: 0.8rem; color: #94A3B8; display: block;">API Environment Binding</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: #FFFFFF; font-weight: 600;">FastAPI Engine Localhost:8000</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
