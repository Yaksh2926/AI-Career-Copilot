import os
import base64
import streamlit as st
from frontend.components.upload_card import render_upload_card

def get_image_base64(image_path: str) -> str:
    """
    Reads a local image and returns its base64 string to embed directly in custom HTML.
    """
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    return ""

def show_dashboard():
    """
    Renders the custom premium landing dashboard with a bold layout,
    3D tech render asset, horizontal dropzone pill, and a logo strip.
    """
    # 1. Hero Columns (Left: Text & Input bar, Right: 3D Render Image)
    col1, col2 = st.columns([6, 6], gap="large")
    
    with col1:
        hero_text = """
        <div style="margin-top: 1rem; margin-bottom: 1.5rem;">
            <h1 class="hero-title" style="font-size: 3.8rem; line-height: 1.1; font-weight: 800; letter-spacing: -2.5px; margin-bottom: 1.25rem;">
                Build Your<br>Dream Career.<br>Guaranteed.
            </h1>
            <p class="hero-subtitle" style="font-size: 1.05rem; line-height: 1.6; color: #94A3B8; max-width: 480px; margin-bottom: 2rem;">
                Optimize your resume, check ATS keyword alignment, generate vertical roadmaps, 
                and compile mock interview sets tailored to your background. All in one place.
            </p>
        </div>
        """
        st.html(hero_text)
        
        # Sleek, compact uploader pill rendered inline
        render_upload_card()
        
    with col2:
        # Load local generated abstract 3D asset and encode to base64
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "..", "assets", "tech_engine.png")
        base64_img = get_image_base64(image_path)
        
        if base64_img:
            img_html = f"""
            <div class="glass-card" style="
                padding: 8px; 
                border-radius: 20px; 
                box-shadow: 0 20px 50px rgba(124, 58, 237, 0.15); 
                border: 1px solid rgba(255, 255, 255, 0.08); 
                overflow: hidden;
                margin-top: 1rem;
                animation: float-around 15s infinite alternate ease-in-out;
            ">
                <img src="data:image/png;base64,{base64_img}" style="width: 100%; border-radius: 16px; display: block; filter: contrast(1.04) brightness(0.96);">
            </div>
            """
            st.html(img_html)
        else:
            # Fallback graphic if image is missing
            fallback_html = """
            <div class="glass-card" style="padding: 6rem 2rem; border-radius: 20px; text-align: center; border: 1px dashed rgba(255,255,255,0.08); margin-top: 1rem;">
                <div style="font-size: 4rem; animation: pulse 2s infinite;">⚙️</div>
                <div style="font-size: 0.9rem; color: #94A3B8; margin-top: 1rem;">3D Tech Graphics Asset</div>
            </div>
            """
            st.html(fallback_html)
            
    # 2. Testimonial & Client Logos Strip (Fills middle band)
    testimonial_html = """
    <div class="glass-card" style="
        padding: 1.25rem 2rem; 
        border-radius: 16px; 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        margin-top: 2.5rem; 
        margin-bottom: 2.5rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
    ">
        <!-- Testimonial -->
        <div style="display: flex; align-items: center; gap: 12px; width: 40%;">
            <div class="profile-avatar" style="background-image: url('https://api.dicebear.com/7.x/identicon/svg?seed=candidatemoiz'); width: 38px; height: 38px; border-color: #3B82F6;"></div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 700; color: #FFFFFF; line-height: 1.2;">"Incredible results."</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Moiz Ali &bull; Engineering Manager</div>
            </div>
        </div>
        
        <!-- Vertical Divider -->
        <div style="width: 1px; height: 36px; background: rgba(255,255,255,0.08);"></div>
        
        <!-- Logo Grid -->
        <div style="display: flex; gap: 16px; width: 55%; justify-content: space-around; align-items: center;">
            <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1rem; color: rgba(255,255,255,0.3); letter-spacing: -0.5px; text-transform: lowercase;">tabs</span>
            <span style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 0.95rem; color: rgba(255,255,255,0.3); text-transform: lowercase;">wonder monday</span>
            <span style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.85rem; color: rgba(255,255,255,0.3); text-transform: uppercase;">caden lane</span>
            <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 0.9rem; color: rgba(255,255,255,0.3);">❈ create</span>
        </div>
    </div>
    """
    st.html(testimonial_html)
    
    st.html("<h2 style='font-family:\"Outfit\", sans-serif; font-weight:700; font-size:1.5rem; color:#FFFFFF; margin-bottom:1.5rem;'>Interactive Application Features</h2>")
    
    # 3. Feature Cards Grid
    features = [
        {
            "id": "resume_analysis",
            "icon": "📊",
            "title": "Resume Analysis",
            "desc": "Get deep AI feedback, discover missing skills, strengths, weaknesses, and a quality score.",
        },
        {
            "id": "ats_score",
            "icon": "🎯",
            "title": "ATS Score Checker",
            "desc": "Compare your resume directly with a job description to extract gaps and match rates.",
        },
        {
            "id": "career_roadmap",
            "icon": "🗺️",
            "title": "Career Roadmap",
            "desc": "Generate custom learning roadmaps with monthly milestones based on your target goals.",
        },
        {
            "id": "interview_prep",
            "icon": "💬",
            "title": "Interview Preparation",
            "desc": "Generate HR, Technical, Coding, and Scenario questions customized to your experience.",
        },
        {
            "id": "cover_letter",
            "icon": "✉️",
            "title": "Cover Letter Gen",
            "desc": "Draft highly polished cover letters tailored for specific company openings.",
        },
        {
            "id": "linkedin_optimizer",
            "icon": "💼",
            "title": "LinkedIn Optimizer",
            "desc": "Improve your headline, about section, skill indexing, and discover target SEO keywords.",
        },
        {
            "id": "career_chat",
            "icon": "🤖",
            "title": "Career Chat Mentor",
            "desc": "Chat interactively with an AI mentor to plan career changes or negotiate job offers.",
        },
        {
            "id": "saved_reports",
            "icon": "💾",
            "title": "Saved Reports",
            "desc": "Access previously saved analyses and roadmaps anytime in this session.",
        }
    ]
    
    row1_cols = st.columns(4, gap="medium")
    row2_cols = st.columns(4, gap="medium")
    all_cols = row1_cols + row2_cols
    
    for idx, feat in enumerate(features):
        with all_cols[idx]:
            card_html = f"""
            <a href="/?page={feat['id']}" target="_self" style="text-decoration: none; color: inherit;">
                <div class="glass-card glass-card-hover feature-card" style="padding: 1.5rem; border-radius: 14px; height: 210px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div class="feature-icon-wrapper">{feat['icon']}</div>
                        <div class="feature-title">{feat['title']}</div>
                        <div class="feature-desc">{feat['desc']}</div>
                    </div>
                    <div class="feature-arrow">
                        <span>Get Started</span> ➔
                    </div>
                </div>
            </a>
            """
            st.html(card_html)
