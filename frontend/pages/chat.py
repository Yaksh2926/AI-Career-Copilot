"""
pages/chat.py
-------------
ChatGPT-style career mentor chat. Calls POST /career-chat per question.
Chat history lives in st.session_state["chat_history"] for the session.
"""

import streamlit as st

import api
from components.result_view import render_alert, render_section_header


def _render_message(role: str, content: str) -> None:
    avatar = "🧑" if role == "user" else "🤖"
    bubble_class = "user" if role == "user" else "ai"
    st.markdown(
        f"""
        <div class="chat-row {bubble_class}">
            <div class="chat-bubble {bubble_class}">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    render_section_header("💬", "Career Chat")
    st.caption("Ask anything about your career — switching fields, negotiating offers, skill gaps, and more.")

    history = st.session_state["chat_history"]

    chat_container = st.container()
    with chat_container:
        if not history:
            st.markdown(
                """
                <div class="glass-card" style="text-align:center;padding:40px;">
                    <div style="font-size:34px;margin-bottom:8px;">🤖</div>
                    <div style="font-weight:700;margin-bottom:4px;">AI Career Mentor</div>
                    <div class="muted">Ask me anything about your career — I'm here to help.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for msg in history:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-row user"><div class="chat-bubble user">{msg["content"]}</div></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown('<div class="chat-row ai"><div class="chat-bubble ai">', unsafe_allow_html=True)
                    st.markdown(msg["content"])
                    st.markdown("</div></div>", unsafe_allow_html=True)

    question = st.chat_input("Ask your career mentor anything...")

    if question:
        st.session_state["chat_history"].append({"role": "user", "content": question})

        typing_placeholder = st.empty()
        typing_placeholder.markdown(
            """
            <div class="chat-row ai">
                <div class="chat-bubble ai typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        ok, payload = api.career_chat(question)
        typing_placeholder.empty()

        if ok and payload.get("success"):
            answer = payload["data"]["answer"]
            st.session_state["chat_history"].append({"role": "ai", "content": answer})
        else:
            message = payload if isinstance(payload, str) else "Career chat failed."
            render_alert("error", "Chat failed", message)

        st.rerun()

    if history:
        if st.button("🗑️ Clear conversation", key="clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()
