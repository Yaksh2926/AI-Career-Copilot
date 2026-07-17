"""
pages/linkedin.py
------------------
Calls POST /linkedin-profile and renders headline, About, skills, SEO
keywords, and networking tips as separate glass cards.
"""

import streamlit as st

import api
from components.loading import run_loading_sequence
from components.result_view import (
    render_alert,
    render_chips,
    render_download_bar,
    render_markdown_card,
    render_section_header,
)
from components.uploader import render_uploader
from utils.helpers import extract_bullets, find_section, split_numbered_sections


def render() -> None:
    render_section_header("💼", "LinkedIn Optimizer")
    st.caption("Turn your resume into a LinkedIn profile that gets discovered.")

    if not st.session_state.get("resume_filename"):
        render_alert("info", "No resume uploaded yet", "Upload a resume first to optimize your LinkedIn profile.")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_uploader(compact=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    run = st.button("Generate LinkedIn Profile", type="primary", key="run_linkedin")
    st.markdown("</div>", unsafe_allow_html=True)

    if run:
        steps = ["Reading resume...", "Calling Gemini...", "Optimizing your profile..."]
        with run_loading_sequence(steps):
            ok, payload = api.linkedin_profile(st.session_state["resume_filename"])

        if ok and payload.get("success"):
            st.session_state["linkedin_result"] = payload["data"]["linkedin_profile"]
        else:
            message = payload if isinstance(payload, str) else "LinkedIn profile generation failed."
            render_alert("error", "Generation failed", message)

    result = st.session_state.get("linkedin_result")
    if not result:
        return

    st.write("")
    sections = split_numbered_sections(result)

    headline = find_section(sections, "headline")
    about = find_section(sections, "about")
    skills = find_section(sections, "skill")
    seo = find_section(sections, "seo", "keyword")
    networking = find_section(sections, "networking")
    experience = find_section(sections, "experience")

    if sections:
        if headline:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**🏷️ Headline**")
            st.markdown(f"> {headline.strip()}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")

        if about:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**📝 About**")
            st.markdown(about)
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")

        col1, col2 = st.columns(2)
        with col1:
            if skills:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**🧩 Top Skills**")
                render_chips(extract_bullets(skills), variant="neutral")
                st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            if seo:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**🔍 SEO Keywords**")
                render_chips(extract_bullets(seo), variant="keyword")
                st.markdown("</div>", unsafe_allow_html=True)

        if experience:
            st.write("")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**💼 Experience Section Improvements**")
            st.markdown(experience)
            st.markdown("</div>", unsafe_allow_html=True)

        if networking:
            st.write("")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**🤝 Networking Tips**")
            st.markdown(networking)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("View full raw profile"):
            st.markdown(result)
    else:
        render_markdown_card(result)

    st.write("")
    render_download_bar(
        result,
        filename_base=f"linkedin_profile_{st.session_state['resume_filename']}",
        title="LinkedIn Profile",
        key_prefix="linkedin",
    )
