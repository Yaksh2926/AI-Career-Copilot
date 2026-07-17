"""
components/hero.py
-------------------
Large hero section rendered at the top of the dashboard page.
"""

import streamlit as st


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-badge">✨ Powered by Google Gemini</div>
            <div class="hero-title">Build Your Career<br/>With AI</div>
            <div class="hero-subtitle">
                Upload your resume once and unlock resume analysis, ATS optimization,
                a personalized career roadmap, and interview preparation — all in one place.
            </div>
            <div class="hero-pill-row">
                <div class="hero-pill">📄 Resume Analysis</div>
                <div class="hero-pill">🎯 ATS Optimization</div>
                <div class="hero-pill">🗺️ Career Roadmap</div>
                <div class="hero-pill">🧠 Interview Preparation</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
