import streamlit as st
from frontend.config import SESSION_KEYS
from frontend.api import api_get_ats_score
from frontend.utils.parsers import parse_ats_score
from frontend.components.circular_progress import render_circular_progress
import time

def show_ats_score():
    """
    Displays the ATS Score Page, letting users paste job descriptions and compare resumes.
    """
    # 1. Check if a resume is uploaded
    filename = st.session_state.get(SESSION_KEYS["filename"])
    
    if not filename:
        st.markdown("""
        <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="font-family:'Outfit', sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">No Active Resume Selected</h3>
            <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;">You need to upload your resume on the Dashboard first to calculate ATS match rates.</p>
            <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="display:inline-block; width:auto; padding:8px 24px;">Go to Dashboard</a>
        </div>
        """, unsafe_allow_html=True)
        return
        
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">ATS Alignment Engine</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Test resume <strong>{filename}</strong> against specific job opportunities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input area for Job Description
    st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.1rem; color:#FFFFFF; margin-bottom:0.5rem;'>Job Description</h3>", unsafe_allow_html=True)
    jd_input = st.text_area(
        "Paste the job posting description here...", 
        height=180, 
        placeholder="Paste target job descriptions, requirements, and responsibilities here to assess match...",
        label_visibility="collapsed"
    )
    
    # Process calculations
    run_comparison = st.button("Generate Match Report", key="run_ats_comparison_btn", use_container_width=True)
    
    # Read cached analysis if available
    cached_res = st.session_state.get(SESSION_KEYS["ats_score"])
    
    # Reset cache if a new comparison is triggered and input is provided
    if run_comparison and jd_input.strip():
        with st.spinner(""):
            status_container = st.empty()
            steps = ["Reading Job Description...", "Matching Technical Terms...", "Scanning Keyword Frequencies...", "Calculating Match Coefficient...", "Structuring ATS Suggestions..."]
            for step in steps:
                status_container.markdown(f"""
                <div class="premium-loader-container">
                    <div class="premium-loader-circle"></div>
                    <div class="loader-status-text">{step}</div>
                    <div class="loader-sub-text">Calibrating applicant tracking system metrics</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.7)
                
            res = api_get_ats_score(filename, jd_input.strip())
            
            if res.get("success"):
                cached_res = res["data"]["ats_analysis"]
                st.session_state[SESSION_KEYS["ats_score"]] = cached_res
                st.toast("ATS report generated!", icon="🎯")
            else:
                status_container.empty()
                st.error(res.get("message", "ATS Calculation failed"))
                return
            status_container.empty()
            
    if cached_res:
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
        
        parsed = parse_ats_score(cached_res)
        score = parsed["score"]
        
        # Determine notification alert type based on score
        if score >= 80:
            border_color = "#22C55E"
            status_tag = "<span class='chip chip-success'>Excellent Match</span>"
        elif score >= 55:
            border_color = "#F59E0B"
            status_tag = "<span class='chip chip-warning'>Moderate Gaps</span>"
        else:
            border_color = "#EF4444"
            status_tag = "<span class='chip chip-danger'>Weak Alignment</span>"
            
        col1, col2 = st.columns([5, 7], gap="large")
        
        with col1:
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Alignment Rating</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="glass-card" style="padding: 1.5rem; border-radius: 14px; text-align: center; border-top: 4px solid {border_color};">
                <div style="margin-bottom: 1rem;">{status_tag}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Draw circular progress directly inside the container block
            render_circular_progress(score, "ATS Score")
            
        with col2:
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Keyword Audit</h3>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-card' style='padding: 1.5rem; border-radius: 12px; height: calc(100% - 2rem);'>", unsafe_allow_html=True)
            
            st.markdown("<strong style='font-size:0.9rem; color:#22C55E; display:block; margin-bottom:8px;'>✓ Matching Skills & Keywords</strong>", unsafe_allow_html=True)
            if parsed["matching_skills"]:
                chips = "".join([f"<span class='chip chip-success'>{s}</span>" for s in parsed["matching_skills"]])
                st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8;'>No matching keywords detected.</p>", unsafe_allow_html=True)
                
            st.markdown("<strong style='font-size:0.9rem; color:#F59E0B; display:block; margin-top:16px; margin-bottom:8px;'>⚠ Missing Skills</strong>", unsafe_allow_html=True)
            if parsed["missing_skills"]:
                chips = "".join([f"<span class='chip chip-warning'>{s}</span>" for s in parsed["missing_skills"]])
                st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#22C55E;'>No missing core skills detected!</p>", unsafe_allow_html=True)
                
            st.markdown("<strong style='font-size:0.9rem; color:#EF4444; display:block; margin-top:16px; margin-bottom:8px;'>✗ Critical Missing Keywords</strong>", unsafe_allow_html=True)
            if parsed["missing_keywords"]:
                chips = "".join([f"<span class='chip chip-danger'>{s}</span>" for s in parsed["missing_keywords"]])
                st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#22C55E;'>All critical keywords accounted for!</p>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Suggestions Section
        if parsed["suggestions"]:
            st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.25rem; color:#FFFFFF; margin-bottom:0.75rem;'>ATS Optimization Steps</h3>", unsafe_allow_html=True)
            
            sugg_html = ""
            for i, sug in enumerate(parsed["suggestions"]):
                sugg_html += f"""
                <div class="glass-card" style="padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 12px; border-left: 2px solid #7C3AED;">
                    <div style="font-size: 0.88rem; color: #E2E8F0;">{sug}</div>
                </div>
                """
            st.markdown(sugg_html, unsafe_allow_html=True)
            
        # Save Report
        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        if st.button("Save ATS Analysis Report", key="save_ats_btn"):
            saved = st.session_state.get(SESSION_KEYS["saved_reports"], [])
            saved.append({
                "type": "ATS Score",
                "filename": filename,
                "score": score,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "details": f"Job Posting Description:\n{jd_input}\n\nReport:\n{cached_res}"
            })
            st.session_state[SESSION_KEYS["saved_reports"]] = saved
            st.toast("ATS score report saved!", icon="💾")
    elif not jd_input.strip() and run_comparison:
        st.warning("Please paste a job description first.")
