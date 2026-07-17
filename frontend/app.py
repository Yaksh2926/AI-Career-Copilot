"""
app.py
------
Entry point for the AI Career Copilot frontend.

Run with:
    streamlit run frontend/app.py

This file wires together the sidebar navigation, backend status indicator,
and page routing. All actual page content lives in pages/*.py; all reusable
UI pieces live in components/*.py. The FastAPI backend is untouched — this
app only ever calls it through api.py.
"""

import streamlit as st

from components.navbar import render_backend_status, render_sidebar_brand
from components.footer import render_footer
from config import ABOUT_ITEM, APP_NAME, BACKEND_URL, NAV_ITEMS, SETTINGS_ITEM
from theme import configure_page, inject_theme
from utils.helpers import go_to, has_resume, init_session_state

from pages import (
    ats,
    chat,
    cover_letter,
    dashboard,
    interview,
    linkedin,
    resume,
    roadmap,
)

PAGE_RENDERERS = {
    "dashboard": dashboard.render,
    "resume": resume.render,
    "ats": ats.render,
    "roadmap": roadmap.render,
    "interview": interview.render,
    "cover_letter": cover_letter.render,
    "linkedin": linkedin.render,
    "chat": chat.render,
}


def render_settings_page() -> None:
    from components.result_view import render_section_header

    render_section_header("⚙️", "Settings")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Backend connection**")
    st.text_input("Backend URL", value=BACKEND_URL, disabled=True,
                   help="Set the BACKEND_URL environment variable before launching Streamlit to change this.")
    st.write("")
    st.markdown("**Session**")
    st.caption("Your uploaded resume and generated results are stored only in this browser session.")
    if st.button("🗑️ Clear all session data", key="clear_session"):
        for key in list(st.session_state.keys()):
            if key != "page":
                del st.session_state[key]
        init_session_state()
        st.success("Session cleared.")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_about_page() -> None:
    from components.result_view import render_section_header

    render_section_header("ℹ️", "About")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        f"""
**{APP_NAME}** is an AI-powered career assistant that helps you analyze your resume,
optimize it for ATS systems, plan your career growth, prepare for interviews,
write cover letters, polish your LinkedIn profile, and chat with an AI career mentor.

- **Backend:** FastAPI + Google Gemini
- **Frontend:** Streamlit
- **Version:** 1.0.0
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar() -> None:
    with st.sidebar:
        render_sidebar_brand()

        current_page = st.session_state["page"]

        for key, label, icon in NAV_ITEMS:
            active = current_page == key
            disabled = key != "chat" and key != "dashboard" and not has_resume()
            wrapper_class = "nav-active" if active else ""
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True, disabled=disabled):
                go_to(key)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr class="divider-soft" style="margin:14px 0;"/>', unsafe_allow_html=True)

        for key, label, icon in (SETTINGS_ITEM, ABOUT_ITEM):
            active = current_page == key
            wrapper_class = "nav-active" if active else ""
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                go_to(key)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr class="divider-soft" style="margin:14px 0;"/>', unsafe_allow_html=True)
        render_backend_status()


def main() -> None:
    configure_page(APP_NAME)
    init_session_state()
    inject_theme()

    render_sidebar()

    page_key = st.session_state["page"]

    if page_key == "settings":
        render_settings_page()
    elif page_key == "about":
        render_about_page()
    else:
        renderer = PAGE_RENDERERS.get(page_key, dashboard.render)
        renderer()

    render_footer()


if __name__ == "__main__":
    main()
