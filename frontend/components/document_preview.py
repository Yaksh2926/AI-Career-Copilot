import streamlit as st
from frontend.utils.file_helpers import compile_markdown_report, compile_html_document

def render_document_preview(title: str, doc_text: str):
    """
    Renders the cover letter inside a premium document block.
    Includes download buttons and clipboard copy utilities.
    """
    if not doc_text:
        st.info("No document content generated yet.")
        return
        
    st.markdown(f"<h3 style='font-family:\"Outfit\", sans-serif; font-size: 1.25rem; margin-bottom: 0.5rem; color:#FFFFFF;'>{title} Preview</h3>", unsafe_allow_html=True)
    
    # Document Preview Card
    preview_html = f"""
    <div class="doc-preview-container">
        <div class="doc-text">{doc_text}</div>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Action buttons layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Copy to clipboard using JavaScript
        # Escape single quotes and backticks for safe inline JS
        js_escaped_text = doc_text.replace("\\", "\\\\").replace("`", "\\`").replace("'", "\\'").replace("\n", "\\n")
        copy_button_html = f"""
        <button onclick="navigator.clipboard.writeText('{js_escaped_text}'); alert('Document copied to clipboard!');" 
                style="
                    background: rgba(255, 255, 255, 0.05);
                    color: #FFFFFF;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 0.85rem;
                    cursor: pointer;
                    width: 100%;
                    transition: all 0.2s ease;
                "
                onmouseover="this.style.background='rgba(255,255,255,0.08)';"
                onmouseout="this.style.background='rgba(255,255,255,0.05)';"
        >
            📋 Copy to Clipboard
        </button>
        """
        st.markdown(copy_button_html, unsafe_allow_html=True)
        
    with col2:
        # Download Markdown
        md_content = compile_markdown_report(title, doc_text)
        st.download_button(
            label="⬇️ Download Markdown",
            data=md_content,
            file_name="cover_letter.md",
            mime="text/markdown",
            use_container_width=True
        )
        
    with col3:
        # Download PDF (Printable HTML)
        html_content = compile_html_document(title, doc_text)
        st.download_button(
            label="📄 Download Printable PDF",
            data=html_content,
            file_name="cover_letter.html",
            mime="text/html",
            use_container_width=True
        )
