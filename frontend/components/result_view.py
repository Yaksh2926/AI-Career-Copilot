"""
components/result_view.py
--------------------------
A library of small rendering functions used across pages to turn raw
Gemini markdown into a polished UI: alert cards, glass markdown cards,
circular score rings, skill chips, vertical timelines, and a shared
download bar (Copy / Markdown / PDF).

Never rendered: raw JSON or Python tracebacks. All errors flow through
`render_alert`.
"""

from __future__ import annotations

import streamlit as st

from theme import score_color
from utils.helpers import markdown_bytes, pdf_bytes


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------
_ALERT_ICONS = {"error": "⛔", "success": "✅", "info": "ℹ️"}


def render_alert(kind: str, title: str, message: str) -> None:
    icon = _ALERT_ICONS.get(kind, "ℹ️")
    st.markdown(
        f"""
        <div class="alert-card alert-{kind}">
            <div style="font-size:20px;">{icon}</div>
            <div>
                <div class="alert-title">{title}</div>
                <div class="alert-msg">{message}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Section header
# ---------------------------------------------------------------------------
def render_section_header(icon: str, title: str) -> None:
    st.markdown(
        f'<div class="section-header"><span class="icon">{icon}</span><h3>{title}</h3></div>',
        unsafe_allow_html=True,
    )


def render_divider() -> None:
    st.markdown('<hr class="divider-soft"/>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Glass markdown card (fallback renderer used by every page)
# ---------------------------------------------------------------------------
def render_markdown_card(markdown_text: str) -> None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(markdown_text)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Score ring
# ---------------------------------------------------------------------------
def render_score_ring(score: int, label: str = "Score") -> None:
    color = score_color(score)
    angle = int(360 * (score / 100))
    st.markdown(
        f"""
        <div class="score-ring-wrap">
            <div class="score-ring" style="background: conic-gradient({color} {angle}deg, rgba(255,255,255,0.08) {angle}deg);">
                <div class="score-ring-inner">
                    <div class="score-num" style="color:{color};">{score}</div>
                    <div class="score-den">/ 100</div>
                </div>
            </div>
            <div>
                <div style="font-weight:700;font-size:16px;margin-bottom:4px;">{label}</div>
                <div class="muted" style="font-size:13.5px;">
                    {"Excellent match" if score >= 75 else "Room to improve" if score >= 50 else "Needs work"}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Chips
# ---------------------------------------------------------------------------
def render_chips(items: list[str], variant: str = "neutral") -> None:
    if not items:
        st.markdown('<span class="muted">Nothing to show.</span>', unsafe_allow_html=True)
        return
    chips_html = "".join(f'<span class="chip chip-{variant}">{item}</span>' for item in items)
    st.markdown(chips_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Timeline
# ---------------------------------------------------------------------------
def render_timeline(items: list[tuple[str, str]]) -> None:
    # Render dots/labels via HTML, then bodies as native markdown so nested
    # bullet lists inside each month still format correctly.
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for label, body in items:
        st.markdown(
            f'<div class="timeline-item"><div class="timeline-dot"></div>'
            f'<div class="timeline-card"><h4>🗓️ {label}</h4>',
            unsafe_allow_html=True,
        )
        st.markdown(body)
        st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Download bar (Copy / Markdown / PDF)
# ---------------------------------------------------------------------------
def render_download_bar(content: str, filename_base: str, title: str, key_prefix: str) -> None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "⬇️ Download Markdown",
            data=markdown_bytes(content),
            file_name=f"{filename_base}.md",
            mime="text/markdown",
            use_container_width=True,
            key=f"{key_prefix}_dl_md",
        )
    with col2:
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_bytes(content, title=title),
            file_name=f"{filename_base}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key=f"{key_prefix}_dl_pdf",
        )
    with col3:
        with st.popover("📋 Copy text", use_container_width=True):
            st.caption("Click the icon in the top-right of the box to copy.")
            st.code(content, language=None)


def render_doc_viewer(content: str) -> None:
    st.markdown('<div class="doc-viewer">', unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("</div>", unsafe_allow_html=True)
