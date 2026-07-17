"""
components/footer.py
---------------------
Small persistent footer shown at the bottom of every page.
"""

import streamlit as st


def render_footer() -> None:
    st.markdown(
        """
        <div class="app-footer">
            <span class="brand">AI Career Copilot</span> · Built with FastAPI + Gemini + Streamlit
            <br/>Your data stays on your machine unless you choose to share it.
        </div>
        """,
        unsafe_allow_html=True,
    )
