"""
components/feature_cards.py
----------------------------
Renders the animated glass feature-card grid on the dashboard, and wires
each card's "Open" button to navigate to the corresponding page.
"""

import streamlit as st

from config import FEATURE_CARDS
from utils.helpers import go_to, has_resume


def render_feature_cards() -> None:
    st.markdown(
        '<div class="section-header"><span class="icon">✨</span><h3>Everything you need, in one workspace</h3></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="medium")
    for i, feature in enumerate(FEATURE_CARDS):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature['icon']}</div>
                    <div class="feature-title">{feature['title']}</div>
                    <div class="feature-desc">{feature['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            disabled = feature["key"] != "chat" and not has_resume()
            btn_label = "Open →" if not disabled else "Upload resume first"
            if st.button(
                btn_label,
                key=f"card_btn_{feature['key']}",
                use_container_width=True,
                disabled=disabled,
            ):
                go_to(feature["key"])
                st.rerun()
            st.write("")
