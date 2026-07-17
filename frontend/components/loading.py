"""
components/loading.py
----------------------
Replaces Streamlit's default spinner with a sequence of animated "loading
cards" (e.g. "Reading Resume...", "Calling Gemini...") so long-running AI
calls feel intentional rather than like a stalled app.

Usage:
    with run_loading_sequence(["Reading resume...", "Calling Gemini..."]):
        ok, payload = api.upload_resume(...)
"""

from contextlib import contextmanager
import time

import streamlit as st


def _render(placeholder, done_steps: list[str], active_step: str) -> None:
    html = ['<div>']
    for step in done_steps:
        html.append(
            f'<div class="loading-card"><span class="loading-check">✅</span>'
            f'<span class="loading-text done">{step}</span></div>'
        )
    html.append(
        f'<div class="loading-card"><span class="loading-spinner"></span>'
        f'<span class="loading-text">{active_step}</span></div>'
    )
    html.append("</div>")
    placeholder.markdown("".join(html), unsafe_allow_html=True)


@contextmanager
def run_loading_sequence(steps: list[str], step_delay: float = 0.35):
    """
    Animates through all steps but the last, then keeps the last step
    spinning for the duration of the wrapped block (the real network call).
    """
    if not steps:
        steps = ["Working..."]

    placeholder = st.empty()
    done: list[str] = []

    for step in steps[:-1]:
        _render(placeholder, done, step)
        time.sleep(step_delay)
        done.append(step)

    _render(placeholder, done, steps[-1])

    try:
        yield
    finally:
        placeholder.empty()
