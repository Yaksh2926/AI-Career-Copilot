import streamlit as st

def show_settings():
    """
    Renders SaaS configuration preferences, notifications settings, and mock API bindings.
    """
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 class="hero-title" style="font-size: 2.5rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 0.25rem;">Workspace Settings</h1>
        <p style="color: #94A3B8; font-size: 0.95rem;">Configure your preferences, notification metrics, and Gemini API bindings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([7, 5], gap="large")
    
    with col1:
        st.markdown("<div class='glass-card' style='padding: 2.25rem 2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size: 1.25rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1.5rem;'>Platform Preferences</h3>", unsafe_allow_html=True)
        
        # Email settings
        st.checkbox("Receive weekly email reports on ATS scoring updates", value=True, key="settings_email_weekly")
        st.checkbox("Enable real-time notification alerts for saved reports", value=True, key="settings_notifications")
        st.checkbox("Sync candidate workspace details across local devices", value=False, key="settings_sync")
        st.checkbox("Opt-in to anonymous quality feedback metrics for Copilot model tuning", value=True, key="settings_telemetry")
        
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Save Preferences Action Button
        if st.button("Save Workspace Preferences", key="save_settings_pref"):
            st.success("Preferences updated successfully!")
            st.toast("Settings saved!", icon="💾")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card' style='padding: 2.25rem 2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size: 1.25rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1.5rem;'>Gemini API Integration</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.8rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;'>To bypass default server rate limits, enter your personal Google Gemini API key below. This token remains locally cached in your secure session space.</p>", unsafe_allow_html=True)
        
        gemini_key = st.text_input("Gemini API Key Override", type="password", placeholder="AIzaSy...", key="settings_gemini_key")
        
        if st.button("Apply API Key Override", key="apply_gemini_key"):
            if gemini_key.strip():
                st.success("API Key applied! Connecting Copilot backend engine to your direct key instance...")
                st.toast("Gemini API Key override active", icon="⚡")
            else:
                st.info("API Key override cleared. System will revert to sandbox server bindings.")
                
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card' style='padding: 2.25rem 2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size: 1.25rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1.5rem;'>Sandbox Diagnostics</h3>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 16px;">
            <div>
                <span style="font-size: 0.8rem; color: #94A3B8; display: block;">Localhost Gateway Binding</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: #22C55E; font-weight: 600;">✓ Healthy (Port 8000)</span>
            </div>
            <div>
                <span style="font-size: 0.8rem; color: #94A3B8; display: block;">Copilot App Version</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: #FFFFFF; font-weight: 600;">v1.4.2-premium</span>
            </div>
            <div>
                <span style="font-size: 0.8rem; color: #94A3B8; display: block;">Server Architecture</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: #FFFFFF; font-weight: 600;">FastAPI & Streamlit SPA</span>
            </div>
            <div>
                <span style="font-size: 0.8rem; color: #94A3B8; display: block;">Session Runtime</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; color: #FFFFFF; font-weight: 600;">Python 3.12 Environment</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
