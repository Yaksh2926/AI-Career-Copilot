import streamlit as st

def render_accordion(category_title: str, items: list):
    """
    Renders a set of interview questions in a clean glassmorphic collapsible accordion layout.
    """
    if not items:
        st.markdown(f"<p style='color: #94A3B8; font-size: 0.9rem;'>No questions generated for {category_title} yet.</p>", unsafe_allow_html=True)
        return
        
    st.markdown(f"<h3 style='font-family:\"Outfit\", sans-serif; font-size: 1.1rem; color: #7C3AED; margin-top: 1rem; margin-bottom: 0.75rem;'>{category_title} Questions</h3>", unsafe_allow_html=True)
    
    for i, item in enumerate(items):
        # Heuristic to split question and answer/explanation if they are joined
        question = item
        answer = "Click to reveal explanation and sample answer."
        
        # Check if the text contains a split pattern
        if " - " in item:
            parts = item.split(" - ", 1)
            question = parts[0]
            answer = parts[1]
        elif "Answer:" in item:
            parts = item.split("Answer:", 1)
            question = parts[0]
            answer = f"<strong>Answer:</strong> {parts[1]}"
        elif "?" in item and len(item) > item.find("?") + 10:
            q_idx = item.find("?")
            question = item[:q_idx + 1]
            answer = item[q_idx + 1:].strip()
            
        accordion_html = f"""
        <details class="accordion-item">
            <summary class="accordion-summary">
                <span>{question}</span>
            </summary>
            <div class="accordion-content">
                {answer}
            </div>
        </details>
        """
        st.markdown(accordion_html, unsafe_allow_html=True)
