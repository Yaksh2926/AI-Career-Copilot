"""
theme.py
--------
Loads and injects the design system (assets/styles.css) into the Streamlit
app, and exposes the color palette to other modules that need it for
inline-styled HTML (e.g. dynamically colored score rings).
"""

from pathlib import Path

import streamlit as st

from config import PALETTE

_CSS_PATH = Path(__file__).parent / "assets" / "styles.css"


def inject_theme() -> None:
    """Inject the global stylesheet once per session render."""
    css = _CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def score_color(score: int) -> str:
    """Return a palette color name based on a 0-100 score band."""
    if score >= 75:
        return PALETTE["success"]
    if score >= 50:
        return PALETTE["warning"]
    return PALETTE["danger"]


def configure_page(page_title: str = "AI Career Copilot") -> None:
    """Set Streamlit page config. Must be the first Streamlit call."""
    st.set_page_config(
        page_title=page_title,
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )
