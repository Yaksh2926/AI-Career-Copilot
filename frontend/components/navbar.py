"""
components/navbar.py
---------------------
Sidebar brand header + backend connection status indicator.
The main navigation links live in the sidebar (see app.py) — this module
only renders the brand block and a live "online/offline" pill so the user
always knows whether the FastAPI backend is reachable.
"""

import streamlit as st

import api
from config import APP_NAME


def render_sidebar_brand() -> None:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="logo-dot">🚀</div>
            <div>
                <div class="brand-text">AI Career Copilot</div>
                <div class="brand-sub">Your AI job-search partner</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_backend_status() -> None:
    """Checks (and caches for the session) whether the backend is reachable."""
    if st.session_state.get("backend_online") is None:
        ok, _ = api.health_check()
        st.session_state["backend_online"] = ok

    online = st.session_state["backend_online"]
    dot_class = "status-online" if online else "status-offline"
    label = "Backend online" if online else "Backend offline"

    st.markdown(
        f"""
        <div style="display:flex;align-items:center;font-size:12.5px;color:var(--muted);
                    padding:8px 4px 4px 4px;">
            <span class="status-dot {dot_class}"></span>{label}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not online:
        if st.button("↻ Retry connection", key="retry_backend", use_container_width=True):
            st.session_state["backend_online"] = None
            st.rerun()
