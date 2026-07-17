"""
pages/dashboard.py
-------------------
Landing page: hero, resume uploader, feature card grid.
"""

import streamlit as st

from components.feature_cards import render_feature_cards
from components.hero import render_hero
from components.uploader import render_uploader


def render() -> None:
    render_hero()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    render_uploader()
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    render_feature_cards()
