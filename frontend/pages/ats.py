"""
pages/ats.py
------------
Job-description matcher. Calls POST /ats-score with the stored resume
filename + a pasted job description, then renders a circular score,
matching/missing skill chips, keyword badges, and recommendations.
"""

import streamlit as st

import api
from components.loading import run_loading_sequence
from components.result_view import (
    render_alert,
    render_chips,
    render_download_bar,
    render_markdown_card,
    render_score_ring,
    render_section_header,
    render_divider,
)
from components.uploader import render_uploader
from utils.helpers import extract_bullets, extract_score, find_section, split_numbered_sections


def render() -> None:
    render_section_header("🎯", "ATS Score")
    st.caption("See how well your resume matches a specific job description.")

    if not st.session_state.get("resume_filename"):
        render_alert("info", "No resume uploaded yet", "Upload a resume first to run an ATS check.")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_uploader(compact=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    jd = st.text_area(
        "Paste the job description",
        height=220,
        placeholder="Paste the full job description here...",
        key="ats_jd_input",
    )
    run = st.button("Run ATS Analysis", type="primary", key="run_ats")
    st.markdown("</div>", unsafe_allow_html=True)

    if run:
        if not jd.strip():
            render_alert("error", "Job description required", "Please paste a job description first.")
        else:
            steps = ["Reading resume...", "Comparing with job description...", "Calling Gemini...", "Scoring ATS match..."]
            with run_loading_sequence(steps):
                ok, payload = api.ats_score(st.session_state["resume_filename"], jd)

            if ok and payload.get("success"):
                st.session_state["ats_result"] = payload["data"]["ats_analysis"]
            else:
                message = payload if isinstance(payload, str) else "ATS analysis failed."
                render_alert("error", "ATS analysis failed", message)

    result = st.session_state.get("ats_result")
    if not result:
        return

    st.write("")
    score = extract_score(result)
    sections = split_numbered_sections(result)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if score is not None:
        render_score_ring(score, label="ATS Match Score")
    else:
        st.markdown("#### ATS Analysis")
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")

    matching = find_section(sections, "matching skill")
    missing = find_section(sections, "missing skill")
    keywords = find_section(sections, "keyword")
    suggestions = find_section(sections, "suggestion", "improve")

    if any([matching, missing, keywords]):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**✅ Matching Skills**")
            render_chips(extract_bullets(matching or ""), variant="match")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**⚠️ Missing Skills**")
            render_chips(extract_bullets(missing or ""), variant="missing")
            st.markdown("</div>", unsafe_allow_html=True)

        if keywords:
            st.write("")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**🔑 Important Keywords**")
            render_chips(extract_bullets(keywords), variant="keyword")
            st.markdown("</div>", unsafe_allow_html=True)

        if suggestions:
            st.write("")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**💡 Recommendations**")
            st.markdown(suggestions)
            st.markdown("</div>", unsafe_allow_html=True)

        render_divider()
        with st.expander("View full raw analysis"):
            st.markdown(result)
    else:
        render_markdown_card(result)

    st.write("")
    render_download_bar(
        result,
        filename_base=f"ats_score_{st.session_state['resume_filename']}",
        title="ATS Score Analysis",
        key_prefix="ats",
    )
