import streamlit as st
from frontend.config import SESSION_KEYS
from frontend.api import api_generate_linkedin_profile
from frontend.utils.parsers import parse_linkedin_profile
import time

def show_linkedin_optimizer():
    """
    Displays the LinkedIn Profile Optimizer Page.
    """
    # 1. Check if a resume is uploaded
    filename = st.session_state.get(SESSION_KEYS["filename"])
    
    if not filename:
        st.markdown("""
        <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💼</div>
            <h3 style="font-family:'Outfit', sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.5rem;">No Active Resume Selected</h3>
            <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:1.5rem;">You need to upload your resume on the Dashboard first to run LinkedIn profile optimizations.</p>
            <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="display:inline-block; width:auto; padding:8px 24px;">Go to Dashboard</a>
        </div>
        """, unsafe_allow_html=True)
        return
        
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">LinkedIn Profile Optimizer</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Optimize profile branding, headlines, and search indexing for <strong>{filename}</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Process calculations
    run_linkedin = st.button("Optimize LinkedIn Profile", key="run_linkedin_btn", use_container_width=True)
    
    # Read cached linkedin optimization if available
    cached_linkedin = st.session_state.get(SESSION_KEYS["linkedin"])
    
    # Reset cache if comparison is triggered
    if run_linkedin:
        with st.spinner(""):
            status_container = st.empty()
            steps = ["Assessing Brand Presence...", "Generating Catchy Headlines...", "Writing Immersive Story About Section...", "Indexing Core Capabilities...", "Extracting High-impact Keywords...", "Compiling Outreach Methods..."]
            for step in steps:
                status_container.markdown(f"""
                <div class="premium-loader-container">
                    <div class="premium-loader-circle"></div>
                    <div class="loader-status-text">{step}</div>
                    <div class="loader-sub-text">Polishing professional profiles with Gemini</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.7)
                
            res = api_generate_linkedin_profile(filename)
            
            if res.get("success"):
                cached_linkedin = res["data"]["linkedin_profile"]
                st.session_state[SESSION_KEYS["linkedin"]] = cached_linkedin
                st.toast("LinkedIn optimization complete!", icon="💼")
            else:
                status_container.empty()
                st.error(res.get("message", "LinkedIn generation failed"))
                return
            status_container.empty()
            
    if cached_linkedin:
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
        
        parsed = parse_linkedin_profile(cached_linkedin)
        
        col1, col2 = st.columns([5, 7], gap="large")
        
        with col1:
            # 1. Headline card
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Professional Headline</h3>", unsafe_allow_html=True)
            if parsed["headline"]:
                st.markdown(f"""
                <div class="glass-card" style="padding: 1.5rem; border-radius: 12px; border-top: 4px solid #7C3AED; margin-bottom: 1.5rem;">
                    <div style="font-family:'Outfit', sans-serif; font-size: 1.05rem; font-weight: 600; line-height: 1.4; color: #FFFFFF;">
                        "{parsed["headline"]}"
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Small clipboard button
                js_escaped_headline = parsed["headline"].replace("'", "\\'").replace('"', '\\"')
                st.markdown(f"""
                <button onclick="navigator.clipboard.writeText('{js_escaped_headline}'); alert('Headline copied!');" 
                        style="
                            background: rgba(255, 255, 255, 0.05);
                            color: #FFFFFF;
                            border: 1px solid rgba(255, 255, 255, 0.1);
                            padding: 6px 12px;
                            border-radius: 6px;
                            font-size: 0.8rem;
                            cursor: pointer;
                            margin-bottom: 1.5rem;
                        "
                >
                    📋 Copy Headline
                </button>
                """, unsafe_allow_html=True)
                
            # 2. Skills & SEO Keywords
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>SEO Keyword & Skill Index</h3>", unsafe_allow_html=True)
            st.markdown("<div class='glass-card' style='padding: 1.25rem; border-radius: 12px;'>", unsafe_allow_html=True)
            
            st.markdown("<strong style='font-size:0.9rem; color:#A855F7; display:block; margin-bottom:8px;'>Top 15 Profile Skills</strong>", unsafe_allow_html=True)
            if parsed["skills"]:
                chips = "".join([f"<span class='chip chip-primary'>{s}</span>" for s in parsed["skills"]])
                st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8;'>No skill recommendations listed.</p>", unsafe_allow_html=True)
                
            st.markdown("<strong style='font-size:0.9rem; color:#3B82F6; display:block; margin-top:16px; margin-bottom:8px;'>Target SEO Search Keywords</strong>", unsafe_allow_html=True)
            if parsed["keywords"]:
                chips = "".join([f"<span class='chip chip-primary' style='border-color: rgba(59, 130, 246, 0.25); color: #3B82F6;'>{s}</span>" for s in parsed["keywords"]])
                st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8;'>No target SEO keywords generated.</p>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            # 3. About Section
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Storytelling About Section</h3>", unsafe_allow_html=True)
            if parsed["about"]:
                st.markdown(f"""
                <div class="glass-card" style="padding: 1.5rem; border-radius: 12px; line-height: 1.6; font-size: 0.9rem; color: #E2E8F0; max-height: 380px; overflow-y: auto;">
                    {parsed["about"].replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Copy About button
                js_escaped_about = parsed["about"].replace("\\", "\\\\").replace("`", "\\`").replace("'", "\\'").replace("\n", "\\n")
                st.markdown(f"""
                <button onclick="navigator.clipboard.writeText('{js_escaped_about}'); alert('About text copied!');" 
                        style="
                            background: rgba(255, 255, 255, 0.05);
                            color: #FFFFFF;
                            border: 1px solid rgba(255, 255, 255, 0.1);
                            padding: 6px 12px;
                            border-radius: 6px;
                            font-size: 0.8rem;
                            cursor: pointer;
                            margin-top: 0.75rem;
                            margin-bottom: 1.5rem;
                        "
                >
                    📋 Copy About Section
                </button>
                """, unsafe_allow_html=True)
                
        # Improvements and Networking Tips row
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)
        col3, col4 = st.columns(2, gap="large")
        
        with col3:
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Suggested Experience Fixes</h3>", unsafe_allow_html=True)
            st.markdown("<div class='glass-card' style='padding: 1.25rem; border-radius: 12px;'>", unsafe_allow_html=True)
            if parsed["improvements"]:
                fixes_html = "".join([f"<li style='font-size:0.85rem; color:#E2E8F0; margin-bottom: 8px;'>{item}</li>" for item in parsed["improvements"]])
                st.markdown(f"<ul style='padding-left:16px; margin:0;'>{fixes_html}</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8; margin:0;'>No experience adjustments recommended.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col4:
            st.markdown("<h3 style='font-family:\"Outfit\", sans-serif; font-size:1.15rem; color:#FFFFFF; margin-bottom:0.75rem;'>Networking & Outreach Tips</h3>", unsafe_allow_html=True)
            st.markdown("<div class='glass-card' style='padding: 1.25rem; border-radius: 12px;'>", unsafe_allow_html=True)
            if parsed["networking"]:
                tips_html = "".join([f"<li style='font-size:0.85rem; color:#E2E8F0; margin-bottom: 8px;'>{item}</li>" for item in parsed["networking"]])
                st.markdown(f"<ul style='padding-left:16px; margin:0;'>{tips_html}</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:0.85rem; color:#94A3B8; margin:0;'>No networking tips suggested.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Save Report
        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        if st.button("Save LinkedIn Optimizations", key="save_linkedin_btn"):
            saved = st.session_state.get(SESSION_KEYS["saved_reports"], [])
            saved.append({
                "type": "LinkedIn Optimization",
                "filename": filename,
                "score": 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "details": f"LinkedIn Optimizer Output:\n{cached_linkedin}"
            })
            st.session_state[SESSION_KEYS["saved_reports"]] = saved
            st.toast("LinkedIn optimization report saved!", icon="💾")
