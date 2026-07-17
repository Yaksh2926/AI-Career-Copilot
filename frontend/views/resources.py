import streamlit as st

def show_resources():
    """
    Renders curated list of career resources as high-quality glass cards.
    """
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">Curated Career Resources</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Accelerate your preparation with these vetted external tools and handbooks.</p>
    </div>
    """, unsafe_allow_html=True)
    
    resources_data = [
        {
            "category": "Algorithm Practice",
            "title": "LeetCode Patterns",
            "desc": "Master the 75 most essential coding interview questions covering arrays, trees, and dynamic programming.",
            "link": "https://leetcode.com/",
            "badge": "Coding Prep"
        },
        {
            "category": "System Design",
            "title": "System Design Primer",
            "desc": "An open-source handbook containing diagrams and cheat sheets explaining scaling, load balancing, and database shading.",
            "link": "https://github.com/donnemartin/system-design-primer",
            "badge": "Design Prep"
        },
        {
            "category": "Behavioral Strategy",
            "title": "The STAR Outreach Method",
            "desc": "Understand how to structure your answers using Situation, Task, Action, and Result formats.",
            "link": "https://www.inc.com/",
            "badge": "HR Prep"
        },
        {
            "category": "Resume Templates",
            "title": "Deedy-Resume Template",
            "desc": "A popular, clean LaTeX/PDF layout designed to pass standard Applicant Tracking Systems with ease.",
            "link": "https://github.com/deedy/Deedy-Resume",
            "badge": "ATS Format"
        },
        {
            "category": "Outreach & Networking",
            "title": "Cold Emailing Templates",
            "desc": "Proven high-conversion outreach email copy to message engineering managers directly on LinkedIn.",
            "link": "https://www.linkedin.com/",
            "badge": "Outreach"
        },
        {
            "category": "Developer Portfolios",
            "title": "Vercel Portfolio Starters",
            "desc": "One-click deployment templates on Next.js to host your developer portfolio, projects, and personal blog.",
            "link": "https://vercel.com/templates",
            "badge": "Deployments"
        }
    ]
    
    col1, col2 = st.columns(2, gap="large")
    
    for idx, res in enumerate(resources_data):
        target_col = col1 if idx % 2 == 0 else col2
        
        with target_col:
            card_html = f"""
            <div class="glass-card" style="padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-top: 3px solid #3B82F6;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <span style="font-size: 0.7rem; color: #3B82F6; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{res['category']}</span>
                    <span class="chip chip-primary" style="margin: 0; font-size: 0.65rem; padding: 2px 8px;">{res['badge']}</span>
                </div>
                <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-top: 4px; margin-bottom: 8px;">{res['title']}</h3>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin-bottom: 16px;">{res['desc']}</p>
                <a href="{res['link']}" target="_blank" class="sidebar-upgrade-btn" style="display: inline-block; width: auto; padding: 6px 16px; font-size: 0.8rem; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.08); box-shadow: none;">
                    Explore Asset ➔
                </a>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
