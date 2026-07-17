import streamlit as st
from frontend.config import SESSION_KEYS
from frontend.utils.parsers import parse_resume_analysis
from frontend.components.circular_progress import render_circular_progress

def show_resume_analysis():
    """
    Displays the AI Resume Analysis page.
    """
    # 1. Check if a resume is uploaded
    filename = st.session_state.get(SESSION_KEYS["filename"])
    analysis_text = st.session_state.get(SESSION_KEYS["resume_analysis"])
    
    if not filename or not analysis_text:
        st.markdown(f"""
        <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="font-family:'Outfit', sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">No Active Resume Analyzed</h3>
            <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;">You need to upload your resume on the Dashboard first to view this analysis.</p>
            <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="display:inline-block; width:auto; padding:8px 24px;">Go to Dashboard</a>
        </div>
        """, unsafe_allow_html=True)
        return
        
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">Resume Analytics</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Comprehensive review of <strong>{filename}</strong> powered by Google Gemini.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Parse the cached markdown response
    sections = parse_resume_analysis(analysis_text)
    
    col1, col2 = st.columns([5, 7], gap="large")
    
    with col1:
        # Score and Summary Card
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Overall Health</h3>", unsafe_allow_html=True)
        
        score_card_content = f"""
        <div class="glass-card" style="padding: 1.5rem; border-radius: 14px; text-align: center;">
            <p style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 0.5rem;">Resume Quality Index</p>
        </div>
        """
        # Render Circular Progress Gauge
        render_circular_progress(sections["score"], "Quality Index")
        
        # Professional Summary Card
        if sections["summary"]:
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-top: 1.5rem; margin-bottom:0.75rem;'>Professional Summary</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card" style="padding: 1.5rem; border-radius: 14px; line-height: 1.6; font-size: 0.9rem; color: #E2E8F0;">
                {sections["summary"]}
            </div>
            """, unsafe_allow_html=True)
            
    with col2:
        # Strengths & Weaknesses
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Core Assessment</h3>", unsafe_allow_html=True)
        
        # Grid of Strengths and Weaknesses
        s_col, w_col = st.columns(2)
        with s_col:
            st.markdown("<div class='glass-card' style='padding: 1.25rem; border-radius: 12px; height: 100%; border-left: 3px solid #22C55E;'>", unsafe_allow_html=True)
            st.markdown("<strong style='color:#22C55E; font-size:0.95rem;'>⭐ Key Strengths</strong>", unsafe_allow_html=True)
            if sections["strengths"]:
                items_html = "".join([f"<li style='font-size:0.85rem; color:#E2E8F0; margin-bottom: 6px;'>{item}</li>" for item in sections["strengths"]])
                st.markdown(f"<ul style='padding-left:16px; margin-top:8px;'>{items_html}</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8; margin-top:8px;'>No strengths highlighted.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with w_col:
            st.markdown("<div class='glass-card' style='padding: 1.25rem; border-radius: 12px; height: 100%; border-left: 3px solid #EF4444;'>", unsafe_allow_html=True)
            st.markdown("<strong style='color:#EF4444; font-size:0.95rem;'>⚠️ Areas to Improve</strong>", unsafe_allow_html=True)
            if sections["weaknesses"]:
                items_html = "".join([f"<li style='font-size:0.85rem; color:#E2E8F0; margin-bottom: 6px;'>{item}</li>" for item in sections["weaknesses"]])
                st.markdown(f"<ul style='padding-left:16px; margin-top:8px;'>{items_html}</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8; margin-top:8px;'>No specific weaknesses found.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Skill Chips Layout
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-top: 1.5rem; margin-bottom:0.75rem;'>Skills Profiling</h3>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card' style='padding: 1.5rem; border-radius: 12px;'>", unsafe_allow_html=True)
        st.markdown("<strong style='font-size:0.9rem; color:#A855F7; display:block; margin-bottom:8px;'>Detected Technical Skills</strong>", unsafe_allow_html=True)
        if sections["skills"]:
            skills_html = "".join([f"<span class='chip chip-primary'>{s}</span>" for s in sections["skills"]])
            st.markdown(f"<div>{skills_html}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:0.85rem; color:#94A3B8;'>No skills listed.</p>", unsafe_allow_html=True)
            
        st.markdown("<strong style='font-size:0.9rem; color:#F59E0B; display:block; margin-top:16px; margin-bottom:8px;'>Identified Gaps / Missing Skills</strong>", unsafe_allow_html=True)
        if sections["missing_skills"]:
            missing_html = "".join([f"<span class='chip chip-warning'>{s}</span>" for s in sections["missing_skills"]])
            st.markdown(f"<div>{missing_html}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:0.85rem; color:#22C55E;'>No critical skill gaps identified!</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Suggestions for Improvement Block
    if sections["suggestions"]:
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.25rem; color:#FFFFFF; margin-bottom:0.75rem;'>Actionable Recommendations</h3>", unsafe_allow_html=True)
        
        sugg_html = ""
        for i, item in enumerate(sections["suggestions"]):
            sugg_html += f"""
            <div class="glass-card" style="padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 1.1rem; color: #7C3AED; font-weight: bold;">{i+1}</div>
                <div style="font-size: 0.88rem; color: #E2E8F0;">{item}</div>
            </div>
            """
        st.markdown(sugg_html, unsafe_allow_html=True)
        
    # Save Report Trigger
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    if st.button("Save this Report to Dashboard History", key="save_analysis_btn"):
        saved = st.session_state.get(SESSION_KEYS["saved_reports"], [])
        saved.append({
            "type": "Resume Analysis",
            "filename": filename,
            "score": sections["score"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "details": analysis_text
        })
        st.session_state[SESSION_KEYS["saved_reports"]] = saved
        st.toast("Report saved successfully!", icon="💾")
        
import time
