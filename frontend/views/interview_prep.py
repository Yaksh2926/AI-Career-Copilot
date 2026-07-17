import streamlit as st
from frontend.config import SESSION_KEYS
from frontend.api import api_generate_interview_questions
from frontend.utils.parsers import parse_interview_questions
from frontend.components.accordion import render_accordion
import time

def show_interview_prep():
    """
    Displays the Interview Question Generator Page.
    """
    # 1. Check if a resume is uploaded
    filename = st.session_state.get(SESSION_KEYS["filename"])
    
    if not filename:
        st.markdown("""
        <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
            <h3 style="font-family:'Outfit', sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">No Active Resume Selected</h3>
            <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;">You need to upload your resume on the Dashboard first to compile matching interview questions.</p>
            <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="display:inline-block; width:auto; padding:8px 24px;">Go to Dashboard</a>
        </div>
        """, unsafe_allow_html=True)
        return
        
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">Interview Simulator</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Generate targeted mock questions customized to your resume <strong>{filename}</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input area for Role
    st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.1rem; color:#FFFFFF; margin-bottom:0.5rem;'>What is your Target Role?</h3>", unsafe_allow_html=True)
    role_input = st.text_input(
        "Enter role...", 
        placeholder="e.g. Lead Frontend Engineer, Senior Product Designer, Backend Engineer...",
        label_visibility="collapsed"
    )
    
    # Process calculations
    run_interview = st.button("Generate Interview Pack", key="run_interview_btn", use_container_width=True)
    
    # Read cached interview questions if available
    cached_interview = st.session_state.get(SESSION_KEYS["interview"])
    
    # Reset cache if a new comparison is triggered and input is provided
    if run_interview and role_input.strip():
        with st.spinner(""):
            status_container = st.empty()
            steps = ["Analyzing Experience Metrics...", "Aligning Target Role Requirements...", "Drafting Technical Inquiries...", "Writing Coding Challenges...", "Formulating Behavioral Scenarios...", "Structuring Review Pack..."]
            for step in steps:
                status_container.markdown(f"""
                <div class="premium-loader-container">
                    <div class="premium-loader-circle"></div>
                    <div class="loader-status-text">{step}</div>
                    <div class="loader-sub-text">Calibrating mock evaluations using Gemini</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.7)
                
            res = api_generate_interview_questions(filename, role_input.strip())
            
            if res.get("success"):
                cached_interview = res["data"]["questions"]
                st.session_state[SESSION_KEYS["interview"]] = cached_interview
                st.toast("Questions pack generated!", icon="💬")
            else:
                status_container.empty()
                st.error(res.get("message", "Mock generation failed"))
                return
            status_container.empty()
            
    if cached_interview:
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
        
        parsed = parse_interview_questions(cached_interview)
        
        # Display questions categories inside collapsible blocks
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            render_accordion("HR / Culture-Fit", parsed["hr"])
            render_accordion("Technical Core", parsed["technical"])
            render_accordion("Coding / Algorithms", parsed["coding"])
            
        with col2:
            render_accordion("Resume-Based Specifics", parsed["resume"])
            render_accordion("Project Deep-dives", parsed["project"])
            render_accordion("Scenario / Behavioral", parsed["scenario"])
            
        # Save Report
        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        if st.button("Save Interview Questions Pack", key="save_interview_btn"):
            saved = st.session_state.get(SESSION_KEYS["saved_reports"], [])
            saved.append({
                "type": "Interview Prep",
                "filename": filename,
                "score": 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "details": f"Target Role: {role_input}\n\nQuestions:\n{cached_interview}"
            })
            st.session_state[SESSION_KEYS["saved_reports"]] = saved
            st.toast("Interview pack saved!", icon="💾")
    elif not role_input.strip() and run_interview:
        st.warning("Please enter your target role first.")
