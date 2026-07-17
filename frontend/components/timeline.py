import streamlit as st

def render_timeline(timeline_items: list):
    """
    Renders monthly goals in a premium vertical timeline layout.
    """
    if not timeline_items:
        st.info("No timeline roadmap compiled yet.")
        return
        
    html = '<div class="timeline-container">'
    html += '<div class="timeline-line"></div>'
    
    for i, item in enumerate(timeline_items):
        month = item.get("month", f"Month {i+1}")
        details = item.get("details", "")
        
        # Parse bullet points inside details to format list nicely
        bullet_html = ""
        lines = details.split("\n")
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("-") or line_str.startswith("*"):
                bullet_html += f"<li style='margin-bottom: 4px;'>{line_str[1:].strip()}</li>"
            elif line_str:
                bullet_html += f"<p style='margin-bottom: 8px;'>{line_str}</p>"
                
        if bullet_html.startswith("<li"):
            bullet_html = f"<ul style='margin-top: 8px; padding-left: 16px;'>{bullet_html}</ul>"
            
        html += f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="glass-card timeline-card">
                <div class="timeline-month">{month}</div>
                <div class="timeline-details">{bullet_html if bullet_html else details}</div>
            </div>
        </div>
        """
        
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
