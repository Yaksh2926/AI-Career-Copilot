"""
pages/roadmap.py
-----------------
Calls POST /career-roadmap and renders the response as a vertical timeline
when month/phase headings are detected, falling back to plain markdown.
"""

import streamlit as st

import api
from components.loading import run_loading_sequence
from components.result_view import (
    render_alert,
    render_download_bar,
    render_markdown_card,
    render_section_header,
    render_timeline,
)
from components.uploader import render_uploader
from utils.helpers import split_timeline


def render() -> None:
    render_section_header("🗺️", "Career Roadmap")
    st.caption("A personalized, month-by-month learning plan based on your resume and goal.")

    if not st.session_state.get("resume_filename"):
        render_alert("info", "No resume uploaded yet", "Upload a resume first to generate a roadmap.")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_uploader(compact=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    goal = st.text_input(
        "What's your career goal?",
        placeholder="e.g. Become a Machine Learning Engineer at a product company",
        key="roadmap_goal_input",
    )
    run = st.button("Generate Roadmap", type="primary", key="run_roadmap")
    st.markdown("</div>", unsafe_allow_html=True)

    if run:
        if not goal.strip():
            render_alert("error", "Career goal required", "Please tell us what you're aiming for.")
        else:
            steps = ["Reading resume...", "Assessing current skill level...", "Calling Gemini...", "Building your roadmap..."]
            with run_loading_sequence(steps):
                ok, payload = api.career_roadmap(st.session_state["resume_filename"], goal)

            if ok and payload.get("success"):
                st.session_state["roadmap_result"] = payload["data"]["roadmap"]
            else:
                message = payload if isinstance(payload, str) else "Roadmap generation failed."
                render_alert("error", "Roadmap generation failed", message)

    result = st.session_state.get("roadmap_result")
    if not result:
        return

    st.write("")
    timeline_items = split_timeline(result)

    if timeline_items:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Your Learning Roadmap")
        render_timeline(timeline_items)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("View full raw roadmap"):
            st.markdown(result)
    else:
        render_markdown_card(result)

    st.write("")
    render_download_bar(
        result,
        filename_base=f"career_roadmap_{st.session_state['resume_filename']}",
        title="Career Roadmap",
        key_prefix="roadmap",
    )
