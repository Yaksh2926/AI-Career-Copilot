import streamlit as st
from frontend.config import SESSION_KEYS

def show_saved_reports():
    """
    Renders saved reports history cached in the session state.
    """
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">Saved Career Records</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Review and download your saved cover letters, ATS scores, and evaluations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    saved_list = st.session_state.get(SESSION_KEYS["saved_reports"], [])
    
    if not saved_list:
        st.markdown("""
        <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💾</div>
            <h3 style="font-family:'Outfit', sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">No Saved Records</h3>
            <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;">Draft cover letters, ATS match audits, or resume reviews and save them to build a list.</p>
            <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="display:inline-block; width:auto; padding:8px 24px;">Go to Dashboard</a>
        </div>
        """, unsafe_allow_html=True)
        return
        
    # Option to clear all
    col1, col2 = st.columns([9, 3])
    with col2:
        if st.button("Purge All Saved Records", key="clear_all_saved_btn", use_container_width=True):
            st.session_state[SESSION_KEYS["saved_reports"]] = []
            st.toast("Records purged!", icon="🧹")
            st.rerun()
            
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    for idx, report in enumerate(reversed(saved_list)):
        rep_type = report.get("type", "Analysis")
        filename = report.get("filename", "Unknown File")
        score = report.get("score", 0)
        timestamp = report.get("timestamp", "")
        details = report.get("details", "")
        
        # Color borders based on report type
        if "ATS" in rep_type:
            border_c = "#3B82F6"
            icon = "🎯"
            score_badge = f"<span class='chip chip-primary' style='border-color: rgba(59, 130, 246, 0.25); color: #3B82F6;'>Score: {score}%</span>"
        elif "Resume" in rep_type:
            border_c = "#22C55E"
            icon = "📊"
            score_badge = f"<span class='chip chip-success'>Index: {score}%</span>"
        elif "Cover" in rep_type:
            border_c = "#A855F7"
            icon = "✉️"
            score_badge = ""
        else:
            border_c = "#7C3AED"
            icon = "🗺️"
            score_badge = ""
            
        header_html = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div style="text-align: left;">
                    <strong style="color: #FFFFFF; font-size: 1rem; font-family: 'Outfit', sans-serif;">{rep_type} &bull; {filename}</strong>
                    <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Saved at: {timestamp}</div>
                </div>
            </div>
            <div>
                {score_badge}
            </div>
        </div>
        """
        
        # Use st.expander styled like a card to house details
        with st.expander(f"{icon} {rep_type} - {filename} ({timestamp})", expanded=False):
            st.markdown(f"<pre style='background: rgba(0,0,0,0.3); padding: 16px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; font-size: 0.85rem; color:#E2E8F0; border: 1px solid rgba(255,255,255,0.05);'>{details}</pre>", unsafe_allow_html=True)
            
            # Action to download
            st.download_button(
                label="⬇️ Download Markdown Copy",
                data=details,
                file_name=f"{rep_type.lower().replace(' ', '_')}_{idx}.md",
                mime="text/markdown",
                key=f"dl_saved_{idx}"
            )
