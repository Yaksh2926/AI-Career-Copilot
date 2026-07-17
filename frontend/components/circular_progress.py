import streamlit as st

def render_circular_progress(score: int, label: str = "ATS Match"):
    """
    Generates a premium circular progress indicator using an animated inline SVG.
    Adapts the stroke colors to represent warning/success/danger zones.
    """
    # Circumference = 2 * pi * 42 = 263.89
    circumference = 263.89
    stroke_offset = circumference - (min(max(score, 0), 100) / 100) * circumference
    
    # Theme color definitions
    if score >= 80:
        color = "#22C55E"  # Success green
    elif score >= 55:
        color = "#F59E0B"  # Warning gold
    else:
        color = "#EF4444"  # Danger red
        
    svg_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin: 1.5rem 0;">
        <div class="circular-progress-container">
            <svg class="circular-progress-svg" viewBox="0 0 100 100">
                <!-- Outer Background Circle -->
                <circle class="circle-bg" cx="50" cy="50" r="42"></circle>
                <!-- Animated Progress Circle -->
                <circle class="circle-fg" cx="50" cy="50" r="42" 
                    stroke="{color}" 
                    stroke-dasharray="{circumference}" 
                    stroke-dashoffset="{stroke_offset}"
                ></circle>
            </svg>
            <div class="circle-text">
                <div class="circle-score" style="color: {color};">{score}%</div>
                <div class="circle-label">{label}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(svg_html, unsafe_allow_html=True)
