"""
components/uploader.py
-----------------------
Drag-and-drop resume uploader. On successful upload, the filename returned
by the backend is stored in `st.session_state["resume_filename"]` so every
other page can reuse it without asking the user to upload again, exactly as
the backend expects (`filename` is required by /ats-score, /career-roadmap,
/interview-questions, /cover-letter, and /linkedin-profile).
"""

import streamlit as st

import api
from components.loading import run_loading_sequence
from components.result_view import render_alert


def render_uploader(compact: bool = False) -> None:
    if not compact:
        st.markdown(
            '<div class="section-header"><span class="icon">📤</span><h3>Upload your resume</h3></div>',
            unsafe_allow_html=True,
        )

    if st.session_state.get("resume_filename"):
        st.markdown(
            f"""
            <div class="upload-badge">✅ Using resume: <strong>{st.session_state['resume_filename']}</strong></div>
            """,
            unsafe_allow_html=True,
        )
        col_a, col_b = st.columns([1, 5])
        with col_a:
            if st.button("Replace file", key="replace_resume"):
                st.session_state["resume_filename"] = None
                st.session_state["resume_analysis"] = None
                st.rerun()
        return

    uploaded = st.file_uploader(
        "Drag and drop your resume here (PDF only)",
        type=["pdf"],
        key="resume_uploader",
        label_visibility="collapsed" if compact else "visible",
    )

    if uploaded is not None:
        steps = ["Reading resume...", "Extracting text...", "Calling Gemini...", "Analyzing resume..."]
        with run_loading_sequence(steps):
            ok, payload = api.upload_resume(
                uploaded.getvalue(), uploaded.name, uploaded.type or "application/pdf"
            )

        if ok and payload.get("success"):
            data = payload.get("data", {})
            st.session_state["resume_filename"] = data.get("filename")
            st.session_state["resume_analysis"] = data.get("analysis")
            st.rerun()
        else:
            message = payload if isinstance(payload, str) else "Resume analysis failed."
            render_alert("error", "Upload failed", message)
