"""
pages/resume.py
----------------
Displays the AI resume analysis captured at upload time
(POST /upload-resume already returns `data.analysis`, so this page
never re-calls the backend — it just renders what's in session state).
"""

import streamlit as st

from components.result_view import (
    render_alert,
    render_download_bar,
    render_markdown_card,
    render_section_header,
)
from components.uploader import render_uploader
from utils.helpers import extract_score, split_numbered_sections


def render() -> None:
    render_section_header("📄", "Resume Analysis")
    st.caption("A full AI-powered breakdown of your resume: summary, skills, strengths, and score.")

    if not st.session_state.get("resume_filename"):
        render_alert(
            "info",
            "No resume uploaded yet",
            "Upload a PDF resume below to get your AI analysis.",
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_uploader(compact=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    analysis = st.session_state.get("resume_analysis") or ""

    if not analysis:
        render_alert("error", "No analysis available", "Try re-uploading your resume.")
        return

    score = extract_score(analysis)
    if score is not None:
        from components.result_view import render_score_ring

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_score_ring(score, label="Resume Score")
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

    sections = split_numbered_sections(analysis)
    if sections:
        for heading, body in sections:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"#### {heading}")
            st.markdown(body)
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")
    else:
        render_markdown_card(analysis)

    st.write("")
    render_download_bar(
        analysis,
        filename_base=f"resume_analysis_{st.session_state['resume_filename']}",
        title="Resume Analysis",
        key_prefix="resume",
    )
