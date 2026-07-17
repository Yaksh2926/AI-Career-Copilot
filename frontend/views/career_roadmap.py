import streamlit as st
from frontend.config import SESSION_KEYS
from frontend.api import api_generate_career_roadmap
from frontend.utils.parsers import parse_career_roadmap
from frontend.components.timeline import render_timeline
import time

def show_career_roadmap():
    """
    Displays the Career Roadmap Generation Page.
    """
    # 1. Check if a resume is uploaded
    filename = st.session_state.get(SESSION_KEYS["filename"])
    
    if not filename:
        st.markdown("""
        <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🗺️</div>
            <h3 style="font-family:'Outfit', sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">No Active Resume Selected</h3>
            <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;">You need to upload your resume on the Dashboard first to model your learning roadmap.</p>
            <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="display:inline-block; width:auto; padding:8px 24px;">Go to Dashboard</a>
        </div>
        """, unsafe_allow_html=True)
        return
        
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">AI Career Roadmap</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Map out your professional trajectory from <strong>{filename}</strong> to your target goals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input area for Career Goal
    st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.1rem; color:#FFFFFF; margin-bottom:0.5rem;'>What is your Target Career Goal?</h3>", unsafe_allow_html=True)
    goal_input = st.text_input(
        "Enter goal...", 
        placeholder="e.g. Senior Frontend Architect, Staff ML Engineer, Technical Product Manager...",
        label_visibility="collapsed"
    )
    
    # Process calculations
    run_roadmap = st.button("Compile Learning Roadmap", key="run_roadmap_btn", use_container_width=True)
    
    # Read cached roadmap if available
    cached_roadmap = st.session_state.get(SESSION_KEYS["roadmap"])
    
    # Reset cache if a new comparison is triggered and input is provided
    if run_roadmap and goal_input.strip():
        with st.spinner(""):
            status_container = st.empty()
            steps = ["Assessing Base Skills...", "Identifying Skill Gaps...", "Drafting Certification Pathway...", "Formulating Monthly Milestones...", "Designing Recommended Projects...", "Assembling Interview Techniques..."]
            for step in steps:
                status_container.markdown(f"""
                <div class="premium-loader-container">
                    <div class="premium-loader-circle"></div>
                    <div class="loader-status-text">{step}</div>
                    <div class="loader-sub-text">Calibrating learning trajectories using Gemini</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.7)
                
            res = api_generate_career_roadmap(filename, goal_input.strip())
            
            if res.get("success"):
                cached_roadmap = res["data"]["roadmap"]
                st.session_state[SESSION_KEYS["roadmap"]] = cached_roadmap
                st.toast("Roadmap compiled successfully!", icon="🗺️")
            else:
                status_container.empty()
                st.error(res.get("message", "Roadmap compilation failed"))
                return
            status_container.empty()
            
    if cached_roadmap:
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
        
        parsed = parse_career_roadmap(cached_roadmap)
        
        col1, col2 = st.columns([5, 7], gap="large")
        
        with col1:
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Skills Breakdown</h3>", unsafe_allow_html=True)
            
            # Base stats card
            st.markdown(f"""
            <div class="glass-card" style="padding: 1.25rem 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <span style="font-size: 0.8rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.5px;">Assessed Skill Level</span>
                <h4 style="font-family:'Outfit', sans-serif; font-size:1.35rem; font-weight:700; color:#A855F7; margin-top:4px; margin-bottom:0;">
                    {parsed["current_level"]}
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Known vs missing list
            st.markdown("<div class='glass-card' style='padding: 1.25rem; border-radius: 12px;'>", unsafe_allow_html=True)
            
            st.markdown("<strong style='font-size:0.9rem; color:#22C55E; display:block; margin-bottom:8px;'>✓ Acquired Skills</strong>", unsafe_allow_html=True)
            if parsed["known_skills"]:
                chips = "".join([f"<span class='chip chip-success'>{s}</span>" for s in parsed["known_skills"]])
                st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8;'>No known skills listed.</p>", unsafe_allow_html=True)
                
            st.markdown("<strong style='font-size:0.9rem; color:#F59E0B; display:block; margin-top:16px; margin-bottom:8px;'>⚠ Skill Gaps to Bridge</strong>", unsafe_allow_html=True)
            if parsed["skills_to_learn"]:
                chips = "".join([f"<span class='chip chip-warning'>{s}</span>" for s in parsed["skills_to_learn"]])
                st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#22C55E;'>Ready to apply! No critical gaps.</p>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Projects & Certifications
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-top: 1.5rem; margin-bottom:0.75rem;'>Milestones & Credentials</h3>", unsafe_allow_html=True)
            st.markdown("<div class='glass-card' style='padding: 1.25rem; border-radius: 12px;'>", unsafe_allow_html=True)
            
            st.markdown("<strong style='font-size:0.9rem; color:#3B82F6; display:block; margin-bottom:6px;'>🏗 Recommended Portfolio Projects</strong>", unsafe_allow_html=True)
            if parsed["projects"]:
                p_items = "".join([f"<li style='font-size:0.85rem; color:#E2E8F0; margin-bottom:6px;'>{item}</li>" for item in parsed["projects"]])
                st.markdown(f"<ul style='padding-left:16px; margin-bottom:12px;'>{p_items}</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8; margin-bottom:12px;'>No projects suggested.</p>", unsafe_allow_html=True)
                
            st.markdown("<strong style='font-size:0.9rem; color:#A855F7; display:block; margin-bottom:6px;'>🏅 Suggested Certifications</strong>", unsafe_allow_html=True)
            if parsed["certifications"]:
                c_items = "".join([f"<li style='font-size:0.85rem; color:#E2E8F0; margin-bottom:6px;'>{item}</li>" for item in parsed["certifications"]])
                st.markdown(f"<ul style='padding-left:16px; margin-bottom:0;'>{c_items}</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8; margin-bottom:0;'>No certs suggested.</p>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Month-by-Month Roadmap</h3>", unsafe_allow_html=True)
            # Render custom vertical timeline
            render_timeline(parsed["timeline"])
            
        # Interview prep tips block
        if parsed["interview_tips"]:
            st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.25rem; color:#FFFFFF; margin-bottom:0.75rem;'>Roadmap Interview Preparation Tips</h3>", unsafe_allow_html=True)
            
            tips_html = ""
            for tip in parsed["interview_tips"]:
                tips_html += f"""
                <div class="glass-card" style="padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; border-left: 2px solid #3B82F6;">
                    <div style="font-size: 0.88rem; color: #E2E8F0;">{tip}</div>
                </div>
                """
            st.markdown(tips_html, unsafe_allow_html=True)
            
        # Save Report
        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        if st.button("Save Career Roadmap Report", key="save_roadmap_btn"):
            saved = st.session_state.get(SESSION_KEYS["saved_reports"], [])
            saved.append({
                "type": "Career Roadmap",
                "filename": filename,
                "score": 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "details": f"Target Goal: {goal_input}\n\nRoadmap Output:\n{cached_roadmap}"
            })
            st.session_state[SESSION_KEYS["saved_reports"]] = saved
            st.toast("Career roadmap report saved!", icon="💾")
    elif not goal_input.strip() and run_roadmap:
        st.warning("Please enter your career goal first.")
