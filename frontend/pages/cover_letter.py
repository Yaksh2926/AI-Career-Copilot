"""
pages/cover_letter.py
----------------------
Calls POST /cover-letter and displays the result inside a professional
"document viewer" card with Copy / Markdown / PDF export options.
"""

import streamlit as st

import api
from components.loading import run_loading_sequence
from components.result_view import (
    render_alert,
    render_doc_viewer,
    render_download_bar,
    render_section_header,
)
from components.uploader import render_uploader


def render() -> None:
    render_section_header("✉️", "Cover Letter Generator")
    st.caption("A professional, role-specific cover letter built from your resume.")

    if not st.session_state.get("resume_filename"):
        render_alert("info", "No resume uploaded yet", "Upload a resume first to generate a cover letter.")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_uploader(compact=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company name", placeholder="e.g. Google", key="cl_company_input")
    with col2:
        role = st.text_input("Job role", placeholder="e.g. Software Engineer", key="cl_role_input")
    run = st.button("Generate Cover Letter", type="primary", key="run_cover_letter")
    st.markdown("</div>", unsafe_allow_html=True)

    if run:
        if not company.strip() or not role.strip():
            render_alert("error", "Missing details", "Please provide both a company name and a job role.")
        else:
            steps = ["Reading resume...", "Matching your experience to the role...", "Calling Gemini...", "Drafting your cover letter..."]
            with run_loading_sequence(steps):
                ok, payload = api.cover_letter(st.session_state["resume_filename"], company, role)

            if ok and payload.get("success"):
                st.session_state["cover_letter_result"] = payload["data"]["cover_letter"]
            else:
                message = payload if isinstance(payload, str) else "Cover letter generation failed."
                render_alert("error", "Generation failed", message)

    result = st.session_state.get("cover_letter_result")
    if not result:
        return

    st.write("")
    render_doc_viewer(result)

    st.write("")
    render_download_bar(
        result,
        filename_base=f"cover_letter_{st.session_state['resume_filename']}",
        title="Cover Letter",
        key_prefix="cover_letter",
    )
