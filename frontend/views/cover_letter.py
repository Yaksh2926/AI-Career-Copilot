import streamlit as st
from frontend.config import SESSION_KEYS
from frontend.api import api_generate_cover_letter
from frontend.components.document_preview import render_document_preview
import time

def show_cover_letter():
    """
    Displays the Cover Letter Generator Page.
    """
    # 1. Check if a resume is uploaded
    filename = st.session_state.get(SESSION_KEYS["filename"])
    
    if not filename:
        st.markdown("""
        <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">✉️</div>
            <h3 style="font-family:'Outfit', sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">No Active Resume Selected</h3>
            <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;">You need to upload your resume on the Dashboard first to draft matching cover letters.</p>
            <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="display:inline-block; width:auto; padding:8px 24px;">Go to Dashboard</a>
        </div>
        """, unsafe_allow_html=True)
        return
        
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">Cover Letter Architect</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Draft a professional cover letter linking <strong>{filename}</strong> with job postings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2 Form Inputs
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1rem; color:#FFFFFF; margin-bottom:0.5rem;'>Target Company Name</h3>", unsafe_allow_html=True)
        company_input = st.text_input("Company name input", placeholder="e.g. Vercel, Linear, Google...", label_visibility="collapsed", key="cl_company_input")
    with col2:
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1rem; color:#FFFFFF; margin-bottom:0.5rem;'>Target Job Role</h3>", unsafe_allow_html=True)
        role_input = st.text_input("Job role input", placeholder="e.g. Senior Frontend Engineer, Product Designer...", label_visibility="collapsed", key="cl_role_input")
        
    # Process cover letter drafting
    run_cl = st.button("Draft Cover Letter", key="run_cl_btn", use_container_width=True)
    
    # Read cached cover letter if available
    cached_cl = st.session_state.get(SESSION_KEYS["cover_letter"])
    
    if run_cl and company_input.strip() and role_input.strip():
        with st.spinner(""):
            status_container = st.empty()
            steps = ["Loading Resume Profile...", "Extracting Best Core Experiences...", "Writing Professional Opening...", "Structuring Custom Fit Value Proposition...", "Polishing Call-to-action & Signature..."]
            for step in steps:
                status_container.markdown(f"""
                <div class="premium-loader-container">
                    <div class="premium-loader-circle"></div>
                    <div class="loader-status-text">{step}</div>
                    <div class="loader-sub-text">Formatting professional letters with Gemini</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.7)
                
            res = api_generate_cover_letter(filename, company_input.strip(), role_input.strip())
            
            if res.get("success"):
                cached_cl = res["data"]["cover_letter"]
                st.session_state[SESSION_KEYS["cover_letter"]] = cached_cl
                st.toast("Cover letter drafted!", icon="✉️")
            else:
                status_container.empty()
                st.error(res.get("message", "Cover letter drafting failed"))
                return
            status_container.empty()
            
    if cached_cl:
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
        
        # Render document preview component
        title_str = f"Cover Letter - {role_input} at {company_input}" if (company_input and role_input) else "Cover Letter Document"
        render_document_preview(title_str, cached_cl)
        
        # Save Report
        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        if st.button("Save Cover Letter to History", key="save_cover_letter_btn"):
            saved = st.session_state.get(SESSION_KEYS["saved_reports"], [])
            saved.append({
                "type": "Cover Letter",
                "filename": filename,
                "score": 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "details": f"Company: {company_input}\nRole: {role_input}\n\nDocument:\n{cached_cl}"
            })
            st.session_state[SESSION_KEYS["saved_reports"]] = saved
            st.toast("Cover letter saved!", icon="💾")
    elif run_cl:
        st.warning("Please fill in both the Company Name and Job Role fields.")
