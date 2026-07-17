import streamlit as st

def render_chat_interface(chat_history: list):
    """
    Renders the ChatGPT-styled dialog bubbles.
    """
    if not chat_history:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h3 style="font-family: 'Outfit', sans-serif; font-weight: 600; color: #FFFFFF;">AI Career Mentor</h3>
            <p style="color: #94A3B8; font-size: 0.9rem; max-width: 450px; margin: 0 auto;">
                Ask your career mentor questions about negotiation, interview preparation, portfolio reviews, or navigating career changes.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Use HTML bubbles for custom ChatGPT styles
    chat_html = '<div class="chat-container">'
    for msg in chat_history:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        
        # Clean linebreaks for HTML rendering
        html_content = content.replace("\n", "<br>")
        
        # Wrap code snippets inside styled elements
        html_content = html_content.replace("```", "<pre style='background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; font-family: monospace;'>")
        
        bubble_class = "chat-user" if role == "user" else "chat-assistant"
        role_label = "You" if role == "user" else "AI Mentor"
        
        chat_html += f"""
        <div class="chat-bubble {bubble_class}">
            <div style="font-size: 0.75rem; font-weight: 700; opacity: 0.8; margin-bottom: 4px; text-transform: uppercase;">{role_label}</div>
            <div style="font-size: 0.9rem; white-space: pre-wrap; word-break: break-word;">{content}</div>
        </div>
        """
    chat_html += '</div>'
    
    st.markdown(chat_html, unsafe_allow_html=True)

def render_typing_indicator():
    """
    Renders an animated typing bubble to give users active feedback during API calls.
    """
    indicator_html = """
    <div class="chat-bubble chat-assistant" style="align-self: flex-start; padding: 8px 16px;">
        <div style="font-size: 0.75rem; font-weight: 700; opacity: 0.8; margin-bottom: 4px; text-transform: uppercase;">AI Mentor</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """
    st.markdown(indicator_html, unsafe_allow_html=True)
