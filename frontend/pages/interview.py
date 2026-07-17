"""
pages/interview.py
-------------------
Calls POST /interview-questions and renders results in an accordion,
categorized into HR, Technical, Coding, Resume-Based, Project-Based and
Scenario-Based sections (mirroring the backend prompt's structure).
"""

import streamlit as st

import api
from components.loading import run_loading_sequence
from components.result_view import (
    render_alert,
    render_download_bar,
    render_markdown_card,
    render_section_header,
)
from components.uploader import render_uploader
from utils.helpers import categorize_interview_sections, split_numbered_sections

_CATEGORY_META = {
    "hr": ("🤝", "HR Questions"),
    "technical": ("⚙️", "Technical Questions"),
    "coding": ("💻", "Coding Questions"),
    "resume": ("📄", "Resume-Based Questions"),
    "project": ("🛠️", "Project-Based Questions"),
    "scenario": ("🧩", "Scenario-Based Questions"),
}


def render() -> None:
    render_section_header("🧠", "Interview Preparation")
    st.caption("Role-specific interview questions generated from your resume.")

    if not st.session_state.get("resume_filename"):
        render_alert("info", "No resume uploaded yet", "Upload a resume first to generate interview questions.")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_uploader(compact=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    role = st.text_input(
        "Target role",
        placeholder="e.g. Backend Developer, Data Analyst, Product Manager",
        key="interview_role_input",
    )
    run = st.button("Generate Questions", type="primary", key="run_interview")
    st.markdown("</div>", unsafe_allow_html=True)

    if run:
        if not role.strip():
            render_alert("error", "Role required", "Please enter the role you're preparing for.")
        else:
            steps = ["Reading resume...", "Analyzing target role...", "Calling Gemini...", "Generating questions..."]
            with run_loading_sequence(steps):
                ok, payload = api.interview_questions(st.session_state["resume_filename"], role)

            if ok and payload.get("success"):
                st.session_state["interview_result"] = payload["data"]["questions"]
            else:
                message = payload if isinstance(payload, str) else "Interview question generation failed."
                render_alert("error", "Generation failed", message)

    result = st.session_state.get("interview_result")
    if not result:
        return

    st.write("")
    sections = split_numbered_sections(result)
    categorized = categorize_interview_sections(sections) if sections else {}

    if any(categorized.values()):
        for key, (icon, label) in _CATEGORY_META.items():
            body = categorized.get(key)
            if not body:
                continue
            with st.expander(f"{icon}  {label}", expanded=(key == "hr")):
                st.markdown(body)
    else:
        render_markdown_card(result)

    st.write("")
    render_download_bar(
        result,
        filename_base=f"interview_questions_{st.session_state['resume_filename']}",
        title="Interview Questions",
        key_prefix="interview",
    )
