import time
import streamlit as st
from frontend.api import api_upload_resume
from frontend.config import SESSION_KEYS


def render_upload_card():
    """
    Renders a premium upload card container and processes uploaded PDF files.
    Caches the results in st.session_state so the user doesn't have to upload again.
    """
    # If already uploaded, show file success card
    if st.session_state.get(SESSION_KEYS["filename"]):
        filename = st.session_state.get(SESSION_KEYS["filename"])
        success_card_html = f"""
        <div class="glass-card" style="padding: 2rem; border-radius: 16px; border: 1px solid rgba(34, 197, 94, 0.3); text-align: center; background: rgba(34, 197, 94, 0.02);">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📄</div>
            <h3 style="font-family: 'Outfit', sans-serif; font-weight: 600; margin-bottom: 0.5rem; color: #FFFFFF;">Resume Active</h3>
            <div style="font-size: 0.9rem; color: #22C55E; margin-bottom: 1.25rem;">
                <span class="chip chip-success" style="margin: 0;">✓ {filename}</span>
            </div>
            <p style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 1.5rem;">This resume will be automatically used for ATS scoring, roadmaps, interview prep, and optimizations.</p>
        </div>
        """
        st.markdown(success_card_html, unsafe_allow_html=True)
        
        # Add a small text button to upload a new resume
        if st.button("Upload a Different Resume", key="re_upload_btn"):
            st.session_state[SESSION_KEYS["filename"]] = None
            st.session_state[SESSION_KEYS["resume_analysis"]] = None
            st.session_state[SESSION_KEYS["ats_score"]] = None
            st.session_state[SESSION_KEYS["roadmap"]] = None
            st.session_state[SESSION_KEYS["interview"]] = None
            st.session_state[SESSION_KEYS["cover_letter"]] = None
            st.session_state[SESSION_KEYS["linkedin"]] = None
            st.rerun()
        return

    # If not uploaded, show upload card
    upload_ui_html = """
    <div class="custom-upload-card">
        <div class="upload-icon">📤</div>
        <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.25rem; color: #FFFFFF; margin-bottom: 8px;">Upload Resume</h3>
        <p style="font-size: 0.85rem; color: #94A3B8; line-height: 1.5; margin-bottom: 16px;">Drag and drop your PDF resume here, or choose file to upload.</p>
        <span class="chip chip-primary" style="font-size: 0.75rem; padding: 4px 10px;">PDF only (Max 10MB)</span>
    </div>
    """
    st.markdown(upload_ui_html, unsafe_allow_html=True)
    
    # Hidden label but active uploader
    uploaded_file = st.file_uploader(
        "Choose file", 
        type=["pdf"], 
        label_visibility="collapsed",
        key="resume_uploader"
    )
    
    if uploaded_file is not None:
        with st.spinner(""):
            # Setup loading states in UI
            status_container = st.empty()
            steps = ["Reading Resume...", "Extracting Skills...", "Analyzing Resume...", "Calling Gemini...", "Generating AI Response..."]
            for step in steps:
                status_container.markdown(f"""
                <div class="premium-loader-container">
                    <div class="premium-loader-circle"></div>
                    <div class="loader-status-text">{step}</div>
                    <div class="loader-sub-text">AI Career Copilot is building your profile</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.8)
                
            res = api_upload_resume(uploaded_file.name, uploaded_file.getvalue())
            
            if res.get("success"):
                st.session_state[SESSION_KEYS["filename"]] = res["data"]["filename"]
                st.session_state[SESSION_KEYS["resume_analysis"]] = res["data"]["analysis"]
                st.success(f"Resume uploaded and analyzed successfully: {uploaded_file.name}")
                st.rerun()
            else:
                status_container.empty()
                st.error(res.get("message", "Upload failed"))
