import streamlit as st
from frontend.config import SESSION_KEYS
from frontend.api import api_career_chat
from frontend.components.chat_interface import render_chat_interface, render_typing_indicator

def show_career_chat():
    """
    Displays the AI Career Chat Page, implementing a ChatGPT-like interface.
    """
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-family:'Outfit', sans-serif; font-weight:800; font-size:2rem; margin-bottom: 0.25rem;">Career Chat Mentor</h1>
        <p style="color:#94A3B8; font-size:0.9rem;">Receive encouraging, practical career advice and interview strategies in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Initialize chat history in session state
    if SESSION_KEYS["chat_history"] not in st.session_state:
        st.session_state[SESSION_KEYS["chat_history"]] = []
        
    chat_history = st.session_state[SESSION_KEYS["chat_history"]]

    # Container to hold chat bubbles
    chat_container = st.container()

    # 2. Render existing messages
    with chat_container:
        render_chat_interface(chat_history)

    # 3. User message input
    user_prompt = st.chat_input("Ask your AI Career Mentor a question...")

    if user_prompt:
        # Append user message
        chat_history.append({"role": "user", "content": user_prompt})
        st.session_state[SESSION_KEYS["chat_history"]] = chat_history
        
        # Redraw page to show user message immediately
        with chat_container:
            render_chat_interface(chat_history)
            
        # Draw typing bubble
        with chat_container:
            render_typing_indicator()
            
        # Send query to FastAPI Career Chat
        res = api_career_chat(user_prompt)
        
        if res.get("success"):
            reply = res["data"]["answer"]
            # Append AI reply
            chat_history.append({"role": "assistant", "content": reply})
            st.session_state[SESSION_KEYS["chat_history"]] = chat_history
        else:
            chat_history.append({"role": "assistant", "content": f"I apologized, but I encountered an error: {res.get('message')}"})
            st.session_state[SESSION_KEYS["chat_history"]] = chat_history
            
        # Trigger page update to display the response and clear typing indicator
        st.rerun()
        
    # Reset chat button
    if chat_history:
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("Clear Conversation History", key="clear_chat_btn"):
            st.session_state[SESSION_KEYS["chat_history"]] = []
            st.toast("Conversation cleared!", icon="🧹")
            st.rerun()
